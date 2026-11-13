#!/usr/bin/env python3
"""Run a registered offline variant on synthetic or admitted development data."""
import argparse
from datetime import datetime,timezone
from decimal import Decimal as D
import hashlib
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from trading_research.data import load_admitted_dataset
from trading_research.engine import run,Settings
from trading_research.core import Rules
from trading_research import synthetic


def stamp(day):
    return int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp()*1000)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    source=p.add_mutually_exclusive_group(required=True)
    source.add_argument('--synthetic',action='store_true')
    source.add_argument('--data-dir',type=Path)
    p.add_argument('--proxy-usd',action='store_true',help='Explicitly acknowledge USD source/USDC execution-cost mismatch')
    p.add_argument('--variant',default='TREND-20')
    p.add_argument('--start',default='2021-01-01')
    p.add_argument('--end-exclusive',default='2021-07-20')
    p.add_argument('--friction-bps',help='Override config/runner.json round-trip friction for a recorded scenario')
    p.add_argument('--extra-delay-bars',type=int,default=0)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--summary',type=Path)
    args=p.parse_args()
    policy=json.loads((ROOT/'config/research-policy.json').read_text())
    variants={x['id']:x for x in policy['variants']}
    if args.variant not in variants:
        p.error('Variant is not in the frozen policy')
    if not args.synthetic and args.variant != policy['poc']['active_variant']:
        p.error('POC is focused on TREND-20; preregister a scope change before another historical variant')
    cutoff=stamp(policy['split']['exact_utc_boundaries']['holdout_start_inclusive'])
    if args.synthetic:
        data=synthetic.panel()
        body=json.dumps({a:[[x.timestamp_ms,str(x.open),str(x.high),str(x.low),str(x.close),str(x.volume)] for x in bars] for a,bars in data.items()},sort_keys=True).encode()
        dataset_hash=hashlib.sha256(body).hexdigest();quote='USDC';provider='synthetic'
    else:
        if not policy['real_data_search_authorized_by_this_file']:
            p.error('Development dataset is not yet admitted by the policy')
        if args.output.resolve()==ROOT or ROOT in args.output.resolve().parents:
            p.error('Keep the full source-derived ledger outside the public checkout')
        if not args.proxy_usd:
            p.error('Explicit --proxy-usd acknowledgement is required')
        data,manifest=load_admitted_dataset(args.data_dir,policy['dataset_admission'],cutoff)
        dataset_hash=manifest['normalized_sha256']
        quote=manifest['quote'];provider=manifest['provider']
    execution=json.loads((ROOT/'config/runner.json').read_text())
    rules={a:Rules(quantity_decimals=x['quantity_decimals'],tick=D(x['tick']),
                   minimum_base=D(x['minimum_base']),minimum_quote=D(x['minimum_quote']))
           for a,x in execution['markets'].items()}
    result=run(data,variants[args.variant],stamp(args.start),stamp(args.end_exclusive),
               Settings(initial_eth=D(execution['initial_eth']),quote=quote,source=provider,fee=D(execution['fee_per_execution']),
                        publication_minutes=execution['publication_lag_minutes'],
                        processing_minutes=execution['processing_lag_minutes'],rules=rules,
                        friction_round_trip_bps=D(args.friction_bps if args.friction_bps is not None else execution['default_noncommission_round_trip_bps']),extra_delay_bars=args.extra_delay_bars),holdout_start_ms=cutoff)
    canonical=json.dumps(result,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    source_dirty=subprocess.run(['git','diff','--quiet','HEAD','--','src','scripts','tests','config'],cwd=ROOT).returncode!=0
    if source_dirty:
        raise RuntimeError('Commit source/configuration before recording a research result')
    envelope={'code_commit':commit,'dataset_sha256':dataset_hash,'result_sha256':hashlib.sha256(canonical).hexdigest(),
              'result':result}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(envelope,indent=2,allow_nan=False)+'\n')
    summary={k:v for k,v in envelope.items() if k!='result'}
    summary.update({k:v for k,v in result.items() if k not in ['curve','fills','decisions','rejections']})
    summary['full_ledger_committed']=False
    if args.summary:
        args.summary.parent.mkdir(parents=True,exist_ok=True)
        args.summary.write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:summary[k] for k in ['evidence_type','variant','quote','orders_executed','orders_rejected','result_sha256']},indent=2))


if __name__=='__main__':
    main()
