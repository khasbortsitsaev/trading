#!/usr/bin/env python3
"""Registered start-date sensitivity, reusing the existing offline engine."""
import argparse
from datetime import date
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
from run_research import ROOT, stamp, run, Settings, Rules, load_admitted_dataset


def windows(first, cutoff):
    start=date.fromisoformat(first);limit=date.fromisoformat(cutoff)
    if start.day!=1:
        raise ValueError('Monthly starts require day one')
    result=[]
    while True:
        end=date(start.year+1,start.month,1)
        if end>limit:break
        result.append((start.isoformat(),end.isoformat()))
        start=date(start.year+(start.month==12),start.month%12+1,1)
    return result


def summarize(rows):
    returns=[r['strategy_return'] for r in rows]
    excess=[r['strategy_return']-r['eth_return'] for r in rows]
    return {'windows':len(rows),'beat_eth_count':sum(x>0 for x in excess),
            'beat_eth_fraction':sum(x>0 for x in excess)/len(rows),
            'loss_count':sum(x<0 for x in returns),'median_return':statistics.median(returns),
            'worst_return':min(returns),'best_return':max(returns),
            'median_eth_return':statistics.median(r['eth_return'] for r in rows),
            'median_paired_excess_return':statistics.median(excess),
            'median_drawdown':statistics.median(r['strategy_drawdown'] for r in rows),
            'worst_drawdown':max(r['strategy_drawdown'] for r in rows),
            'median_eth_drawdown':statistics.median(r['eth_drawdown'] for r in rows),
            'worst_eth_drawdown':max(r['eth_drawdown'] for r in rows)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir',type=Path,required=True)
    parser.add_argument('--ledger-dir',type=Path,required=True)
    args=parser.parse_args()
    if ROOT==args.ledger_dir.resolve() or ROOT in args.ledger_dir.resolve().parents:
        parser.error('Keep full ledgers outside checkout')
    if subprocess.run(['git','diff','--quiet','HEAD','--','src','scripts','tests','config'],cwd=ROOT).returncode:
        raise RuntimeError('Commit implementation/configuration before running')
    policy=json.loads((ROOT/'config/research-policy.json').read_text());cfg=policy['rolling_start_analysis']
    cutoff=policy['split']['exact_utc_boundaries']['holdout_start_inclusive']
    data,manifest=load_admitted_dataset(args.data_dir,policy['dataset_admission'],stamp(cutoff))
    execution=json.loads((ROOT/'config/runner.json').read_text())
    rules={a:Rules(quantity_decimals=x['quantity_decimals'],tick=D(x['tick']),minimum_base=D(x['minimum_base']),minimum_quote=D(x['minimum_quote'])) for a,x in execution['markets'].items()}
    variants={x['id']:x for x in policy['variants']};s2=policy['poc']['s2_spec'];variants[s2['id']]=dict(s2,lookback_days=s2['trend_lookback_days'])
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    args.ledger_dir.mkdir(parents=True,exist_ok=True)
    opens={b.timestamp_ms:b.open for b in data['ETH']}
    for family,variant_id in cfg['variants'].items():
        rows=[]
        for start,end in windows(cfg['first_start'],cutoff):
            settings=Settings(initial_eth=D(cfg['initial_quote_equity'])/opens[stamp(start)],quote=manifest['quote'],source=manifest['provider'],fee=D(execution['fee_per_execution']),friction_round_trip_bps=D(execution['default_noncommission_round_trip_bps']),publication_minutes=execution['publication_lag_minutes'],processing_minutes=execution['processing_lag_minutes'],rules=rules)
            r=run(data,variants[variant_id],stamp(start),stamp(end),settings,holdout_start_ms=stamp(cutoff))
            body=json.dumps(r,sort_keys=True,separators=(',',':'),allow_nan=False).encode();digest=hashlib.sha256(body).hexdigest()
            (args.ledger_dir/f'{family}-{start}.json').write_bytes(body)
            rows.append({'start':start,'end_exclusive':end,'strategy_return':r['metrics']['total_return'],'eth_return':r['eth_benchmark_metrics']['total_return'],'strategy_drawdown':r['metrics']['maximum_drawdown'],'eth_drawdown':r['eth_benchmark_metrics']['maximum_drawdown'],'result_sha256':digest,'fills':r['orders_executed']})
        result={'experiment_id':f'{family}-002','evidence_type':'post_hoc_development_start_date_sensitivity_not_independent_validation','code_commit':commit,'dataset_sha256':manifest['normalized_sha256'],'settings':execution,'registered_design':cfg,'variant':variants[variant_id],'summary':summarize(rows),'windows':rows,'holdout_access':False,'overlapping_windows_independent':False,'full_ledgers_committed':False}
        path=ROOT/f'research/artifacts/{family}/{family.lower()}-002-rolling.json'
        path.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        print(family,json.dumps(result['summary']))


if __name__=='__main__':main()
