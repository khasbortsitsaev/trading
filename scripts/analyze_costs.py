#!/usr/bin/env python3
"""Audit local public-book snapshots under explicit synthetic cost assumptions.

No networking, order placement, credentials, backtesting or third-party packages.
Raw input responses stay outside git. See research/reports/costs.md for interpretation.
"""
import argparse
from decimal import Decimal, ROUND_DOWN
import hashlib
import json
from pathlib import Path

D = Decimal
ONE = D(1)
BPS = D(10000)


def commission_hurdle(buy_fee, sell_fee):
    """Gross executed-price return needed when both fees are in quote currency."""
    if not (0 <= buy_fee < 1 and 0 <= sell_fee < 1):
        raise ValueError('Fee must be a fraction between zero and one')
    return (ONE + buy_fee) / (ONE - sell_fee) - ONE


def sweep(levels, quantity):
    """Quote notional for quantity, or None if displayed depth is insufficient."""
    if quantity <= 0:
        raise ValueError('Quantity must be positive')
    remaining, total = quantity, D(0)
    for price, size in levels:
        fill = min(remaining, size)
        total += fill * price
        remaining -= fill
        if remaining == 0:
            return total
    return None


def affordable_quantity(asks, quote_budget, fee, decimals):
    """Reserve quote fees and round down; never extrapolate beyond the book."""
    if quote_budget <= 0 or not 0 <= fee < 1 or decimals < 0:
        raise ValueError('Invalid budget, fee or precision')
    remaining, quantity = quote_budget / (ONE + fee), D(0)
    for price, size in asks:
        fill = min(size, remaining / price)
        quantity += fill
        remaining -= fill * price
        # Decimal division can leave tiny residuals; quantity is rounded down below.
        if fill < size or remaining <= 0:
            return quantity.quantize(D(1).scaleb(-decimals), rounding=ROUND_DOWN)
    return None


def parse_book(payload, venue):
    if venue == 'kraken':
        if payload.get('error'):
            raise ValueError(f'Kraken returned an API error: {payload["error"]}')
        books = list(payload['result'].values())
        if len(books) != 1:
            raise ValueError('Expected exactly one Kraken book')
        payload = books[0]
    book = {side: [(D(x[0]), D(x[1])) for x in payload[side]]
            for side in ('bids', 'asks')}
    for side, reverse in [('bids', True), ('asks', False)]:
        levels = book[side]
        if not levels or any(p <= 0 or q <= 0 for p, q in levels):
            raise ValueError('Empty book or non-positive price/size')
        if levels != sorted(levels, key=lambda x: x[0], reverse=reverse):
            raise ValueError('Book prices are out of order')
    if book['bids'][0][0] >= book['asks'][0][0]:
        raise ValueError('Crossed or locked book')
    return book


def midpoint(book):
    return (book['bids'][0][0] + book['asks'][0][0]) / 2


def analyze(response_dir, config):
    rows = []
    for path in sorted(response_dir.glob('*-r[0-9]*.meta.json')):
        meta = json.loads(path.read_text())
        identity = meta['id']
        venue, rest = identity.split('-', 1)
        pair, round_id = rest.rsplit('-', 1)
        if venue not in config['markets']:
            continue
        if meta['curl_exit'] != 0 or not meta['response'].startswith('200 '):
            raise ValueError(f'Unsuccessful response: {identity}')
        body = response_dir / identity
        if hashlib.sha256(body.read_bytes()).hexdigest() != meta['sha256']:
            raise ValueError(f'Response hash mismatch: {identity}')
        book = parse_book(json.loads(body.read_text()), venue)
        quote = pair.split('-')[1]
        eth = parse_book(json.loads((response_dir / f'{venue}-ETH-{quote}-{round_id}').read_text()), venue)
        equity = D(config['initial_eth']) * midpoint(eth)
        regime = config['markets'][venue][pair]
        fee = D(config['fee_regimes'][regime]['taker'])
        spread = (book['asks'][0][0] - book['bids'][0][0]) / midpoint(book) * BPS
        outcomes = []
        for fraction in map(D, config['equity_fractions']):
            budget = equity * fraction
            qty = affordable_quantity(book['asks'], budget, fee,
                                      config['base_quantity_decimals'][pair.split('-')[0]])
            if qty is None or qty <= 0:
                outcomes.append({'equity_fraction': str(fraction), 'insufficient_depth': True})
                continue
            buy = sweep(book['asks'], qty)
            sell = sweep(book['bids'], qty)
            if buy is None or sell is None:
                outcomes.append({'equity_fraction': str(fraction), 'insufficient_depth': True})
                continue
            spent = buy * (ONE + fee)
            if spent > budget:
                raise ValueError('Rounded size exceeds fee-inclusive quote budget')
            proceeds = sell * (ONE - fee)
            outcomes.append({
                'equity_fraction': str(fraction), 'quote_budget': str(budget),
                'base_quantity': str(qty), 'insufficient_depth': False,
                'fee_inclusive_spend': str(spent),
                'unspent_quote': str(budget - spent),
                'depth_buy_bps_beyond_best_ask': str((buy / qty / book['asks'][0][0] - ONE) * BPS),
                'depth_sell_bps_beyond_best_bid': str((ONE - sell / qty / book['bids'][0][0]) * BPS),
                'frozen_book_loss_bps_before_fees': str((ONE - sell / buy) * BPS),
                'frozen_book_loss_bps_with_taker_fees': str((ONE - proceeds / spent) * BPS),
                'gross_hurdle_bps_with_taker_fees': str((spent / proceeds - ONE) * BPS),
            })
        rows.append({'source_id': identity, 'venue': venue, 'pair': pair,
                     'round': round_id, 'observed_at_utc': meta['observed_at_utc'],
                     'sha256': meta['sha256'], 'fee_regime': regime,
                     'spread_bps': str(spread), 'sizes': outcomes})
    if not rows:
        raise ValueError('No matching response snapshots; refusing a zero-sample audit')
    return {'scope': 'Frozen-book scenarios, not fills, P&L or calibrated future costs',
            'model_as_of': config['as_of'], 'snapshot_count': len(rows), 'observations': rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--responses', type=Path, required=True)
    parser.add_argument('--model', type=Path, default=Path('config/cost-model.json'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = analyze(args.responses, json.loads(args.model.read_text()))
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(f'Analyzed {result["snapshot_count"]} snapshots; output: {args.output}')


if __name__ == '__main__':
    main()
