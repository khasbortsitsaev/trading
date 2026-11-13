#!/usr/bin/env python3
"""Fetch bounded development-only USD history, storing raw bodies outside Git."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from trading_research.data import collect_bitstamp


def stamp(day):
    return int(datetime.fromisoformat(day).replace(tzinfo=timezone.utc).timestamp()*1000)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--start',default='2020-01-01')
    p.add_argument('--end-exclusive',default='2025-11-13')
    args=p.parse_args()
    policy=json.loads((Path(__file__).resolve().parents[1]/'config/research-policy.json').read_text())
    cutoff=policy['split']['exact_utc_boundaries']['holdout_start_inclusive']
    result=collect_bitstamp(args.output_dir,stamp(args.start),stamp(args.end_exclusive),stamp(cutoff))
    print(json.dumps({'complete':result['complete'],'markets':{a:{k:v for k,v in q.items() if k!='missing_timestamps_ms'} for a,q in result['markets'].items()},'normalized_sha256':result['normalized_sha256']},indent=2))
