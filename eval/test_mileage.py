"""Mileage sensitivity rejects silent assumptions and invalid financial inputs."""
from decimal import Decimal
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/orchestrator/scripts/mileage_adjustment.py'
spec = importlib.util.spec_from_file_location('mileage', SCRIPT)
mileage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mileage)


class MileageTests(unittest.TestCase):
    def test_explicit_zero_and_cent_rounding(self):
        self.assertEqual(mileage.compute_mileage_adjustment(10000, 10001, '0'), Decimal('0.00'))
        self.assertEqual(mileage.compute_mileage_adjustment(10000, 10001, '0.125'), Decimal('0.13'))

    def test_invalid_mileage_or_rate_fails(self):
        for args in ((-1, 3, '.1'), (1.5, 3, '.1'), (True, 3, '.1'), (1, 3, 'NaN'), (1, 3, '-1'), ('1e999999999', 0, 1)):
            with self.subTest(args=args), self.assertRaises(ValueError):
                mileage.compute_mileage_adjustment(*args)

    def test_cli_requires_explicit_rate(self):
        result = subprocess.run([sys.executable, str(SCRIPT), '--miles-a', '10000', '--miles-b', '12000'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--rate', result.stderr)


if __name__ == '__main__':
    unittest.main()
