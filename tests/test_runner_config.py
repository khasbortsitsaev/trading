"""Verify editable assumptions actually reach a complete CLI run."""
import importlib.util
import json
import hashlib
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('research_cli', ROOT/'scripts/run_research.py')
cli = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cli)


class RunnerConfigTests(unittest.TestCase):
    def test_intraday_cli_binds_separate_data_hashes_and_fills_at_fifteen_minutes(self):
        from dataclasses import replace
        from test_model_contract import wide_panel
        with tempfile.TemporaryDirectory() as directory:
            base=Path(directory);root=base/'checkout';(root/'config').mkdir(parents=True)
            policy=json.loads((ROOT/'config/research-policy.json').read_text())
            variant={'id':'FIXTURE-TREND-1','family':'trend','lookback_days':1}
            policy['variants'].append(variant);policy['poc']['active_variant']=variant['id']
            execution=json.loads((ROOT/'config/runner.json').read_text())
            execution['execution_interval_minutes']=15
            panel=wide_panel()
            intraday={a:[replace(b,timestamp_ms=b.timestamp_ms+i*15*60000,
                                  open=b.open,close=b.open,high=b.open,low=b.open)
                         for b in bs[2:10] for i in range(96)] for a,bs in panel.items()}
            def save(name, data, interval=None):
                target=base/name;target.mkdir()
                body=json.dumps({a:[[b.timestamp_ms,*map(str,[b.open,b.high,b.low,b.close,b.volume])]
                                     for b in bs] for a,bs in data.items()}).encode()
                (target/'normalized.json').write_bytes(body)
                manifest={'provider':'synthetic_fixture_not_market_data','quote':'USD','complete':True,
                          'normalized_sha256':hashlib.sha256(body).hexdigest()}
                if interval:manifest['interval_ms']=interval
                raw=json.dumps(manifest).encode();(target/'manifest.json').write_bytes(raw)
                admission={'source':manifest['provider'],'quote':'USD','normalized_sha256':manifest['normalized_sha256'],
                           'manifest_sha256':hashlib.sha256(raw).hexdigest()}
                return target,admission
            daily,daily_admission=save('daily',panel)
            intraday_dir,intraday_admission=save('intraday',intraday,900000)
            policy['dataset_admission']=daily_admission
            policy['execution_dataset_admission']=intraday_admission
            (root/'config/research-policy.json').write_text(json.dumps(policy))
            (root/'config/runner.json').write_text(json.dumps(execution))
            output=base/'result.json'
            with patch.object(cli,'ROOT',root), \
                 patch('sys.argv',['run_research.py','--data-dir',str(daily),'--proxy-usd',
                                   '--execution-data-dir',str(intraday_dir),'--variant',variant['id'],
                                   '--start','2020-01-03','--end-exclusive','2020-01-11','--output',str(output)]), \
                 patch.object(cli.subprocess,'check_output',return_value='fixture-commit\n'), \
                 patch.object(cli.subprocess,'run',return_value=SimpleNamespace(returncode=0)), \
                 patch('builtins.print'):
                cli.main()
            result=json.loads(output.read_text())
            self.assertEqual(result['dataset_sha256'],daily_admission['normalized_sha256'])
            self.assertEqual(result['execution_dataset_sha256'],intraday_admission['normalized_sha256'])
            self.assertNotEqual(result['dataset_sha256'],result['execution_dataset_sha256'])
            self.assertEqual(result['result']['fills'][0]['signal_close_to_fill_seconds'],900)
            self.assertFalse(result['result']['usdc_wealth_claimed'])

    def test_capital_and_friction_come_from_config_and_override_is_recorded(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root/'config').mkdir()
            policy = json.loads((ROOT/'config/research-policy.json').read_text())
            execution = json.loads((ROOT/'config/runner.json').read_text())
            execution.update(initial_eth='1.25', default_noncommission_round_trip_bps='37')
            (root/'config/research-policy.json').write_text(json.dumps(policy))
            (root/'config/runner.json').write_text(json.dumps(execution))
            for extra, expected in [([], '37'), (['--friction-bps', '50'], '50')]:
                output = root/'result.json'
                with patch.object(cli, 'ROOT', root), \
                     patch('sys.argv', ['run_research.py', '--synthetic', '--output', str(output), *extra]), \
                     patch.object(cli.subprocess, 'check_output', return_value='test-commit\n'), \
                     patch.object(cli.subprocess, 'run', return_value=SimpleNamespace(returncode=0)), \
                     patch('builtins.print'):
                    cli.main()
                result = json.loads(output.read_text())['result']
                self.assertEqual(result['initial_eth'], '1.25')
                self.assertEqual(result['settings']['noncommission_round_trip_bps'], expected)
