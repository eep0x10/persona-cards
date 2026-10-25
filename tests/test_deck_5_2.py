from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('build_5_2',ROOT/'deck/build_5_2.py')
BUILDER=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class Complete52Contract(unittest.TestCase):
    def test_counts_metadata_active_copies_and_preserved_history(self):
        raw=(ROOT/'deck/persona-cards-5.2.json').read_bytes()
        for path in ['app/public/deck.json','skills/persona-cards/references/deck.json']:
            self.assertEqual(raw,(ROOT/path).read_bytes())
        d=json.loads(raw)
        self.assertEqual(d['versao'],'5.2')
        self.assertEqual(d['revisao_editorial'],'5.2.0')
        self.assertEqual(len(d['cartas']),166)
        self.assertEqual(len({c['codigo'] for c in d['cartas']}),166)
        self.assertEqual(sum(c['familia'] in BUILDER.FAMILIES for c in d['cartas']),150)
        self.assertEqual(d['familias_sorteaveis'],['OR','CV','D','F','V','L','P','N'])
        self.assertEqual(d['criacao_completa']['guia'],'G07')
        self.assertEqual(d['criacao_completa']['journey'],['call','response','fact','belief','choice'])
        self.assertEqual(d['modulos']['expansao_5_2'],24)
        self.assertEqual(d['modulos']['guia_contexto'],7)
        hashes={'5.0':'eb97dcae9235f08008fcea79ee765d8735b1b5eff5453a6e9b8dd79e09dab7e5',
                '5.1':'181d079735ed27358a911bc3e1affc249ac3815ca740fa0330115563210ea06f'}
        for version,expected in hashes.items():
            self.assertEqual(hashlib.sha256((ROOT/f'deck/persona-cards-{version}.json').read_bytes()).hexdigest(),expected)

    def test_old_card_identity_and_all_non_guide_text_is_preserved(self):
        previous=json.loads((ROOT/'deck/persona-cards-5.1.json').read_bytes())
        current={c['codigo']:c for c in BUILDER.build_deck()['cartas']}
        for old in previous['cartas']:
            new=deepcopy(current[old['codigo']])
            self.assertEqual(new['titulo'],old['titulo'])
            self.assertEqual(new['modulo'],old['modulo'])
            new['versao']=old['versao']
            if old['codigo'] not in BUILDER.GUIDE_REVISIONS:
                self.assertEqual(new,old,old['codigo'])
        self.assertNotIn('opcional',current['G06']['campos']['Use'].lower())
        self.assertIn('não a omiti-lo',current['G06']['campos']['Use'])

    def test_approved_prototype_text_and_two_complete_d6_lists(self):
        expansion=json.loads(BUILDER.EXPANSION.read_text(encoding='utf-8'))
        originals=expansion['cartas'][:24]
        canonical=json.dumps(originals,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
        self.assertEqual(hashlib.sha256(canonical).hexdigest(),'a1e8253b1f5c4ba114bbe764af04892130d7ef5fdeb3de4a41407e381a348cda')
        for family in ['OR','CV']:
            self.assertEqual([c['codigo'] for c in originals if c['familia']==family],[f'{family}{n:02d}' for n in range(1,13)])
        g=expansion['cartas'][24]
        self.assertEqual(list(g['campos']),['Chamado','Resposta','Fato','Crença','Escolha'])
        for field in ['Chamado','Resposta']:
            lines=g['campos'][field].splitlines()
            self.assertEqual(len(lines),6)
            self.assertTrue(all(line.startswith(f'{n}. ') for n,line in enumerate(lines,1)))

    def test_rebuild_is_deterministic_and_cli_defaults_to_eight(self):
        outputs=BUILDER.OUTPUTS
        try:
            with tempfile.TemporaryDirectory() as directory:
                BUILDER.OUTPUTS=tuple(Path(directory)/f'copy{i}.json' for i in range(3))
                BUILDER.main()
                first=[p.read_bytes() for p in BUILDER.OUTPUTS]
                BUILDER.main()
                self.assertEqual(first,[p.read_bytes() for p in BUILDER.OUTPUTS])
                self.assertTrue(all(raw==(ROOT/'deck/persona-cards-5.2.json').read_bytes() for raw in first))
        finally:BUILDER.OUTPUTS=outputs
        helper=ROOT/'skills/persona-cards/scripts/cards.py'
        result=subprocess.run([sys.executable,'-X','utf8',str(helper),'draw','--seed','12'],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual([c['familia'] for c in json.loads(result.stdout)],BUILDER.FAMILIES)
