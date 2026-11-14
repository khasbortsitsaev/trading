"""Hand-audited S2 signals and causal end-to-end synthetic ledger checks."""
from dataclasses import replace
from decimal import Decimal as D
import json
from pathlib import Path
import unittest
from test_engine import BASE, bars
from trading_research.core import DataError
from trading_research.engine import DAY, Settings, run, signals

SPEC = json.loads((Path(__file__).resolve().parents[1]/'config/research-policy.json').read_text())['poc']['s2_spec']
VARIANT = dict(SPEC, lookback_days=SPEC['trend_lookback_days'])


def history(last_price=120, last_volume=151, prior_volume=100):
    candles = bars([100]*20+[last_price])
    return [replace(b, volume=D(prior_volume)) for b in candles[:-1]] + [replace(candles[-1], volume=D(last_volume))]


def signal(candles, active=False):
    return signals({'ETH':candles}, VARIANT, {'ETH':active})['ETH']


def panel():
    prices = list(range(100,123)) + [80]*17
    candles = bars(prices)
    candles = [replace(b, volume=D(200 if i==20 else 100)) for i,b in enumerate(candles)]
    return {'ETH':candles, 'BTC':list(candles)}


def simulate(data, start=21):
    return run(data, VARIANT, BASE+start*DAY, BASE+35*DAY, Settings(), holdout_start_ms=BASE+100*DAY)


class S2Fixtures(unittest.TestCase):
    def test_strict_entry_boundaries_and_current_volume_excluded(self):
        self.assertTrue(signal(history(last_volume=151)))  # Including current bar would fail.
        self.assertFalse(signal(history(last_volume=150)))
        self.assertFalse(signal(history(last_price=100)))
        self.assertFalse(signal(history(last_price=99)))

    def test_low_volume_holds_until_nonpositive_trend(self):
        self.assertTrue(signal(history(last_volume=0), active=True))
        self.assertFalse(signal(history(last_volume=0)))
        self.assertFalse(signal(history(last_price=100), active=True))
        self.assertFalse(signal(history(last_price=99), active=True))

    def test_zero_mean_blocks_entry_but_not_existing_trend(self):
        self.assertFalse(signal(history(prior_volume=0)))
        self.assertTrue(signal(history(prior_volume=0), active=True))

    def test_invalid_volume_fails_instead_of_manufacturing_signal(self):
        for value in ['-1','NaN','Infinity']:
            with self.subTest(value=value), self.assertRaises(DataError):
                signal(history(last_volume=value))

    def test_insufficient_warmup_and_different_windows(self):
        with self.assertRaises(DataError):
            signal(history()[:-1])
        changed = dict(VARIANT, volume_lookback_days=25)
        with self.assertRaises(DataError):
            run(panel(), changed, BASE+21*DAY, BASE+35*DAY, Settings(), holdout_start_ms=BASE+100*DAY)
        with self.assertRaises(DataError):
            simulate(panel(), start=20)

    def test_full_pipeline_entry_hold_exit_and_reconciled_equity(self):
        data=panel(); result=simulate(data)
        states=[d['active']['ETH'] for d in result['decisions']]
        self.assertEqual(states[:4], [True,True,True,False])
        self.assertTrue(any(f['asset']=='BTC' and f['side']=='buy' for f in result['fills']))
        self.assertTrue(any(f['asset']=='BTC' and f['side']=='sell' and f['source_close_ms']==BASE+24*DAY for f in result['fills']))
        for row in result['curve']:
            day=(row['time_ms']-BASE)//DAY-1
            equity=D(row['cash'])+sum(D(q)*data[a][day].close for a,q in row['inventory'].items())
            self.assertEqual(equity,D(row['equity']))
            self.assertGreaterEqual(D(row['cash']),0)
            self.assertTrue(all(D(q)>=0 for q in row['inventory'].values()))
        self.assertEqual(result, simulate(data))

    def test_startup_does_not_inherit_prescored_volume_entry(self):
        result=simulate(panel(), start=22)  # Spike occurred before first scored decision.
        self.assertFalse(result['decisions'][0]['active']['ETH'])
        self.assertFalse(any(f['side']=='buy' for f in result['fills']))

    def test_future_close_and_volume_do_not_change_earlier_decisions_or_fills(self):
        data=panel(); changed={a:list(bs) for a,bs in data.items()}
        for a,bs in changed.items():
            for i in range(27,len(bs)):
                b=bs[i];bs[i]=replace(b,open=b.open*2,close=b.close*2,high=b.high*2,low=b.low*2,volume=b.volume*100)
        first=simulate(data); second=simulate(changed)
        self.assertEqual([d for d in first['decisions'] if d['source_close_ms']<BASE+28*DAY],
                         [d for d in second['decisions'] if d['source_close_ms']<BASE+28*DAY])
        self.assertEqual([f for f in first['fills'] if f['source_close_ms']<BASE+28*DAY],
                         [f for f in second['fills'] if f['source_close_ms']<BASE+28*DAY])
