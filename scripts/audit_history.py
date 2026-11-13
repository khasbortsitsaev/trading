#!/usr/bin/env python3
"""Audit locally captured development candles without computing returns/signals."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from trading_research.core import audit_candles


def timestamp(date):
    return int(datetime.fromisoformat(date).replace(tzinfo=timezone.utc).timestamp()*1000)


def audit(root):
    start, cutoff, accounting = map(timestamp,['2020-01-01','2025-11-13','2021-01-01'])
    markets = {}
    for market in ['ETH-EUR','BTC-EUR','ETH-USDC','BTC-USDC','USDC-EUR']:
        pages, sources = [], []
        for path in sorted(root.glob('history-'+market+'-*.meta.json')):
            meta = json.loads(path.read_text())
            raw = root/meta['id']
            if meta['curl_exit'] or not meta['response'].startswith('200 '):
                raise ValueError('Failed source response')
            if hashlib.sha256(raw.read_bytes()).hexdigest()!=meta['sha256']:
                raise ValueError('Source hash mismatch')
            pages.append(json.loads(raw.read_text()))
            sources.append(meta)
        bars, report = audit_candles(pages,start,cutoff,holdout_start_ms=cutoff)
        report['first_returned_date'] = datetime.fromtimestamp(bars[0].timestamp_ms/1000,timezone.utc).date().isoformat() if bars else None
        report['last_returned_date'] = datetime.fromtimestamp(bars[-1].timestamp_ms/1000,timezone.utc).date().isoformat() if bars else None
        accounting_pages = [[[b.timestamp_ms,str(b.open),str(b.high),str(b.low),str(b.close),str(b.volume)] for b in bars if b.timestamp_ms>=accounting]]
        _, account_report = audit_candles(accounting_pages,accounting,cutoff,holdout_start_ms=cutoff)
        report['accounting_period_missing_days'] = account_report['missing_count']
        report['accounting_period_expected_days'] = account_report['expected']
        report['missing_timestamps_ms'] = report['missing_timestamps_ms'][:10]
        report['sources'] = sources
        markets[market] = report
    return {'scope':'Development-only quality audit. No returns, signals or holdout evaluated.',
            'raw_window_start':'2020-01-01','accounting_start':'2021-01-01',
            'development_end_exclusive':'2025-11-13','holdout_retrieved':False,
            'markets':markets}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--responses',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    result=audit(args.responses)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    for market,r in result['markets'].items():
        print(market, 'rows',r['observations'],'missing accounting days',r['accounting_period_missing_days'])
