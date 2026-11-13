"""Verify editable assumptions actually reach a complete CLI run."""
import importlib.util
import json
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
