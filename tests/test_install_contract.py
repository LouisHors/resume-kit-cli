import unittest
from pathlib import Path


class InstallContractTests(unittest.TestCase):
    def test_makefile_exists(self):
        self.assertTrue(Path("Makefile").exists())

    def test_readme_documents_package_command(self):
        text = Path("README.md").read_text(encoding="utf-8")
        self.assertIn("resume-kit package", text)
        self.assertIn("resume-kit doctor --json", text)
