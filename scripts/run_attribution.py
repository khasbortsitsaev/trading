#!/usr/bin/env python3
"""Registered composition diagnostic and fixed execution stresses; no signal tuning."""
import argparse
from dataclasses import replace
from datetime import timedelta
from decimal import Decimal as D
import hashlib,json,statistics,subprocess
from pathlib import Path
from run_research import ROOT,stamp,run,Settings,Rules,load_admitted_dataset
from trading_research.core import Portfolio
from trading_research.engine import DAY,dt,execute_targets,quantity_floor,metrics


def mean_weights(result, prices):
    sums={a:D(0) for a in prices}
    for point in result['curve']:
        t=point['time_ms']-DAY
        for a in sums:
            sums[a]+=D(point['inventory'].get(a,'0'))*prices[a][t]/D(point['equity'])
    return {a:value/len(result['curve']) for a,value in sums.items()}


def passive(panel, start, end, settings, weights):
    if any(w<0 for w in weights.values()) or sum(weights.values())>1+D('1e-24'):
        raise ValueError('Invalid passive weights')
    indexed={a:{b.timestamp_ms:b for b in bs} for a,bs in panel.items()}
    refs={a:bs[start-DAY].close for a,bs in indexed.items()}
    portfolio=Portfolio(inventory={'ETH':settings.initial_eth})
    initial=settings.initial_eth*indexed['ETH'][start].open
    equity=portfolio.equity(refs);slip=settings.friction_round_trip_bps/D(20000)
    quantities={a:quantity_floor(equity*weights[a]/(refs[a]*(1+slip)*(1+settings.fee)),settings.rules.get(a,Rules())) for a in refs}
    available=dt(start)+timedelta(minutes=settings.publication_minutes)
    target={'quantities':quantities,'source_close_ms':start,'available_at':available,'decision_at':available,'ready_at':available+timedelta(minutes=settings.processing_minutes)}
    curve=[];rejected=[]
    for t in range(start,end,DAY):
        if t==start+DAY:
            execute_targets(portfolio,target,{a:bs[t].open for a,bs in indexed.items()},t,settings,rejected)
        closes={a:bs[t].close for a,bs in indexed.items()}
        curve.append({'time_ms':t+DAY,'equity':str(portfolio.equity(closes)),'cash':str(portfolio.cash),'inventory':{a:str(q) for a,q in portfolio.inventory.items()}})
    return {'metrics':metrics([D(x['equity']) for x in curve],initial,(end-start)/DAY),'curve':curve,'fills':portfolio.events,'rejections':rejected,'weights':{a:str(w) for a,w in weights.items()}}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data-dir',type=Path,required=True);p.add_argument('--baseline-dir',type=Path,required=True);p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args()
    if args.output_dir.resolve()==ROOT or ROOT in args.output_dir.resolve().parents:p.error('Private ledgers must be outside checkout')
    if subprocess.run(['git','diff','--quiet','HEAD','--','src','scripts','tests','config'],cwd=ROOT).returncode:raise RuntimeError('Commit code/config first')
    policy=json.loads((ROOT/'config/research-policy.json').read_text());cfg=policy['attribution_analysis'];execution=json.loads((ROOT/'config/runner.json').read_text())
    cutoff=stamp(policy['split']['exact_utc_boundaries']['holdout_start_inclusive'])
    panel,manifest=load_admitted_dataset(args.data_dir,policy['dataset_admission'],cutoff)
    prices={a:{b.timestamp_ms:b.close for b in bs} for a,bs in panel.items()}
    opens={b.timestamp_ms:b.open for b in panel['ETH']}
    rules={a:Rules(quantity_decimals=x['quantity_decimals'],tick=D(x['tick']),minimum_base=D(x['minimum_base']),minimum_quote=D(x['minimum_quote'])) for a,x in execution['markets'].items()}
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();args.output_dir.mkdir(parents=True,exist_ok=True)
    for family in ['S1','S2','S3']:
        baseline=json.loads((ROOT/f'research/artifacts/{family}/{family.lower()}-002-rolling.json').read_text());rows=[]
        for row in baseline['windows']:
            start,end=stamp(row['start']),stamp(row['end_exclusive']);assert end<=cutoff
            body=(args.baseline_dir/f'{family}-{row["start"]}.json').read_bytes();assert hashlib.sha256(body).hexdigest()==row['result_sha256'];old=json.loads(body)
            settings=Settings(initial_eth=D('1000')/opens[start],quote=manifest['quote'],source=manifest['provider'],fee=D(execution['fee_per_execution']),friction_round_trip_bps=D(execution['default_noncommission_round_trip_bps']),publication_minutes=execution['publication_lag_minutes'],processing_minutes=execution['processing_lag_minutes'],rules=rules)
            weights=mean_weights(old,prices);control=passive(panel,start,end,settings,weights)
            record={'start':row['start'],'baseline_return':row['strategy_return'],'control_return':control['metrics']['total_return'],'control_drawdown':control['metrics']['maximum_drawdown'],'target_weights_hindsight':control['weights'],'control_realized_mean_weights':{a:str(w) for a,w in mean_weights(control,prices).items()},'scenarios':{}}
            controlbody=json.dumps(control,sort_keys=True,separators=(',',':')).encode();(args.output_dir/f'{family}-{row["start"]}-control.json').write_bytes(controlbody);record['control_sha256']=hashlib.sha256(controlbody).hexdigest()
            for scenario,changes in [('friction30',{'friction_round_trip_bps':D(30)}),('friction50',{'friction_round_trip_bps':D(50)}),('extra_day',{'extra_delay_bars':1})]:
                result=run(panel,baseline['variant'],start,end,replace(settings,**changes),holdout_start_ms=cutoff)
                raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode();(args.output_dir/f'{family}-{row["start"]}-{scenario}.json').write_bytes(raw)
                record['scenarios'][scenario]={**result['metrics'],'result_sha256':hashlib.sha256(raw).hexdigest()}
            rows.append(record)
        summary={'windows':len(rows),'beat_hindsight_control':sum(x['baseline_return']>x['control_return'] for x in rows),'median_paired_excess_vs_control':statistics.median(x['baseline_return']-x['control_return'] for x in rows),'median_control_return':statistics.median(x['control_return'] for x in rows)}
        for scenario in ['friction30','friction50','extra_day']:
            summary[scenario]={'profitable_windows':sum(x['scenarios'][scenario]['total_return']>0 for x in rows),'median_return':statistics.median(x['scenarios'][scenario]['total_return'] for x in rows),'worst_return':min(x['scenarios'][scenario]['total_return'] for x in rows),'worst_drawdown':max(x['scenarios'][scenario]['maximum_drawdown'] for x in rows)}
        output={'experiment_id':f'{family}-003','evidence_type':'post_hoc_development_diagnostic_not_causal_alpha_or_independent_validation','code_commit':commit,'dataset_sha256':manifest['normalized_sha256'],'design':cfg,'summary':summary,'windows':rows,'holdout_access':False,'overlapping_windows_independent':False}
        (ROOT/f'research/artifacts/{family}/{family.lower()}-003-attribution.json').write_text(json.dumps(output,indent=2)+'\n');print(family,json.dumps(summary))


if __name__=='__main__':main()
