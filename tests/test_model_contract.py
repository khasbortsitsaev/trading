"""Independent regressions for the quant review, never profitability evidence."""
from dataclasses import replace
from decimal import Decimal as D
import json
import math
from pathlib import Path
import unittest

from test_engine import BASE, CUTOFF, TREND, bars, fixture, simulate
from trading_research.core import DataError, HoldoutAccessError, Rules
from trading_research.engine import DAY, Settings, run, signals, validate_variant
from trading_research.risk import equity_envelope, drawdown_upper_bound


def wide_panel():
    return {a:[replace(b,high=D(200),low=D(50)) for b in bs]
            for a,bs in fixture(list(range(100,112))).items()}


def execution_bars(panel, minute=15):
    return {a:[replace(b,timestamp_ms=b.timestamp_ms+minute*60000,
                       open=D(110),high=D(110),low=D(110),close=D(110))
               for b in bs[2:10]] for a,bs in panel.items()}


def intraday(panel, execution=None, **settings):
    return run(panel,TREND,BASE+2*DAY,BASE+10*DAY,
               Settings(execution_interval_minutes=15,execution_source='synthetic_15m',**settings),
               holdout_start_ms=CUTOFF,execution_panel=execution if execution is not None else execution_bars(panel))


class ParameterValidity(unittest.TestCase):
    def test_unreachable_entry_fails_even_before_history_is_available(self):
        variant={'family':'reversal','lookback_days':5,'entry_z':2}
        for prices in [[],[100,100,100,100,.01]]:
            with self.assertRaisesRegex(ValueError,'Unreachable'):
                signals({'ETH':bars(prices)},variant,{})
        with self.assertRaises(ValueError):
            run(fixture(),variant,BASE+5*DAY,BASE+10*DAY,Settings(),holdout_start_ms=CUTOFF)

    def test_valid_collapse_still_enters_and_bad_thresholds_fail(self):
        variant={'family':'reversal','lookback_days':5,'entry_z':1}
        self.assertTrue(signals({'ETH':bars([100]*4+[.01])},variant,{})['ETH'])
        for value in [0,-1,float('nan'),float('inf'),2]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_variant(dict(variant,entry_z=value))
        validate_variant(dict(variant,entry_z=4/math.sqrt(5)))

    def test_registry_quarantines_without_substitution_or_trial_erasure(self):
        policy=json.loads((Path(__file__).resolve().parents[1]/'config/research-policy.json').read_text())
        for variant in policy['variants']:
            if variant['id']=='REVERSAL-5-2':
                self.assertFalse(variant['enabled'])
                with self.assertRaises(ValueError):validate_variant(variant)
            else:
                validate_variant(variant)
                self.assertNotIn('REVERSAL-5-2',variant['neighbor_ids'])
        self.assertEqual(policy['poc']['historical_trials_used'],3)
        self.assertEqual(policy['evidence_status']['additional_scenario_control_evaluations'],846)
        self.assertEqual(policy['budget']['selection_variants_total'],18)


class ExecutionContract(unittest.TestCase):
    def test_zero_volume_reference_cannot_manufacture_an_intraday_trade(self):
        p=wide_panel();e={a:[replace(b,volume=D(0)) for b in bs] for a,bs in execution_bars(p).items()}
        r=intraday(p,e)
        self.assertEqual(r['fills'],[])
        self.assertTrue(any(x['reason']=='zero_volume_execution_bar' for x in r['rejections']))
        self.assertEqual(D(r['curve'][-1]['inventory']['ETH']),D('.5'))

    def test_ten_minute_readiness_uses_actual_fifteen_minute_reference(self):
        r=intraday(wide_panel(),fee=D(0),friction_round_trip_bps=D(0))
        first=r['fills'][0]
        self.assertTrue(first['fill_at'].endswith('00:15:00+00:00'))
        self.assertEqual(first['signal_close_to_fill_seconds'],900)
        self.assertEqual(first['reference_price'],'110')
        self.assertNotEqual(first['reference_price'],str(wide_panel()['ETH'][2].open))
        self.assertEqual(r['settings']['execution_source'],'synthetic_15m')

    def test_grid_boundary_is_strictly_after_ready(self):
        p=wide_panel()
        r=intraday(p,execution_bars(p,minute=30),publication_minutes=5,processing_minutes=10)
        self.assertTrue(r['fills'][0]['fill_at'].endswith('00:30:00+00:00'))

    def test_missing_designated_bar_never_substitutes_later_or_daily_open(self):
        p=wide_panel();execution=execution_bars(p)
        execution['BTC'][0]=replace(execution['BTC'][0],timestamp_ms=BASE+2*DAY+30*60000)
        r=intraday(p,execution)
        self.assertTrue(any(x['asset']=='BTC' and x['at_ms']==BASE+2*DAY+15*60000
                            and x['reason']=='missing_designated_execution_bar' for x in r['rejections']))
        self.assertFalse(any(x['asset']=='BTC' and x['source_close_ms']==BASE+2*DAY for x in r['fills']))

    def test_no_intraday_prices_duplicates_misalignment_and_holdout_fail(self):
        p=wide_panel()
        with self.assertRaises(DataError):
            run(p,TREND,BASE+2*DAY,BASE+10*DAY,
                Settings(execution_interval_minutes=15,execution_source='fixture'),holdout_start_ms=CUTOFF)
        for mode in ['duplicate','misaligned','holdout','outside_daily_range']:
            e=execution_bars(p)
            if mode=='duplicate':e['ETH'].append(e['ETH'][0])
            if mode=='misaligned':e['ETH'][0]=replace(e['ETH'][0],timestamp_ms=BASE+2*DAY+1)
            if mode=='holdout':e['ETH'][0]=replace(e['ETH'][0],timestamp_ms=CUTOFF)
            if mode=='outside_daily_range':e['ETH'][0]=replace(e['ETH'][0],high=D(201))
            with self.subTest(mode=mode), self.assertRaises(DataError):intraday(p,e)

    def test_extra_delay_remains_one_day_and_pending_orders_keep_chronology(self):
        p=wide_panel()
        a=intraday(p);b=intraday(p,extra_delay_bars=1)
        self.assertEqual(a['fills'][0]['signal_close_to_fill_seconds'],900)
        self.assertEqual(b['fills'][0]['signal_close_to_fill_seconds'],86400+900)
        self.assertEqual(b['pending_intents_not_filled_at_end'],1)
        self.assertEqual([f['fill_at'] for f in b['fills']],sorted(f['fill_at'] for f in b['fills']))

    def test_execution_price_perturbation_cannot_change_decision_or_prior_fills(self):
        p=wide_panel();e=execution_bars(p)
        changed={a:[replace(b,open=D(150),close=D(150),high=D(150),low=D(150))
                    if b.timestamp_ms>=BASE+6*DAY else b for b in bs] for a,bs in e.items()}
        a=intraday(p,e);b=intraday(p,changed)
        self.assertEqual(a['decisions'][:5],b['decisions'][:5])
        self.assertEqual([f for f in a['fills'] if f['source_close_ms']<BASE+6*DAY],
                         [f for f in b['fills'] if f['source_close_ms']<BASE+6*DAY])

    def test_legacy_daily_latency_and_balances_are_unchanged(self):
        r=simulate(fixture())
        self.assertEqual(r['fills'][0]['signal_close_to_fill_seconds'],86400)
        self.assertEqual(D(r['curve'][-1]['equity']),D('49.5'))
        self.assertEqual(r['settings']['execution_interval_minutes'],1440)


class RiskContract(unittest.TestCase):
    def test_unsynchronized_asset_extrema_are_a_bound_not_a_portfolio_path(self):
        candles={'ETH':replace(bars([100])[0],low=D(50),high=D(100)),
                 'BTC':replace(bars([100])[0],low=D(80),high=D(120))}
        low,high=equity_envelope([(D(0),{'ETH':D(1),'BTC':D(1)})],candles,set())
        self.assertEqual((low,high),(D(130),D(220)))
        upper=drawdown_upper_bound([{'equity_lower_bound':str(low),'equity_upper_bound':str(high)}],D(200))
        # A possible observed path with distinct extrema: 200, 170, 180, 200.
        self.assertAlmostEqual(upper,1-130/220)
        self.assertGreater(upper,.15)

    def test_fifty_percent_intraday_crash_is_visible_without_inventing_path(self):
        p={'ETH':[replace(b,open=D(100),close=D(100),high=D(100),low=D(50)) for b in bars([100]*4)]}
        r=run(p,TREND,BASE+2*DAY,BASE+3*DAY,Settings(),holdout_start_ms=CUTOFF)
        self.assertEqual(r['metrics']['maximum_drawdown'],0)
        self.assertEqual(r['risk']['daily_close_maximum_drawdown'],0)
        self.assertEqual(r['risk']['ohlc_maximum_drawdown_upper_bound'],.5)
        self.assertFalse(r['risk']['intraday_drawdown_observed'])
        self.assertEqual(r['curve'][0]['equity_lower_bound'],'25.0')
        self.assertIn('within_run',r['metrics']['maximum_drawdown_basis'])

    def test_multiasset_bound_encloses_closes_and_exposure_changes(self):
        r=intraday(wide_panel())
        self.assertGreater(r['risk']['ohlc_maximum_drawdown_upper_bound'],r['metrics']['maximum_drawdown'])
        for row in r['curve']:
            self.assertLessEqual(D(row['equity_lower_bound']),D(row['equity']))
            self.assertGreaterEqual(D(row['equity_upper_bound']),D(row['equity']))
        self.assertIn('extrema/order_may_not_coincide',r['risk']['bound_method'])

    def test_suspended_holdings_flag_inconclusive_and_zero_recovery_not_a_sale(self):
        p=fixture(list(range(100,112)))
        status={t:{'ETH':False,'BTC':False} for t in range(BASE+2*DAY,BASE+10*DAY,DAY)}
        r=run(p,TREND,BASE+2*DAY,BASE+10*DAY,Settings(),holdout_start_ms=CUTOFF,market_status=status)
        self.assertEqual(r['orders_executed'],0)
        self.assertEqual(r['valuation_status'],'inconclusive')
        self.assertFalse(r['promotion_eligible_on_valuation'])
        self.assertEqual(r['risk']['ohlc_maximum_drawdown_upper_bound'],1)
        self.assertTrue(all(D(x['zero_recovery_close_equity'])==0 for x in r['curve']))
        self.assertTrue(all(D(x['inventory']['ETH'])==D('.5') for x in r['curve']))

    def test_unheld_suspension_does_not_invalidate_owned_eth_mark(self):
        p=fixture(list(range(100,112)))
        r=run(p,TREND,BASE+2*DAY,BASE+10*DAY,Settings(),holdout_start_ms=CUTOFF,
              market_status={t:{'BTC':False} for t in range(BASE+2*DAY,BASE+10*DAY,DAY)})
        self.assertEqual(r['valuation_issues'],[])
        self.assertTrue(r['promotion_eligible_on_valuation'])

    def test_continuous_run_keeps_signal_memory_instead_of_monthly_reset(self):
        p={a:bars([100]*19+[50,95]+[100]*40) for a in ['ETH','BTC']}
        v={'family':'reversal','lookback_days':20,'entry_z':1}
        full=run(p,v,BASE+20*DAY,BASE+40*DAY,Settings(),holdout_start_ms=CUTOFF)
        fresh=run(p,v,BASE+21*DAY,BASE+40*DAY,Settings(),holdout_start_ms=CUTOFF)
        self.assertTrue(full['decisions'][1]['active']['ETH'])
        self.assertFalse(fresh['decisions'][0]['active']['ETH'])
        self.assertEqual(len(full['curve']),20)


class CostContract(unittest.TestCase):
    def test_combined_cost_and_delay_apply_together(self):
        r=simulate(fixture(list(range(100,112))),Settings(friction_round_trip_bps=D(50),extra_delay_bars=1))
        self.assertEqual(r['fills'][0]['signal_close_to_fill_seconds'],2*86400)
        self.assertTrue(all(f['noncommission_round_trip_bps']=='50' for f in r['fills']))
        self.assertGreater(D(r['commission_quote']),0)
        self.assertGreater(D(r['modeled_adverse_price_cost']),0)

    def test_range_stress_uses_prior_available_bar_and_cannot_see_future_range(self):
        p=fixture(list(range(100,112)))
        settings=Settings(stress_range_threshold=D('.1'),stress_friction_multiplier=D(3))
        a=simulate(p,settings)
        changed={asset:[replace(b,high=D(200)) if i==5 else b for i,b in enumerate(bs)] for asset,bs in p.items()}
        b=simulate(changed,settings)
        self.assertEqual(a['decisions'][:4],b['decisions'][:4])
        self.assertEqual(b['decisions'][4]['noncommission_round_trip_bps'],'45')
        self.assertEqual(b['decisions'][5]['noncommission_round_trip_bps'],'15')
        self.assertTrue(all(f['noncommission_round_trip_bps']=='45' for f in b['fills'] if f['source_close_ms']==BASE+6*DAY))

    def test_bad_timing_and_stress_inputs_fail(self):
        for changes in [dict(execution_interval_minutes=7),dict(execution_interval_minutes=15),
                        dict(extra_delay_bars=.5),dict(processing_minutes=1440),
                        dict(stress_range_threshold=D(0)),dict(stress_friction_multiplier=D('.5')),
                        dict(stress_friction_multiplier=D('NaN'))]:
            with self.subTest(changes=changes), self.assertRaises(ValueError):Settings(**changes).validate()
