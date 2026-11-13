"""Hand-calculated and adversarial fixtures, with synthetic prices only."""
from datetime import datetime, timedelta, timezone
from decimal import Decimal as D
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from trading_research.core import (DataError, HoldoutAccessError, Portfolio, Rules,
    audit_candles, deduplicate_trades, report_wealth, scheduled_reference, validate_weights)

UTC = timezone.utc
T = datetime(2024, 1, 2, tzinfo=UTC)
TIMES = dict(available_at=T, decision_at=T, ready_at=T+timedelta(minutes=5), fill_at=T+timedelta(days=1))


def fill(p, side, quantity, price='100', fee='0.01', asset='ETH', **kwargs):
    return p.fill(asset, side, quantity, price, fee, kwargs.pop('rules', Rules()), **TIMES, **kwargs)


class PortfolioFixtures(unittest.TestCase):
    def test_two_asset_rotation_reconciles_every_fee(self):
        p = Portfolio(inventory={'ETH': '.5'})
        fill(p, 'sell', '.25', price='1000', fee='.001')
        fill(p, 'buy', '.005', price='40000', fee='.001', asset='BTC')
        self.assertEqual(p.cash, D('49.55'))
        self.assertEqual(p.inventory, {'ETH': D('.25'), 'BTC': D('.005')})
        self.assertEqual(p.equity({'ETH': '1000', 'BTC': '40000'}), D('499.55'))
        self.assertEqual(len(p.events), 2)

    def test_buy_and_sell_quote_fees(self):
        p = Portfolio('1000', {'ETH': '.5'})
        fill(p, 'buy', '1')
        fill(p, 'sell', '.5', price='120')
        self.assertEqual(p.cash, D('958.40'))
        self.assertEqual(p.inventory['ETH'], D(1))

    def test_base_asset_fee_and_no_forced_conversion(self):
        p = Portfolio('100')
        fill(p, 'buy', '1', fee_asset='base')
        self.assertEqual(p.cash, 0)
        self.assertEqual(p.inventory['ETH'], D('.99'))
        initial = Portfolio(inventory={'ETH': '.5'})
        report = report_wealth(initial, {'ETH': '1000'}, '1000', '.8')
        self.assertEqual(report, {'quote': D(500), 'eth_equivalent': D('.5'), 'usdc': D(625)})
        self.assertEqual(initial.events, [])

    def test_overspending_fees_rejects_atomically(self):
        p = Portfolio('100')
        with self.assertRaises(ValueError):
            fill(p, 'buy', '1')
        self.assertEqual((p.cash, p.inventory, p.events), (D(100), {}, []))

    def test_selling_unowned_inventory_or_base_fee_rejects(self):
        for p, kwargs in [(Portfolio('100'), {}), (Portfolio(inventory={'ETH': '1'}), {'fee_asset': 'base'})]:
            with self.assertRaises(ValueError):
                fill(p, 'sell', '1', **kwargs)
            self.assertEqual(p.events, [])

    def test_minimums_precision_tick_and_suspension(self):
        cases = [('.01', '100', {'rules': Rules(minimum_quote=D(5))}),
                 ('.0011', '100', {'rules': Rules(quantity_decimals=2)}),
                 ('1', '100.001', {}), ('1', '100', {'tradable': False})]
        for qty, price, kwargs in cases:
            p = Portfolio('1000')
            with self.assertRaises(ValueError):
                fill(p, 'buy', qty, price=price, **kwargs)
            self.assertEqual(p.cash, D(1000))
            self.assertEqual(p.events, [])

    def test_future_inputs_and_same_instant_fill_reject(self):
        for changed in [dict(available_at=T+timedelta(seconds=1)), dict(fill_at=T), dict(ready_at=T)]:
            times = TIMES | changed
            with self.assertRaises(DataError):
                Portfolio('1000').fill('ETH','buy','1','100','.01',Rules(),**times)

    def test_cash_benchmark_conversion_charged_once(self):
        p = Portfolio(inventory={'ETH': '.5'})
        fill(p, 'sell', '.5', price='1000', fee='.0025')
        self.assertEqual(p.cash, D('498.75'))
        self.assertEqual(p.equity({}), D('498.75'))
        self.assertEqual(len(p.events), 1)

    def test_missing_future_and_stale_marks_reject(self):
        p = Portfolio(inventory={'ETH': '.5'})
        for marks in [{}, {'ETH': ('100', T-timedelta(hours=2))}, {'ETH': ('100', T+timedelta(seconds=1))}]:
            with self.assertRaises(DataError):
                p.marked_equity(marks, T, timedelta(hours=1))
        self.assertEqual(p.marked_equity({'ETH': ('100',T)}, T, timedelta(hours=1)), D(50))

    def test_multiple_weights_no_arbitrary_position_count_or_leverage(self):
        self.assertEqual(len(validate_weights({str(i): '.05' for i in range(20)})), 20)
        for weights in [{'ETH': '-.1'}, {'ETH': '.6', 'BTC': '.5'}, {'ETH': 'NaN'}]:
            with self.assertRaises(ValueError):
                validate_weights(weights)


class CausalDataFixtures(unittest.TestCase):
    def test_one_full_daily_buffer_and_extra_delay(self):
        bars = [{'start': T+timedelta(days=i), 'open': '100'} for i in [0,1,2]]
        first = scheduled_reference(T,T,bars)
        self.assertEqual(first['start'], T+timedelta(days=1))
        self.assertEqual(scheduled_reference(T,T,bars,extra_bars=1)['start'], T+timedelta(days=2))

    def test_missing_or_delisted_designated_bar_does_not_fill_later(self):
        later = {'start': T+timedelta(days=2), 'open': '100'}
        self.assertIsNone(scheduled_reference(T,T,[later]))
        suspended = {'start': T+timedelta(days=1), 'open': '100','tradable': False}
        self.assertIsNone(scheduled_reference(T,T,[suspended,later]))

    def test_availability_and_timezone_reject(self):
        with self.assertRaises(DataError):
            scheduled_reference(T+timedelta(seconds=1),T,[])
        with self.assertRaises(ValueError):
            scheduled_reference(T.replace(tzinfo=None),T,[])

    def test_descending_and_overlapping_pages_are_normalized(self):
        a = [0,'1','3','.5','2','4'];b = [86400000,'2','4','1','3','5']
        rows, report = audit_candles([[b,a],[b]],0,172800000)
        self.assertEqual([x.timestamp_ms for x in rows], [0,86400000])
        self.assertEqual(report['identical_overlaps'],1)
        self.assertEqual(report['missing_count'],0)

    def test_missing_day_is_reported_not_filled(self):
        rows, report = audit_candles([[[0,'1','3','.5','2','4']]],0,172800000)
        self.assertEqual(len(rows),1)
        self.assertEqual(report['missing_timestamps_ms'],[86400000])

    def test_conflicting_duplicate_and_invalid_bar_fail(self):
        a = [0,'1','3','.5','2','4']
        for bad in [[0,'1','3','.5','2.5','4'], [0,'1','.2','.5','2','4'], [0,'NaN','3','.5','2','4']]:
            with self.assertRaises(ValueError):
                audit_candles([[a,bad]],0,86400000)

    def test_holdout_in_request_or_response_rejects(self):
        with self.assertRaises(HoldoutAccessError):
            audit_candles([],0,172800000,holdout_start_ms=86400000)
        with self.assertRaises(HoldoutAccessError):
            audit_candles([[[86400000,'1','3','.5','2','4']]],0,86400000,holdout_start_ms=86400000)

    def test_trade_ids_not_timestamps_control_overlap(self):
        a = {'trade_id': 1,'timestamp': 100,'price': '2'}
        b = {'trade_id': 2,'timestamp': 100,'price': '2'}
        self.assertEqual(len(deduplicate_trades([a,a,b])),2)
        with self.assertRaises(DataError):
            deduplicate_trades([a,a|{'price':'3'}])


if __name__ == '__main__':
    unittest.main()
