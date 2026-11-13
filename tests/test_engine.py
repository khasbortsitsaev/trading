"""Small independent fixtures for the complete offline signal-to-ledger path."""
from dataclasses import replace
from datetime import datetime,timezone
from decimal import Decimal as D
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from trading_research.core import Candle,DataError,HoldoutAccessError,Portfolio,Rules
from trading_research.engine import DAY,Settings,run,signals,target_quantities
from trading_research.data import bitstamp_rows,load_panel,collect_bitstamp,load_admitted_dataset
from unittest.mock import patch
import hashlib,json,tempfile

BASE=int(datetime(2020,1,1,tzinfo=timezone.utc).timestamp()*1000)
CUTOFF=BASE+1000*DAY
TREND={'id':'SYNTHETIC-TREND-1','family':'trend','lookback_days':1}


def bars(prices,opens=None):
    return [Candle(BASE+i*DAY,D(str((opens or prices)[i])),
                   max(D(str(p)),D(str((opens or prices)[i])))*D('1.01'),
                   min(D(str(p)),D(str((opens or prices)[i])))*D('.99'),D(str(p)),D(100))
            for i,p in enumerate(prices)]


def fixture(prices=None):
    return {a:bars(prices or [100]*12) for a in ['ETH','BTC']}


def simulate(panel,settings=None,variant=None):
    return run(panel,variant or TREND,BASE+2*DAY,BASE+10*DAY,
               settings or Settings(fee=D('.01'),friction_round_trip_bps=D(0)),holdout_start_ms=CUTOFF)


class EngineFixtures(unittest.TestCase):
    def test_constant_flat_signal_sells_initial_eth_once_and_matches_cash(self):
        result=simulate(fixture())
        self.assertEqual(result['orders_executed'],1)
        self.assertEqual(D(result['curve'][-1]['equity']),D('49.5'))
        self.assertEqual(D(result['curve'][-1]['cash_benchmark']),D('49.5'))
        self.assertEqual(D(result['curve'][-1]['eth_benchmark']),D(50))
        self.assertEqual(D(result['commission_quote']),D('.5'))

    def test_zero_cost_flat_account_reconciles(self):
        result=simulate(fixture(),Settings(fee=D(0),friction_round_trip_bps=D(0)))
        self.assertEqual(result['metrics']['total_return'],0)
        self.assertEqual(result['metrics']['maximum_drawdown'],0)
        self.assertEqual(D(result['curve'][-1]['equity']),D(50))

    def test_causal_fills_and_multiple_positions(self):
        result=simulate(fixture(list(range(100,112))))
        self.assertTrue(result['fills'])
        self.assertTrue(any(D(x['inventory'].get('BTC','0'))>0 and D(x['inventory']['ETH'])>0 for x in result['curve']))
        for fill in result['fills']:
            available=datetime.fromisoformat(fill['available_at'])
            ready=datetime.fromisoformat(fill['ready_at'])
            at=datetime.fromisoformat(fill['fill_at'])
            self.assertLess(available,ready)
            self.assertLess(ready,at)
            self.assertLessEqual(fill['source_close_ms'],int(available.timestamp()*1000))
        self.assertTrue(all(D(x['cash'])>=0 and all(D(q)>=0 for q in x['inventory'].values()) for x in result['curve']))

    def test_future_price_changes_do_not_change_prior_decisions_or_fills(self):
        original=fixture(list(range(100,112)))
        changed={a:list(bs) for a,bs in original.items()}
        for a,bs in changed.items():
            for i in range(7,len(bs)):
                b=bs[i];bs[i]=replace(b,open=b.open*2,high=b.high*2,low=b.low*2,close=b.close*2)
        a,b=simulate(original),simulate(changed)
        self.assertEqual([x for x in a['decisions'] if x['source_close_ms']<BASE+7*DAY],
                         [x for x in b['decisions'] if x['source_close_ms']<BASE+7*DAY])
        self.assertEqual([x for x in a['fills'] if datetime.fromisoformat(x['fill_at']).timestamp()*1000<BASE+7*DAY],
                         [x for x in b['fills'] if datetime.fromisoformat(x['fill_at']).timestamp()*1000<BASE+7*DAY])

    def test_extra_delay_runs_and_moves_first_fill(self):
        panel=fixture(list(range(100,112)))
        a=simulate(panel)
        b=simulate(panel,Settings(fee=D('.01'),friction_round_trip_bps=D(0),extra_delay_bars=1))
        first_a=datetime.fromisoformat(a['fills'][0]['fill_at'])
        first_b=datetime.fromisoformat(b['fills'][0]['fill_at'])
        self.assertEqual((first_b-first_a).days,1)
        self.assertEqual(b['pending_intents_not_filled_at_end'],2)

    def test_gap_and_holdout_rejected_before_scoring(self):
        panel=fixture();panel['BTC'].pop(5)
        with self.assertRaises(DataError):simulate(panel)
        panel=fixture();panel['ETH'].append(replace(panel['ETH'][-1],timestamp_ms=CUTOFF))
        with self.assertRaises(HoldoutAccessError):simulate(panel)

    def test_large_gap_resizes_orders_without_negative_cash(self):
        prices=list(range(100,112));panel=fixture(prices)
        panel['BTC']=bars(prices,opens=[100,101,102]+[150]*9)
        result=simulate(panel)
        self.assertTrue(any(x['cash_resized'] for x in result['fills']))
        self.assertTrue(all(D(x['cash'])>=0 for x in result['curve']))

    def test_suspension_rejects_designated_orders_without_hidden_fills(self):
        panel=fixture(list(range(100,112)))
        result=run(panel,TREND,BASE+2*DAY,BASE+10*DAY,Settings(),holdout_start_ms=CUTOFF,
                   market_status={t:{'BTC':False,'ETH':True} for t in range(BASE+2*DAY,BASE+10*DAY,DAY)})
        self.assertFalse(any(x['asset']=='BTC' for x in result['fills']))
        self.assertTrue(any(x['reason']=='market_unavailable' for x in result['rejections']))

    def test_minimum_order_keeps_residual_cash(self):
        settings=Settings(rules={a:Rules(minimum_quote=D(1000)) for a in ['BTC','ETH']})
        result=simulate(fixture(list(range(100,112))),settings)
        self.assertEqual(result['orders_executed'],0)
        self.assertGreater(result['orders_rejected'],0)
        self.assertEqual(D(result['curve'][-1]['inventory']['ETH']),D('.5'))

    def test_reversal_zero_variance_and_state(self):
        variant={'family':'reversal','lookback_days':3,'entry_z':1}
        self.assertEqual(signals({'ETH':bars([100,100,100])},variant,{'ETH':True}),{'ETH':False})
        self.assertEqual(signals({'ETH':bars([100,100,50])},variant,{}),{'ETH':True})
        self.assertEqual(signals({'ETH':bars([50,50,100])},variant,{'ETH':True}),{'ETH':False})

    def test_deterministic_result_and_no_usd_usdc_identity_claim(self):
        panel=fixture(list(range(100,112)))
        self.assertEqual(simulate(panel),simulate(panel))
        result=simulate(panel,Settings(quote='USD',source='external USD proxy'))
        self.assertFalse(result['usdc_wealth_claimed'])
        self.assertEqual(result['evidence_type'],'historical_source_proxy_not_venue_replication')

    def test_equal_weight_more_than_two_assets_and_decimal_remainder(self):
        prices={a:D(100) for a in ['ETH','BTC','A','B','C','D']}
        targets=target_quantities(Portfolio('600'),prices,{a:True for a in prices},Settings())
        self.assertEqual(len(targets),6)
        self.assertTrue(all(q>0 for q in targets.values()))


class SourceFixtures(unittest.TestCase):
    def test_public_api_schema_and_pair_identity(self):
        payload={'data':{'pair':'BTC/USD','ohlc':[{'timestamp':'1577836800','open':'1','high':'3','low':'.5','close':'2','volume':'4'}]}}
        self.assertEqual(bitstamp_rows(payload,'btcusd')[0],[BASE,'1','3','.5','2','4'])
        with self.assertRaises(DataError):bitstamp_rows(payload,'ethusd')
        with self.assertRaises(DataError):bitstamp_rows({'error':'bad request'},'btcusd')

    def test_collector_rejects_holdout_before_any_network_request(self):
        with tempfile.TemporaryDirectory() as tmp, patch('trading_research.data.urlopen') as network:
            with self.assertRaises(HoldoutAccessError):
                collect_bitstamp(Path(tmp)/'raw',BASE,CUTOFF+DAY,CUTOFF)
            network.assert_not_called()

    def test_collector_keeps_raw_data_outside_public_checkout(self):
        root=Path(__file__).resolve().parents[1]
        with patch('trading_research.data.urlopen') as network:
            with self.assertRaises(ValueError):
                collect_bitstamp(root/'not-created-market-data',BASE,BASE+DAY,CUTOFF)
            network.assert_not_called()
        self.assertFalse((root/'not-created-market-data').exists())

    def test_hash_and_gap_validation_on_saved_inputs(self):
        data={'ETH':[[BASE,'1','3','.5','2','4'],[BASE+2*DAY,'1','3','.5','2','4']]}
        body=json.dumps(data).encode()
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'data.json';p.write_bytes(body)
            with self.assertRaises(DataError):load_panel(p,'incorrect',CUTOFF)
            with self.assertRaises(DataError):load_panel(p,hashlib.sha256(body).hexdigest(),CUTOFF)
            valid={'ETH':[[BASE,'1','3','.5','2','4']]}
            normalized=json.dumps(valid).encode();(Path(tmp)/'normalized.json').write_bytes(normalized)
            digest=hashlib.sha256(normalized).hexdigest()
            manifest={'provider':'Bitstamp public OHLC API','quote':'USD','complete':True,'normalized_sha256':digest}
            original=json.dumps(manifest).encode();mp=Path(tmp)/'manifest.json';mp.write_bytes(original)
            admission={'source':manifest['provider'],'quote':'USD','normalized_sha256':digest,'manifest_sha256':hashlib.sha256(original).hexdigest()}
            _,actual=load_admitted_dataset(tmp,admission,CUTOFF)
            self.assertEqual(actual['quote'],'USD')
            mp.write_text(json.dumps(manifest|{'quote':'USDC'}))
            with self.assertRaises(DataError):load_admitted_dataset(tmp,admission,CUTOFF)
            mp.write_bytes(original)
            with self.assertRaises(DataError):load_admitted_dataset(tmp,admission|{'quote':'USDC'},CUTOFF)



if __name__=='__main__':unittest.main()
