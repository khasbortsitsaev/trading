import sys
from pathlib import Path
import unittest
from decimal import Decimal as D
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_attribution import mean_weights,passive,Settings
from test_engine import fixture,BASE
from trading_research.engine import DAY


class AttributionFixtures(unittest.TestCase):
    def test_weights_use_each_assets_marked_inventory(self):
        result={'curve':[{'time_ms':DAY,'equity':'100','inventory':{'ETH':'1'}},{'time_ms':2*DAY,'equity':'200','inventory':{'ETH':'1','BTC':'1'}}]}
        self.assertEqual(mean_weights(result,{'ETH':{0:D(50),DAY:D(100)},'BTC':{0:D(100),DAY:D(50)}}),{'ETH':D('.5'),'BTC':D('.125')})

    def test_hold_eth_control_constant_prices_and_no_churn(self):
        result=passive(fixture(),BASE+2*DAY,BASE+10*DAY,Settings(fee=D(0),friction_round_trip_bps=D(0)),{'ETH':D(1),'BTC':D(0)})
        self.assertEqual(result['metrics']['total_return'],0)
        self.assertEqual(result['fills'],[])

    def test_cash_control_charges_one_owned_eth_sale(self):
        result=passive(fixture(),BASE+2*DAY,BASE+10*DAY,Settings(fee=D('.01'),friction_round_trip_bps=D(0)),{'ETH':D(0),'BTC':D(0)})
        self.assertEqual(len(result['fills']),1)
        self.assertEqual(D(result['curve'][-1]['equity']),D('49.5'))
        with self.assertRaises(ValueError):passive(fixture(),BASE+2*DAY,BASE+10*DAY,Settings(),{'ETH':D('1.1'),'BTC':D(0)})

    def test_fixed_weights_hold_quantities_without_future_information(self):
        from dataclasses import replace
        from test_engine import bars
        prices=list(range(100,112))
        data={a:bars(prices) for a in ['ETH','BTC']}
        changed={a:list(bs) for a,bs in data.items()}
        for bs in changed.values():
            for i in range(6,len(bs)):
                b=bs[i];bs[i]=replace(b,open=b.open*2,high=b.high*2,low=b.low*2,close=b.close*2)
        weights={'ETH':D('.25'),'BTC':D('.25')}
        first=passive(data,BASE+2*DAY,BASE+10*DAY,Settings(),weights)
        second=passive(changed,BASE+2*DAY,BASE+10*DAY,Settings(),weights)
        self.assertEqual(first['fills'],second['fills'])
        self.assertEqual(first['curve'][:4],second['curve'][:4])
        self.assertEqual(len({tuple(sorted(p['inventory'].items())) for p in first['curve'][1:]}),1)
        self.assertEqual(len({f['fill_at'] for f in first['fills']}),1)
