#!/usr/bin/env python3
"""Audit registered development data without strategy or P&L calculations."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import parse_qs, urlsplit

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from trading_research.core import audit_candles, DataError
from trading_research.data import bitstamp_rows, load_admitted_dataset, DAY


def audit_capture(root: Path, plan: dict, interval_ms: int, cutoff: int) -> tuple[dict, dict, dict]:
    """Bind normalized prices back to every immutable, bounded source response."""
    raw=(root/'manifest.json').read_bytes();manifest=json.loads(raw)
    admission={'source':plan['source'],'quote':plan['quote'],
               'normalized_sha256':manifest['normalized_sha256'],
               'manifest_sha256':hashlib.sha256(raw).hexdigest(),
               'start_ms':plan['start_ms'],'end_exclusive_ms':plan['end_exclusive_ms'],
               'interval_ms':interval_ms,'markets':plan['markets']}
    panel,_=load_admitted_dataset(root,admission,cutoff,interval_ms)
    pages=defaultdict(list);seen=set()
    for record in manifest['requests']:
        asset=record['asset'];name=record['raw_file']
        if asset not in panel or Path(name).name!=name or name in seen:
            raise DataError('Unexpected or duplicate source page identity')
        seen.add(name)
        lower,upper=record['requested_start_ms'],record['requested_end_exclusive_ms']
        if not plan['start_ms']<=lower<upper<=plan['end_exclusive_ms']<=cutoff:
            raise DataError('Source request outside registered development window')
        if lower%interval_ms or upper%interval_ms or not 1<=(upper-lower)//interval_ms<=1000:
            raise DataError('Source page alignment or documented request limit violated')
        url=urlsplit(record['url'])
        expected_query={'step':[str(interval_ms//1000)],'limit':[str((upper-lower)//interval_ms)],
                        'end':[str(upper//1000-1)],'exclude_current_candle':['true']}
        if (url.scheme!='https' or url.netloc!='www.bitstamp.net'
                or url.path!=f'/api/v2/ohlc/{asset.lower()}usd/' or parse_qs(url.query)!=expected_query
                or record['http_status']!=200):
            raise DataError('Unexpected source endpoint or query')
        body=(root/name).read_bytes()
        if hashlib.sha256(body).hexdigest()!=record['sha256']:
            raise DataError('Captured raw response hash mismatch')
        sidecar=json.loads((root/Path(name).with_suffix('.meta.json')).read_text())
        if sidecar!=record:
            raise DataError('Captured page metadata differs from manifest')
        rows=bitstamp_rows(json.loads(body),asset.lower()+'usd')
        if len(rows)!=record['returned_rows']:
            raise DataError('Captured response count mismatch')
        audit_candles([rows],lower,upper,interval_ms,cutoff)
        pages[asset].append(rows)
    for asset,bars in panel.items():
        rebuilt,quality=audit_candles(pages[asset],plan['start_ms'],plan['end_exclusive_ms'],interval_ms,cutoff)
        if quality['missing_count'] or quality['identical_overlaps'] or rebuilt!=bars:
            raise DataError('Raw pages do not reconstruct the exact complete normalized panel')
    return panel,admission,manifest


def compare_intervals(daily: dict, intraday: dict, absolute_tolerance: D, relative_tolerance: D) -> dict:
    """Compare complete daily OHLCV aggregates using independent Decimal sums."""
    if set(daily)!=set(intraday):
        raise DataError('Daily and execution universes differ')
    report={}
    for asset,days in daily.items():
        grouped=defaultdict(list)
        for bar in intraday[asset]:
            grouped[bar.timestamp_ms//DAY*DAY].append(bar)
        raw_ohlc_mismatches=ohlc_mismatches=volume_mismatches=bounds_violations=0;max_volume_difference=D(0)
        for day in days:
            bars=sorted(grouped.pop(day.timestamp_ms,[]),key=lambda b:b.timestamp_ms)
            if [b.timestamp_ms for b in bars]!=list(range(day.timestamp_ms,day.timestamp_ms+DAY,900000)):
                raise DataError('Missing or duplicate intraday bar in daily aggregation')
            aggregate=(bars[0].open,max(b.high for b in bars),min(b.low for b in bars),bars[-1].close)
            raw_ohlc_mismatches+=aggregate!=(day.open,day.high,day.low,day.close)
            traded=[b for b in bars if b.volume>0]
            if not traded:
                raise DataError('Daily trade OHLC cannot be reconstructed without positive-volume bars')
            aggregate=(traded[0].open,max(b.high for b in traded),min(b.low for b in traded),traded[-1].close)
            ohlc_mismatches+=aggregate!=(day.open,day.high,day.low,day.close)
            bounds_violations+=sum(not day.low<=b.low<=b.high<=day.high for b in bars)
            difference=abs(sum((b.volume for b in bars),D(0))-day.volume)
            max_volume_difference=max(max_volume_difference,difference)
            volume_mismatches+=difference>max(absolute_tolerance,abs(day.volume)*relative_tolerance)
        if grouped:
            raise DataError('Intraday data extend beyond daily coverage')
        report[asset]={'days_compared':len(days),'intraday_rows':len(intraday[asset]),
                       'zero_volume_bars':sum(b.volume==0 for b in intraday[asset]),
                       'zero_volume_designated_0015_bars':sum(b.volume==0 and b.timestamp_ms%DAY==900000 for b in intraday[asset]),
                       'raw_all_bar_daily_ohlc_mismatch_count':raw_ohlc_mismatches,
                       'daily_ohlc_mismatch_count':ohlc_mismatches,'intraday_bound_violations':bounds_violations,
                       'volume_tolerance_failures':volume_mismatches,'maximum_volume_sum_difference_base':str(max_volume_difference)}
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--daily-data-dir',type=Path,required=True)
    p.add_argument('--execution-data-dir',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if subprocess.run(['git','diff','--quiet','HEAD','--','src','scripts','tests','config'],cwd=ROOT).returncode:
        raise RuntimeError('Commit implementation/configuration before auditing market data')
    policy=json.loads((ROOT/'config/research-policy.json').read_text());plan=policy['intraday_admission_plan']
    cutoff=int(datetime.fromisoformat(
        policy['split']['exact_utc_boundaries']['holdout_start_inclusive']).replace(
            tzinfo=timezone.utc).timestamp()*1000)
    daily,daily_admission,daily_manifest=audit_capture(args.daily_data_dir,plan,DAY,cutoff)
    if daily_admission['normalized_sha256']!=plan['daily_normalized_sha256_required']:
        raise DataError('Recovered daily normalized prices differ from frozen original; separate review required')
    intraday,admission,manifest=audit_capture(args.execution_data_dir,plan,plan['interval_ms'],cutoff)
    comparisons=compare_intervals(daily,intraday,D(plan['volume_absolute_tolerance_base']),D(plan['volume_relative_tolerance']))
    recommended=all(not (r['daily_ohlc_mismatch_count'] or r['intraday_bound_violations'] or r['volume_tolerance_failures'])
                    for r in comparisons.values())
    result={'experiment_id':'DATA-001','evidence_type':'source_data_quality_audit_not_strategy_performance',
            'code_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
            'registered_plan':plan,'admission_recommended':recommended,'comparisons':comparisons,
            'daily_recovery_admission':daily_admission,'execution_admission_candidate':admission,
            'raw_pages_verified':{'daily':len(daily_manifest['requests']),'intraday':len(manifest['requests'])},
            'raw_pages_exactly_reconstruct_normalized':True,'original_daily_prices_identical':True,
            'holdout_accessed':False,'strategy_runs':0,'costs_calibrated':False,
            'limitations':['OHLC opens are not executable quotes or first-trade timestamp measurements',
                           'Historical publication/receipt latencies are assumed, not measured',
                           'Bitstamp USD candles do not reconstruct Bitvavo USDC execution or spreads']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'admission_recommended':recommended,'comparisons':comparisons,'raw_pages_verified':result['raw_pages_verified']},indent=2))
    if not recommended:
        raise SystemExit('Data admission blocked by registered QA criteria')


if __name__=='__main__':
    main()
