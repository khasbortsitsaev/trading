"""Mean-reversion state and complete synthetic portfolio checks."""
from dataclasses import replace
from decimal import Decimal as D
import json
from pathlib import Path
import unittest
from test_engine import BASE, bars
from trading_research.core import DataError
from trading_research.engine import DAY, Settings, run, signals

POLICY=json.loads((Path(__file__).resolve().parents[1]/'config/research-policy.json').read_text())
VARIANT=next(v for v in POLICY['variants'] if v['id']=='REVERSAL-20-1')


def signal(prices, old=False):
    return signals({'ETH':bars(prices)},VARIANT,{'ETH':old})['ETH']


def panel():
    candles=bars([100]*20+[50,55,60,150]+[100]*36)
    return {'ETH':candles,'BTC':list(candles)}


def simulate(data, start=20):
    return run(data,VARIANT,BASE+start*DAY,BASE+45*DAY,Settings(),holdout_start_ms=BASE+100*DAY)


class S3Fixtures(unittest.TestCase):
    def test_low_price_enters_high_price_exits(self):
        self.assertTrue(signal([100]*19+[50]))
        self.assertFalse(signal([100]*19+[150],True))

    def test_between_entry_and_mean_retains_old_state(self):
        prices=[100]*18+[80,98]
        self.assertFalse(signal(prices,False))
        self.assertTrue(signal(prices,True))

    def test_zero_variance_flattens_and_insufficient_warmup_fails_run(self):
        self.assertFalse(signal([100]*20,True))
        with self.assertRaises(DataError):
            simulate(panel(),19)

    def test_startup_ignores_prescored_signal_state(self):
        # Previous day was extreme, latest has z between -1 and 0.
        data={a:bars([100]*18+[50,95]+[100]*40) for a in ['ETH','BTC']}
        self.assertFalse(simulate(data)['decisions'][0]['active']['ETH'])

    def test_complete_pipeline_buys_then_exits_with_exact_daily_equity(self):
        data=panel();r=simulate(data)
        self.assertEqual([d['active']['ETH'] for d in r['decisions'][:5]],[False,True,True,True,False])
        self.assertTrue(any(f['asset']=='BTC' and f['side']=='buy' and f['source_close_ms']==BASE+21*DAY for f in r['fills']))
        self.assertTrue(any(f['asset']=='BTC' and f['side']=='sell' and f['source_close_ms']==BASE+24*DAY for f in r['fills']))
        for row in r['curve']:
            i=(row['time_ms']-BASE)//DAY-1
            self.assertEqual(D(row['equity']),D(row['cash'])+sum(D(q)*data[a][i].close for a,q in row['inventory'].items()))
            self.assertGreaterEqual(D(row['cash']),0)
            self.assertTrue(all(D(q)>=0 for q in row['inventory'].values()))
        self.assertEqual(r,simulate(data))

    def test_future_prices_cannot_change_earlier_decisions_or_fills(self):
        data=panel();changed={a:list(bs) for a,bs in data.items()}
        for bs in changed.values():
            for i in range(28,len(bs)):
                b=bs[i];bs[i]=replace(b,open=b.open*2,high=b.high*2,low=b.low*2,close=b.close*2)
        x,y=simulate(data),simulate(changed)
        self.assertEqual([d for d in x['decisions'] if d['source_close_ms']<=BASE+28*DAY], [d for d in y['decisions'] if d['source_close_ms']<=BASE+28*DAY])
        self.assertEqual([f for f in x['fills'] if f['source_close_ms']<=BASE+28*DAY], [f for f in y['fills'] if f['source_close_ms']<=BASE+28*DAY])
