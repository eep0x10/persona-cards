import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
HISTORICAL_DECK = ROOT / 'deck/persona-cards-5.0.json'
DECK = ROOT / 'deck/persona-cards-5.1.json'
HELPER = ROOT / 'skills/persona-cards/scripts/cards.py'
SPEC = importlib.util.spec_from_file_location('build_5_1', ROOT / 'deck/build_5_1.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)
EDITORIAL_CODES = {'U08', 'D10', 'D13'}

APPROVED = {
    'U08': {'campos': {
        'Distribua': 'Núcleo: 01–12. Expansão: 13–18. Expansão 5.0: D19–D24, F19–F20, N19–N22, L19–L20 e V19–V22; P termina em P18. Misture por família se quiser.',
        'Contraste': 'Varie desejo, método e expressão; sorteie sem reposição quando quiser reduzir repetições no elenco.',
        'Confira': 'Ausência de conflito não é falha. Não force trauma ou redenção.'}},
    'D10': {
        'leitura': 'Você quer ter poder sobre uma decisão. Que autoridade procura, e quem poderá contestá-la?',
        'campos': {
            'Quero': 'Obter [autoridade] para decidir [assunto].',
            'Mostre': 'Busca apoio, acesso ou posição que lhe permita decidir; descreva como usa esse poder.',
            'Interação': 'Declare a autoridade pretendida e a margem real de recusa dos demais. Só atribua um limite se a pessoa o reconhecer.'}},
    'D13': {
        'leitura': 'Uma ameaça pesa sobre sua continuidade. Você tenta atravessar este perigo ou impedir que ele volte a alcançá-lo?',
        'campos': {
            'Quero': 'Preservar minha vida diante de [ameaça], buscando [condição de sobrevivência].',
            'Mostre': 'Procura uma saída imediata ou uma proteção duradoura; diga qual delas orienta a próxima ação.',
            'Interação': 'Peça, exija ou procure o recurso necessário. Não presuma que desejar sobreviver determina os meios ou um limite moral.'}},
}

class DeckContract(unittest.TestCase):
    def test_frozen_50_and_51_history(self):
        old_raw = HISTORICAL_DECK.read_bytes()
        self.assertEqual(hashlib.sha256(old_raw).hexdigest(), 'eb97dcae9235f08008fcea79ee765d8735b1b5eff5453a6e9b8dd79e09dab7e5')
        raw = DECK.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), '181d079735ed27358a911bc3e1affc249ac3815ca740fa0330115563210ea06f')
        cards = json.loads(raw)['cartas']
        old_cards = json.loads(old_raw)['cartas']
        self.assertEqual(len(cards), 141)
        self.assertEqual(len({c['codigo'] for c in cards}), 141)
        self.assertEqual(sum(c['familia'] in 'DFNLVP' for c in cards), 126)
        self.assertEqual(len({c['leitura'] for c in cards}), 141)
        for old, new in zip(old_cards, cards):
            self.assertEqual(old['codigo'], new['codigo'])
            self.assertEqual(old['titulo'], new['titulo'])
            if old['codigo'] not in EDITORIAL_CODES:
                self.assertEqual(old['campos'], new['campos'])
            self.assertEqual(old['modulo'], new['modulo'])
            self.assertEqual(old['familia'], new['familia'])

    def test_only_approved_three_cards_change_from_previous_reading_edition(self):
        deck = json.loads(DECK.read_bytes())
        self.assertEqual(deck['versao'], '5.1')
        self.assertEqual(deck['revisao_editorial'], '5.1.1')
        unchanged = [c for c in deck['cartas'] if c['codigo'] not in EDITORIAL_CODES]
        self.assertEqual(len(unchanged), 138)
        canonical = json.dumps(unchanged, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        # Captured from the approved 5.1 source before this editorial correction.
        self.assertEqual(hashlib.sha256(canonical).hexdigest(), '80f9be74293403bc413c060eb28701c23cc63726ed70e6ea97b3fa60530b290f')
        by_code = {c['codigo']: c for c in deck['cartas']}
        for code, patch in APPROVED.items():
            for key, expected in patch.items():
                self.assertEqual(by_code[code][key], expected, code)
        self.assertEqual(by_code['U08']['leitura'], 'Varie objetivos, métodos e expressão sem obrigar todos a ter conflito.')
        self.assertEqual(json.loads(BUILDER.EDITORIAL.read_text(encoding='utf-8'))['alteracoes'], APPROVED)

    def test_overlay_rejects_out_of_scope_and_reading_drift_before_mutation(self):
        overlay = json.loads(BUILDER.EDITORIAL.read_text(encoding='utf-8'))
        for mutate in (
            lambda o: o['alteracoes'].update({'D06': {'campos': {}}}),
            lambda o: o['alteracoes']['D10'].update({'titulo': 'Novo título'}),
            lambda o: o['alteracoes']['D13'].update({'leitura': 'Uma abertura não aprovada.'}),
            lambda o: o['alteracoes']['U08']['campos'].update({'Outro': 'Campo fora do contrato'}),
            lambda o: o.update({'revisao_editorial': '5.2'}),
        ):
            candidate = deepcopy(overlay)
            mutate(candidate)
            deck = BUILDER.build_deck()
            before = deepcopy(deck)
            with self.assertRaises(ValueError):
                BUILDER.apply_editorial_overlay(deck, candidate)
            self.assertEqual(deck, before)

    def test_builder_reproduces_identical_bytes_without_rewriting_frozen_source(self):
        before = HISTORICAL_DECK.read_bytes()
        original_outputs = BUILDER.OUTPUTS
        try:
            with tempfile.TemporaryDirectory() as directory:
                BUILDER.OUTPUTS = tuple(Path(directory) / f'copy-{i}.json' for i in range(3))
                BUILDER.main()
                first = [p.read_bytes() for p in BUILDER.OUTPUTS]
                BUILDER.main()
                second = [p.read_bytes() for p in BUILDER.OUTPUTS]
                self.assertEqual(first, second)
                self.assertTrue(all(raw == DECK.read_bytes() for raw in second))
        finally:
            BUILDER.OUTPUTS = original_outputs
        self.assertEqual(before, HISTORICAL_DECK.read_bytes())

    def run_helper(self, *args):
        return subprocess.run([sys.executable, '-X', 'utf8', str(HELPER), *args], capture_output=True, text=True, encoding='utf-8')

    def test_lookup_and_accent_search(self):
        self.assertEqual(json.loads(self.run_helper('get', 'D19', 'G06').stdout)[1]['codigo'], 'G06')
        self.assertIn('D23', [c['codigo'] for c in json.loads(self.run_helper('search', 'vocacao').stdout)])
        self.assertNotEqual(self.run_helper('get', 'D99').returncode, 0)

    def test_draw_limits(self):
        result = self.run_helper('draw', '--seed', '42', '--modules', 'nucleo', '--families', 'D', 'F', 'V')
        self.assertEqual(result.returncode, 0)
        cards = json.loads(result.stdout)
        self.assertEqual([c['familia'] for c in cards], ['D', 'F', 'V'])
        self.assertTrue(all(c['modulo'] == 'nucleo' for c in cards))
        for args in [('draw', '--families', 'G'), ('draw', '--families', 'D', 'D'), ('draw', '--families', 'P', '--modules', 'expansao_5')]:
            self.assertNotEqual(self.run_helper(*args).returncode, 0)

if __name__ == '__main__':
    unittest.main()
