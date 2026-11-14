"""Calendar coverage and paired reporting, not investment-performance tests."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from run_rolling import windows,summarize


class RollingFixtures(unittest.TestCase):
    def test_all_months_and_holdout_boundary(self):
        dates=windows('2021-01-01','2025-11-13')
        self.assertEqual(len(dates),47)
        self.assertEqual(dates[0],('2021-01-01','2022-01-01'))
        self.assertEqual(dates[-1],('2024-11-01','2025-11-01'))
        self.assertIn(('2023-03-01','2024-03-01'),dates)  # Includes leap day.
        self.assertEqual(windows('2024-12-01','2025-11-13'),[])
        with self.assertRaises(ValueError):windows('2021-01-02','2025-11-13')

    def test_counts_and_paired_excess(self):
        rows=[dict(strategy_return=a,eth_return=b,strategy_drawdown=.1,eth_drawdown=.2) for a,b in [(.3,.1),(-.2,-.1),(.1,.1)]]
        s=summarize(rows)
        self.assertEqual(s['beat_eth_count'],1)
        self.assertEqual(s['loss_count'],1)
        self.assertEqual(s['median_return'],.1)
        self.assertEqual(s['median_paired_excess_return'],0)
        self.assertEqual(s['worst_return'],-.2)
