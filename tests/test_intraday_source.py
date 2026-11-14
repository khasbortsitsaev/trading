"""Collector/admission/data QA regressions with no market-data requests."""
from dataclasses import replace
from decimal import Decimal as D
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import parse_qs,urlsplit

from test_engine import BASE,CUTOFF,bars
from trading_research.core import DataError,HoldoutAccessError
from trading_research.data import collect_bitstamp,load_admitted_dataset,DAY

spec=importlib.util.spec_from_file_location('execution_audit',Path(__file__).resolve().parents[1]/'scripts/audit_execution_data.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
INTERVAL=900000


class Response:
    status=200
    def __init__(self,request,timeout=30):
        url=urlsplit(request.full_url);query=parse_qs(url.query)
        step=int(query['step'][0]);count=int(query['limit'][0]);end=int(query['end'][0])
        last=(end//step)*step
        rows=[{'timestamp':str(t),'open':'100','high':'100','low':'100','close':'100',
               'volume':'96' if step==86400 else '1'} for t in range(last-(count-1)*step,last+1,step)]
        self.body=json.dumps({'data':{'pair':url.path.split('/')[-2],'ohlc':rows}}).encode()
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self,limit):return self.body


def capture(root,step=900,periods=96):
    with patch('trading_research.data.urlopen',side_effect=Response) as network:
        manifest=collect_bitstamp(root,BASE,BASE+periods*step*1000,CUTOFF,step)
    return manifest,network


def admission(root):
    raw=(root/'manifest.json').read_bytes();m=json.loads(raw)
    return {'source':m['provider'],'quote':m['quote'],'manifest_sha256':hashlib.sha256(raw).hexdigest(),
            'normalized_sha256':m['normalized_sha256'],'start_ms':m['start_ms'],
            'end_exclusive_ms':m['end_exclusive_ms'],'interval_ms':m['interval_ms'],'markets':['BTC','ETH']}


class IntradayCollector(unittest.TestCase):
    def test_pages_follow_interval_limits_and_resume_without_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);manifest,network=capture(root,periods=1001)
            self.assertEqual(network.call_count,4)
            self.assertEqual([r['returned_rows'] for r in manifest['requests']],[1000,1,1000,1])
            self.assertEqual(manifest['interval_ms'],INTERVAL)
            self.assertTrue(manifest['complete'])
            for asset in ['BTC','ETH']:
                self.assertEqual(manifest['markets'][asset]['observations'],1001)
            with patch('trading_research.data.urlopen') as network:
                again=collect_bitstamp(root,BASE,BASE+1001*INTERVAL,CUTOFF,900)
                network.assert_not_called()
            self.assertEqual(again,manifest)

    def test_cache_tampering_and_interval_reuse_fail_before_network(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);capture(root)
            (root/'btcusd-1.json').write_text('{}')
            with patch('trading_research.data.urlopen') as network:
                with self.assertRaisesRegex(DataError,'Cached'):collect_bitstamp(root,BASE,BASE+DAY,CUTOFF,900)
                network.assert_not_called()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);capture(root)
            with patch('trading_research.data.urlopen') as network:
                with self.assertRaises(DataError):collect_bitstamp(root,BASE,BASE+DAY,CUTOFF,86400)
                network.assert_not_called()

    def test_partial_cache_does_not_become_an_unverified_capture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'btcusd-1.json').write_text('{}')
            with patch('trading_research.data.urlopen') as network:
                with self.assertRaisesRegex(DataError,'Incomplete cached'):collect_bitstamp(root,BASE,BASE+DAY,CUTOFF,900)
                network.assert_not_called()

    def test_holdout_unsupported_step_and_misaligned_request_do_not_use_network(self):
        with tempfile.TemporaryDirectory() as tmp,patch('trading_research.data.urlopen') as network:
            for start,end,step in [(BASE,CUTOFF+INTERVAL,900),(BASE,BASE+DAY,60),(BASE+1,BASE+DAY,900)]:
                with self.subTest(start=start,end=end,step=step),self.assertRaises(ValueError):
                    collect_bitstamp(Path(tmp)/'raw',start,end,CUTOFF,step)
            network.assert_not_called()

    def test_response_at_holdout_is_rejected_without_creating_a_data_page(self):
        class BadResponse(Response):
            def __init__(self,request,timeout=30):
                super().__init__(request);data=json.loads(self.body)
                data['data']['ohlc'][0]['timestamp']=str(CUTOFF//1000)
                self.body=json.dumps(data).encode()
        with tempfile.TemporaryDirectory() as tmp,patch('trading_research.data.urlopen',side_effect=BadResponse):
            root=Path(tmp)
            with self.assertRaises(HoldoutAccessError):collect_bitstamp(root,BASE,BASE+DAY,CUTOFF,900)
            self.assertFalse((root/'normalized.json').exists())
            self.assertFalse((root/'btcusd-1.json').exists())


class SourceAdmission(unittest.TestCase):
    def test_raw_reconstruction_and_exact_decimal_aggregation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);capture(root/'daily',86400,1);capture(root/'intraday')
            plan={'source':'Bitstamp public OHLC API','quote':'USD','markets':['BTC','ETH'],
                  'start_ms':BASE,'end_exclusive_ms':BASE+DAY}
            daily,_,_=audit.audit_capture(root/'daily',plan,DAY,CUTOFF)
            intraday,_,_=audit.audit_capture(root/'intraday',plan,INTERVAL,CUTOFF)
            comparisons=audit.compare_intervals(daily,intraday,D('.000001'),D('.00000001'))
            self.assertTrue(all(r['daily_ohlc_mismatch_count']==r['intraday_bound_violations']==r['volume_tolerance_failures']==0
                                for r in comparisons.values()))
            (root/'intraday/btcusd-1.json').write_text('{}')
            with self.assertRaisesRegex(DataError,'hash mismatch'):
                audit.audit_capture(root/'intraday',plan,INTERVAL,CUTOFF)

    def test_declared_edge_coverage_cannot_be_shortened_even_with_consistent_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);capture(root)
            path=root/'normalized.json';panel=json.loads(path.read_text());panel['ETH'].pop(0)
            body=json.dumps(panel).encode();path.write_bytes(body)
            manifest=json.loads((root/'manifest.json').read_text());manifest['normalized_sha256']=hashlib.sha256(body).hexdigest()
            (root/'manifest.json').write_text(json.dumps(manifest))
            with self.assertRaisesRegex(DataError,'full declared window'):
                load_admitted_dataset(root,admission(root),CUTOFF,INTERVAL)

    def test_admitted_universe_and_interval_are_binding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);capture(root);a=admission(root)
            for changed in [dict(a,markets=['ETH']),dict(a,interval_ms=DAY),dict(a,start_ms=BASE+DAY)]:
                with self.subTest(changed=changed),self.assertRaises(DataError):
                    load_admitted_dataset(root,changed,CUTOFF,INTERVAL)

    def test_price_volume_and_missing_bar_failures_are_separate(self):
        daily={'ETH':[replace(bars([100])[0],high=D(100),low=D(100),volume=D(96))]}
        intraday={'ETH':[replace(daily['ETH'][0],timestamp_ms=BASE+i*INTERVAL,volume=D(1)) for i in range(96)]}
        intraday['ETH'][0]=replace(intraday['ETH'][0],high=D(110),volume=D(2))
        result=audit.compare_intervals(daily,intraday,D('.000001'),D('.00000001'))['ETH']
        self.assertEqual(result['daily_ohlc_mismatch_count'],1)
        self.assertEqual(result['intraday_bound_violations'],1)
        self.assertEqual(result['volume_tolerance_failures'],1)
        intraday['ETH'].pop()
        with self.assertRaisesRegex(DataError,'Missing or duplicate'):
            audit.compare_intervals(daily,intraday,D('.000001'),D('.00000001'))
