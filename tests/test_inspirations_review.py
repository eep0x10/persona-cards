"""Release evidence is tied to every reviewed character and the exact catalogue."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
ORDER=['OR','CV','D','F','V','L','P','N']

class InspirationReview(unittest.TestCase):
    def test_all_105_decisions_are_tied_to_the_current_cards(self):
        raw=(ROOT/'app/public/inspirations.json').read_bytes()
        catalog=json.loads(raw)
        review=json.loads((ROOT/'docs/reviews/inspiration-105-review.json').read_text(encoding='utf-8'))
        self.assertEqual(review['catalogSha256'],hashlib.sha256(raw).hexdigest())
        self.assertEqual(len(review['records']),105)
        self.assertEqual([r['id'] for r in review['records']],[e['id'] for e in catalog['characters']])
        self.assertEqual(sum(r['previousCards'] is None for r in review['records']),5)
        for r,e in zip(review['records'],catalog['characters']):
            self.assertEqual(r['cards'],e['character']['cards'],e['id'])
            self.assertEqual(set(r['reason']),set(ORDER+['G07']),e['id'])
            self.assertTrue(all(isinstance(s,str) and len(s.strip())>=25 for s in r['reason'].values()),e['id'])
            changed=ORDER if r['previousCards'] is None else [f for f in ORDER if r['previousCards'][f]!=r['cards'][f]]
            self.assertEqual(r['changedFamilies'],changed,e['id'])
            self.assertGreater(len(r['recorte'].strip()),15,e['id'])
            self.assertTrue(r['evidence'],e['id'])
            for source in r['evidence']:
                self.assertTrue(source['url'].startswith('https://'),e['id'])
                self.assertGreater(len(source['note'].strip()),10,e['id'])
