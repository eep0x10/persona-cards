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
        self.assertEqual(d['revisao_editorial'],'5.2.2')
        self.assertEqual(len(d['cartas']),169)
        self.assertEqual(len({c['codigo'] for c in d['cartas']}),169)
        self.assertEqual(sum(c['familia'] in BUILDER.FAMILIES for c in d['cartas']),153)
        self.assertEqual(d['familias_sorteaveis'],['OR','CV','D','F','V','L','P','N'])
        self.assertEqual(d['criacao_completa']['guia'],'G07')
        self.assertEqual(d['criacao_completa']['journey'],['call','response','fact','belief','choice'])
        self.assertEqual(d['modulos']['expansao_5_2'],27)
        self.assertEqual(d['modulos']['guia_contexto'],7)
        hashes={'5.0':'eb97dcae9235f08008fcea79ee765d8735b1b5eff5453a6e9b8dd79e09dab7e5',
                '5.1':'181d079735ed27358a911bc3e1affc249ac3815ca740fa0330115563210ea06f'}
        for version,expected in hashes.items():
            self.assertEqual(hashlib.sha256((ROOT/f'deck/persona-cards-{version}.json').read_bytes()).hexdigest(),expected)

    def test_old_card_identity_and_only_versioned_text_patches_change(self):
        previous=json.loads((ROOT/'deck/persona-cards-5.1.json').read_bytes())
        current={c['codigo']:c for c in BUILDER.build_deck()['cartas']}
        revision=json.loads(BUILDER.REVISION.read_text(encoding='utf-8'))
        for old in previous['cartas']:
            new=deepcopy(current[old['codigo']])
            expected_title=revision['revisoes'].get(old['codigo'],{}).get('titulo',old['titulo'])
            self.assertEqual(new['titulo'],expected_title)
            self.assertEqual(new['modulo'],old['modulo'])
            self.assertEqual(new['familia'],old['familia'])
            new['versao']=old['versao']
            if old['codigo'] not in BUILDER.GUIDE_REVISIONS | BUILDER.EDITORIAL_REVISIONS:
                self.assertEqual(new,old,old['codigo'])
        self.assertNotIn('opcional',current['G06']['campos']['Use'].lower())
        self.assertIn('não o omita',current['G06']['campos']['Use'])

    def test_editorial_patch_adds_only_three_cards_and_rejects_identity_edits(self):
        revision=json.loads(BUILDER.REVISION.read_text(encoding='utf-8'))
        current={c['codigo']:c for c in BUILDER.build_deck()['cartas']}
        self.assertEqual(set(revision['revisoes']),{'OR03','N14','P12','L13','D06','G06','U08'})
        self.assertEqual({c['codigo'] for c in revision['cartas']},{'F21','F22','N23'})
        self.assertEqual({c['codigo'] for c in current.values() if c['familia']=='F'},
                         {f'F{n:02d}' for n in range(1,23)})
        self.assertEqual({c['codigo'] for c in current.values() if c['familia']=='N'},
                         {f'N{n:02d}' for n in range(1,24)})
        for card in revision['cartas']:
            self.assertEqual(current[card['codigo']],card)
        for code,patch in revision['revisoes'].items():
            for field,value in patch.items():self.assertEqual(current[code][field],value)
        self.assertIn('F21–22/N23',current['U08']['campos']['Distribua'])
        original=BUILDER.REVISION
        try:
            with tempfile.TemporaryDirectory() as directory:
                invalid=deepcopy(revision)
                invalid['revisoes']['N14']['modulo']='nucleo'
                BUILDER.REVISION=Path(directory)/'invalid.json'
                BUILDER.REVISION.write_text(json.dumps(invalid),encoding='utf-8')
                with self.assertRaisesRegex(ValueError,'cannot change identity'):
                    BUILDER.build_deck()
        finally:BUILDER.REVISION=original

    def test_journey_revision_preserves_other_168_cards_and_source_bytes(self):
        current=BUILDER.build_deck()['cartas']
        unaffected=json.dumps([c for c in current if c['codigo']!='G07'],ensure_ascii=False,
                              sort_keys=True,separators=(',',':')).encode()
        self.assertEqual(hashlib.sha256(unaffected).hexdigest(),
                         'f1766e3ec126c466ff8f2c9818395da9dbdd1022f5c26684e3a441bb5bef89d1')
        for path,expected in [
            (BUILDER.EXPANSION,'70fb8c0fb6e4e200a5e946bb7e6b1695fe019a81f5eeea2cde5f61ca57784445'),
            (BUILDER.REVISION,'7d1fec169d9fee006806b55f606b9ea277327312936338b18a5bf03b9ad28f6c')]:
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),expected)
        original=next(c for c in json.loads(BUILDER.EXPANSION.read_bytes())['cartas'] if c['codigo']=='G07')
        guide=next(c for c in current if c['codigo']=='G07')
        self.assertEqual(set(guide),set(original))
        self.assertEqual(list(guide['campos']),list(original['campos']))
        for key in ['versao','codigo','titulo','familia','modulo']:
            self.assertEqual(guide[key],original[key])
        for key in ['Chamado','Resposta','Crença']:
            self.assertEqual(guide['campos'][key],original['campos'][key])
        self.assertIn('não assumo o chamado',guide['campos']['Escolha'])
        self.assertIn('se as condições mudarem',guide['campos']['Escolha'])
        self.assertIn('registre a ordem',guide['leitura'])

    def test_journey_patch_rejects_other_cards_and_changed_d6_lists(self):
        revision=json.loads(BUILDER.JOURNEY_REVISION.read_bytes())
        original=BUILDER.JOURNEY_REVISION
        try:
            with tempfile.TemporaryDirectory() as directory:
                BUILDER.JOURNEY_REVISION=Path(directory)/'invalid.json'
                for target in ['other-card','d6-list']:
                    invalid=deepcopy(revision)
                    if target=='other-card':invalid['revisoes']['G06']={'leitura':'changed'}
                    else:invalid['revisoes']['G07']['campos']['Resposta']='changed'
                    BUILDER.JOURNEY_REVISION.write_text(json.dumps(invalid),encoding='utf-8')
                    with self.assertRaises(ValueError):BUILDER.build_deck()
        finally:BUILDER.JOURNEY_REVISION=original

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
