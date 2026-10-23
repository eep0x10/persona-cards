import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_DECK = ROOT / 'deck/persona-cards-5.0.json'
DECK = ROOT / 'deck/persona-cards-5.1.json'
HELPER = ROOT / 'skills/persona-cards/scripts/cards.py'

class DeckContract(unittest.TestCase):
    def test_frozen_history_and_equal_active_copies(self):
        old_raw = HISTORICAL_DECK.read_bytes()
        self.assertEqual(hashlib.sha256(old_raw).hexdigest(), 'eb97dcae9235f08008fcea79ee765d8735b1b5eff5453a6e9b8dd79e09dab7e5')
        raw = DECK.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), '6c33a7adb5187c8e909ab5a3bc6c4b283a79c670d03b67ea3c1c32333229f86d')
        for relative in ['app/public/deck.json', 'skills/persona-cards/references/deck.json']:
            self.assertEqual(raw, (ROOT / relative).read_bytes())
        cards = json.loads(raw)['cartas']
        old_cards = json.loads(old_raw)['cartas']
        self.assertEqual(len(cards), 141)
        self.assertEqual(len({c['codigo'] for c in cards}), 141)
        self.assertEqual(sum(c['familia'] in 'DFNLVP' for c in cards), 126)
        self.assertEqual(len({c['leitura'] for c in cards}), 141)
        for old, new in zip(old_cards, cards):
            self.assertEqual(old['codigo'], new['codigo'])
            self.assertEqual(old['titulo'], new['titulo'])
            self.assertEqual(old['campos'], new['campos'])
            self.assertEqual(old['modulo'], new['modulo'])

    def run_helper(self, *args):
        return subprocess.run([sys.executable, '-X', 'utf8', str(HELPER), *args], capture_output=True, text=True, encoding='utf-8')

    def test_lookup_and_accent_search(self):
        self.assertEqual(json.loads(self.run_helper('get', 'D19', 'G06').stdout)[1]['codigo'], 'G06')
        self.assertIn('D23', [c['codigo'] for c in json.loads(self.run_helper('search', 'vocacao').stdout)])
        self.assertNotEqual(self.run_helper('get', 'D99').returncode, 0)

    def test_draw_limits(self):
        result = self.run_helper('draw', '--seed', '42', '--modules', 'nucleo')
        self.assertEqual(result.returncode, 0)
        cards = json.loads(result.stdout)
        self.assertEqual([c['familia'] for c in cards], ['D', 'F', 'V'])
        self.assertTrue(all(c['modulo'] == 'nucleo' for c in cards))
        for args in [('draw', '--families', 'G'), ('draw', '--families', 'D', 'D'), ('draw', '--families', 'P', '--modules', 'expansao_5')]:
            self.assertNotEqual(self.run_helper(*args).returncode, 0)

if __name__ == '__main__':
    unittest.main()
