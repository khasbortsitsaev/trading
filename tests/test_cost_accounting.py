"""Independent hand-calculated fixtures for the cost research calculator."""
from decimal import Decimal as D
import importlib.util
from pathlib import Path
import tempfile
import unittest

script = Path(__file__).resolve().parents[1] / 'scripts' / 'analyze_costs.py'
spec = importlib.util.spec_from_file_location('cost_analysis', script)
costs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(costs)


class CostAccountingTests(unittest.TestCase):
    def test_quote_fee_break_even_preserves_starting_equity(self):
        # Buy one unit at 100, pay 1 quote fee, then sell with a 2% exit fee.
        starting_cash = D(101)
        required_exit = D(101) / D('0.98')
        hurdle = costs.commission_hurdle(D('0.01'), D('0.02'))
        self.assertLess(abs(D(100) * (1 + hurdle) - required_exit), D('1e-23'))
        self.assertLess(abs(required_exit * D('0.98') - starting_cash), D('1e-23'))
        self.assertEqual(costs.commission_hurdle(D(0), D(0)), D(0))

    def test_multi_level_sweep_and_insufficient_depth(self):
        asks = [(D(100), D(1)), (D(102), D(2))]
        # One unit at 100 and half a unit at 102 = 151 quote units.
        self.assertEqual(costs.sweep(asks, D('1.5')), D(151))
        self.assertEqual(costs.sweep(asks, D(3)), D(304))
        self.assertIsNone(costs.sweep(asks, D('3.0001')))

    def test_fee_reserved_budget_and_rounding(self):
        asks = [(D(100), D(1)), (D(102), D(2))]
        # 151 quote notional + 1% fee buys 1.5 units, not 1.51 or more.
        q = costs.affordable_quantity(asks, D('152.51'), D('0.01'), 8)
        self.assertEqual(q, D('1.5'))
        q = costs.affordable_quantity(asks, D('152.50'), D('0.01'), 2)
        self.assertEqual(q, D('1.49'))
        self.assertLessEqual(costs.sweep(asks, q) * D('1.01'), D('152.50'))
        self.assertIsNone(costs.affordable_quantity(asks, D(1000), D('0.01'), 8))

    def test_spread_cost_is_not_a_second_commission(self):
        # Buying one unit for 101 and selling for 99 with 1% fees:
        # outlay 102.01, receipts 98.01; loss is 4/102.01, not 6/102.01.
        asks, bids = [(D(101), D(2))], [(D(99), D(2))]
        spent = costs.sweep(asks, D(1)) * D('1.01')
        received = costs.sweep(bids, D(1)) * D('0.99')
        self.assertEqual(spent - received, D(4))
        self.assertEqual(spent, D('102.01'))

    def test_malformed_books_and_invalid_fees_fail(self):
        for payload in [
            {'bids': [['101', '1']], 'asks': [['100', '1']]},
            {'bids': [], 'asks': [['100', '1']]},
            {'bids': [['99', '-1']], 'asks': [['100', '1']]},
            {'bids': [['98', '1'], ['99', '1']], 'asks': [['100', '1']]},
        ]:
            with self.assertRaises(ValueError):
                costs.parse_book(payload, 'bitvavo')
        for fee in [D('-0.01'), D(1)]:
            with self.assertRaises(ValueError):
                costs.commission_hurdle(fee, D(0))

    def test_zero_snapshot_run_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'zero-sample'):
                costs.analyze(Path(tmp), {})


if __name__ == '__main__':
    unittest.main()
