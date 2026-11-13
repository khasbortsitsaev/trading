"""Offline spot accounting and causal-data checks; no order submission or strategy."""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from decimal import Decimal, ROUND_DOWN

D = Decimal
UTC = timezone.utc


class DataError(ValueError):
    pass


class HoldoutAccessError(DataError):
    pass


def positive(value):
    value = D(value)
    if not value.is_finite() or value <= 0:
        raise ValueError('Expected a finite positive decimal')
    return value


def aware(value):
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError('Timestamp must be timezone-aware')
    return value.astimezone(UTC)


@dataclass(frozen=True)
class Candle:
    timestamp_ms: int
    open: D
    high: D
    low: D
    close: D
    volume: D


def audit_candles(pages, start_ms, end_ms, interval_ms=86400000, holdout_start_ms=None):
    """Merge identical overlaps, reject conflicts, expose gaps without filling them."""
    if start_ms >= end_ms or start_ms % interval_ms or end_ms % interval_ms:
        raise DataError('Window boundaries must be aligned and increasing')
    if holdout_start_ms is not None and end_ms > holdout_start_ms:
        raise HoldoutAccessError('Requested development window enters holdout')
    candles, duplicates = {}, 0
    for page in pages:
        if not isinstance(page, list):
            raise DataError('Expected a candle array, not an API error')
        for row in page:
            if len(row) != 6:
                raise DataError('Expected six candle fields')
            t = int(row[0])
            if holdout_start_ms is not None and t >= holdout_start_ms:
                raise HoldoutAccessError('Response contains a holdout candle')
            if t % interval_ms or not start_ms <= t < end_ms:
                raise DataError('Candle is misaligned or outside requested window')
            o, h, l, c = [positive(x) for x in row[1:5]]
            v = D(row[5])
            if not v.is_finite() or v < 0 or not l <= min(o, c) <= max(o, c) <= h:
                raise DataError('Invalid OHLC or volume')
            candle = Candle(t, o, h, l, c, v)
            if t in candles:
                if candles[t] != candle:
                    raise DataError('Conflicting duplicate candle')
                duplicates += 1
            candles[t] = candle
    missing = [t for t in range(start_ms, end_ms, interval_ms) if t not in candles]
    ordered = [candles[t] for t in sorted(candles)]
    return ordered, {'observations': len(ordered), 'expected': (end_ms-start_ms)//interval_ms,
                     'identical_overlaps': duplicates, 'missing_count': len(missing),
                     'missing_timestamps_ms': missing, 'ohlc_valid': True}


def deduplicate_trades(rows):
    """Caller partitions by venue/instrument; timestamp is deliberately not a key."""
    result = {}
    for row in rows:
        key = row['trade_id']
        if key in result and result[key] != row:
            raise DataError('Conflicting trade ID')
        result[key] = row
    return list(result.values())


def scheduled_reference(available_at, decision_at, bars, latency=timedelta(minutes=5), extra_bars=0):
    """Daily candle proxy: use only the designated future bar, never skip a gap."""
    available_at, decision_at = aware(available_at), aware(decision_at)
    if available_at > decision_at or latency <= timedelta(0) or extra_bars < 0:
        raise DataError('Invalid information time, latency or delay')
    ready = decision_at + latency
    start = ready.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1+extra_bars)
    # No later-bar fallback if the designated reference is missing/suspended.
    matches = [bar for bar in bars if aware(bar['start']) == start and bar.get('tradable', True)]
    if len(matches) > 1:
        raise DataError('Conflicting reference bars')
    if not matches:
        return None
    return {'start': start, 'expires': start+timedelta(days=1),
            'reference_price': positive(matches[0]['open']), 'ready_at': ready,
            'model': 'delayed_candle_proxy_not_observed_fill'}


@dataclass(frozen=True)
class Rules:
    quantity_decimals: int = 8
    tick: D = D('0.01')
    minimum_base: D = D('0')
    minimum_quote: D = D('0')


class Portfolio:
    """Atomic fill accounting in one quote currency; owned spot inventory only."""
    def __init__(self, cash='0', inventory=None):
        self.cash = D(cash)
        self.inventory = {k: D(v) for k, v in (inventory or {}).items()}
        self.events = []
        if not self.cash.is_finite() or self.cash < 0 or any(not v.is_finite() or v < 0 for v in self.inventory.values()):
            raise ValueError('Negative/nonfinite initial balances')

    def equity(self, prices):
        return self.cash + sum((q * positive(prices[a]) for a, q in self.inventory.items() if q), D(0))

    def marked_equity(self, marks, at, maximum_age):
        at = aware(at)
        if maximum_age < timedelta(0):
            raise ValueError('Invalid maximum age')
        prices = {}
        for asset, qty in self.inventory.items():
            if not qty:
                continue
            if asset not in marks:
                raise DataError('Missing inventory valuation')
            price, timestamp = marks[asset]
            age = at - aware(timestamp)
            if age < timedelta(0) or age > maximum_age:
                raise DataError('Future or stale inventory valuation')
            prices[asset] = price
        return self.equity(prices)

    def fill(self, asset, side, quantity, price, fee_rate, rules, *, decision_at,
             available_at, ready_at, fill_at, fee_asset='quote', tradable=True):
        times = [aware(x) for x in [available_at, decision_at, ready_at, fill_at]]
        if not times[0] <= times[1] < times[2] <= times[3]:
            raise DataError('Noncausal fill')
        if not tradable:
            raise DataError('Suspended/delisted market cannot fill')
        quantity, price = positive(quantity), positive(price)
        rate = D(fee_rate)
        if not rate.is_finite() or not 0 <= rate < 1 or side not in ['buy', 'sell'] or fee_asset not in ['base', 'quote']:
            raise ValueError('Invalid fee or fill mode')
        tick = positive(rules.tick)
        if rules.quantity_decimals < 0 or rules.minimum_base < 0 or rules.minimum_quote < 0:
            raise ValueError('Invalid instrument rules')
        quantum = D(1).scaleb(-rules.quantity_decimals)
        if quantity != quantity.quantize(quantum, rounding=ROUND_DOWN) or price % tick:
            raise ValueError('Unrounded quantity or off-tick price')
        notional = quantity * price
        if quantity < rules.minimum_base or notional < rules.minimum_quote:
            raise ValueError('Below market minimum; retain cash/inventory, do not round up')
        old_quantity = self.inventory.get(asset, D(0))
        fee = (notional if fee_asset == 'quote' else quantity) * rate
        if side == 'buy':
            cash = self.cash - notional - (fee if fee_asset == 'quote' else 0)
            held = old_quantity + quantity - (fee if fee_asset == 'base' else 0)
        else:
            cash = self.cash + notional - (fee if fee_asset == 'quote' else 0)
            held = old_quantity - quantity - (fee if fee_asset == 'base' else 0)
        if cash < 0 or held < 0:
            raise ValueError('Insufficient owned cash or inventory; no borrowing')
        # Commit both legs only after all checks, including fees, succeed.
        self.cash, self.inventory[asset] = cash, held
        event = {'asset': asset, 'side': side, 'quantity': str(quantity), 'price': str(price),
                 'fee': str(fee), 'fee_asset': fee_asset, 'fill_at': times[3].isoformat(),
                 'cash_after': str(cash), 'inventory_after': str(held)}
        self.events.append(event)
        return event


def validate_weights(weights):
    weights = {k: D(v) for k, v in weights.items()}
    if any(not x.is_finite() or x < 0 for x in weights.values()) or sum(weights.values(), D(0)) > 1:
        raise ValueError('Spot weights cannot borrow or use leverage')
    return weights


def report_wealth(portfolio, prices, eth_quote, usdc_quote):
    equity = portfolio.equity(prices)
    return {'quote': equity, 'eth_equivalent': equity/positive(eth_quote),
            'usdc': equity/positive(usdc_quote)}
