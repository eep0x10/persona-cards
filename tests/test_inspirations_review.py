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
        deck=json.loads((ROOT/'deck/persona-cards-5.2.json').read_text(encoding='utf-8'))
        self.assertEqual(review['deckRevision'],deck['revisao_editorial'])
        self.assertEqual(review['previousDeckRevision'],'5.2.1')
        history=json.loads((ROOT/'docs/reviews'/review['previousReviewPath']).read_text(encoding='utf-8'))
        self.assertEqual(review['previousCatalogSha256'],history['catalogSha256'])
        self.assertEqual(history['deckRevision'],review['previousDeckRevision'])
        self.assertTrue(all(r['previousCards'] is not None for r in history['records']))
        self.assertTrue(all(r['previousCards'] is not None for r in review['records']))
        previous={r['id']:r for r in history['records']}
        valid={c['codigo']:c['familia'] for c in deck['cartas']}
        for r,e in zip(review['records'],catalog['characters']):
            self.assertEqual(r['previousCards'],previous[r['id']]['cards'],e['id'])
            self.assertEqual(r['cards'],e['character']['cards'],e['id'])
            self.assertEqual(list(r['cards']),ORDER,e['id'])
            self.assertEqual(list(e['character']['fields']),ORDER,e['id'])
            self.assertEqual(list(e['rationale']),ORDER,e['id'])
            self.assertTrue(all(valid[code]==family for family,code in r['cards'].items()),e['id'])
            self.assertEqual(set(r['reason']),set(ORDER+['G07']),e['id'])
            self.assertTrue(all(isinstance(s,str) and len(s.strip())>=25 for s in r['reason'].values()),e['id'])
            changed=ORDER if r['previousCards'] is None else [f for f in ORDER if r['previousCards'][f]!=r['cards'][f]]
            self.assertEqual(r['changedFamilies'],changed,e['id'])
            self.assertGreater(len(r['recorte'].strip()),15,e['id'])
            self.assertTrue(r['evidence'],e['id'])
            for family,change in r['fieldChanges'].items():
                self.assertNotEqual(change['before'],change['after'],e['id'])
                self.assertEqual(change['after'],e['character']['fields'][family],e['id'])
            for key,change in r['journeyChanges'].items():
                self.assertNotEqual(change['before'],change['after'],e['id'])
                self.assertEqual(change['after'],e['character']['journey'][key],e['id'])
            self.assertEqual(list(e['character']['journey']),['call','response','fact','belief','choice'],e['id'])
            self.assertTrue(all(len(value.strip())>=20 for value in e['character']['journey'].values()),e['id'])
            self.assertIn('Premissa da cena autoral:',e['character']['journey']['fact'],e['id'])
            for source in r['evidence']:
                self.assertTrue(source['url'].startswith('https://'),e['id'])
                self.assertGreater(len(source['note'].strip()),10,e['id'])
