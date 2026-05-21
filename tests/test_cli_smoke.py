import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class CliSmokeTests(unittest.TestCase):
    def run_cli(self, *args):
        cmd = [
            sys.executable,
            str(ROOT / "resume_kit" / "cli.py"),
            *args,
        ]
        return subprocess.run(cmd, text=True, capture_output=True, check=False)

    def test_help(self):
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("resume-kit", result.stdout)
        self.assertIn("doctor", result.stdout)

    def test_json_doctor_shape(self):
        result = self.run_cli("doctor", "--json")
        self.assertEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertTrue(payload["ok"])
        self.assertIn("data", payload)
        self.assertIn("sources", payload["data"])
