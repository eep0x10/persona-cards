"""Published print checksums must survive a Git checkout without PDF tooling."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ArtifactTransport(unittest.TestCase):
    def test_print_sources_and_download_bytes_match_receipt(self):
        folder = ROOT / 'skills/persona-cards/print'
        report = json.loads((folder / 'verificacao-impressao-5.2-ilustrado.json').read_text(encoding='utf8'))
        def digest(path):
            return hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(report['manifest_sha256'], digest(ROOT / 'deck/illustration_sheets_5_2.json'))
        self.assertEqual(report['deck_sha256'], digest(ROOT / 'deck/persona-cards-5.2.json'))
        for name, expected in report['files'].items():
            with self.subTest(file=name):
                self.assertEqual(expected, digest(folder / name))

if __name__ == '__main__':
    unittest.main()
