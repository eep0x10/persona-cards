import unittest
from fastapi.testclient import TestClient
from server import app, DECK

client=TestClient(app)

class Contracts(unittest.TestCase):
    def test_deck_and_search(self):
        self.assertEqual(client.get('/api/deck').json(),DECK)
        self.assertEqual(len(DECK['cartas']),141)
        self.assertEqual(client.get('/api/cards/D19').json()['titulo'],'Punir quem causou o dano')
        self.assertIn('Punir e reparar',client.get('/api/cards/D19').json()['leitura'])
        self.assertEqual(client.get('/api/cards/N99').status_code,404)
        hits=client.get('/api/cards',params={'q':'obrigacao','family':'D'}).json()
        self.assertIn('D21',[c['codigo'] for c in hits])
        self.assertIn('D19',[c['codigo'] for c in client.get('/api/cards',params={'q':'punir e reparar','family':'D'}).json()])
        self.assertEqual(client.get('/api/cards',params={'family':'G'}).json().__len__(),6)
        self.assertEqual(client.get('/api/cards',params={'q':'inexistente987'}).json(),[])

    def test_random_filters_exclusions_and_errors(self):
        remaining=[c['codigo'] for c in DECK['cartas'] if c['familia']=='D' and c['codigo']!='D01']
        result=client.post('/api/draw',json={'families':['D'],'modules':['nucleo'],'excluded_codes':remaining})
        self.assertEqual(result.status_code,200)
        self.assertEqual(result.json()['cards'][0]['codigo'],'D01')
        for family in 'DFNLVP':
            drawn=client.post('/api/draw',json={'families':[family],'modules':['nucleo']}).json()['cards'][0]
            self.assertEqual(drawn['familia'],family);self.assertEqual(drawn['modulo'],'nucleo')
        self.assertEqual(client.post('/api/draw',json={'families':['G']}).status_code,422)
        self.assertEqual(client.post('/api/draw',json={'families':['D','D']}).status_code,400)
        self.assertEqual(client.post('/api/draw',json={'families':['D'],'modules':[]}).status_code,422)
        all_d=[c['codigo'] for c in DECK['cartas'] if c['familia']=='D']
        self.assertEqual(client.post('/api/draw',json={'families':['D'],'excluded_codes':all_d}).status_code,400)
        self.assertEqual(client.post('/api/draw',json={'excluded_codes':['D99']}).status_code,400)

    def test_compose_preserves_inputs_and_optional_conflict(self):
        body={'nome':'Liora','papel':'Padeira','contexto':'Uma festa local','codes':['D23','F08','V09'],'guide_codes':['G06']}
        result=client.post('/api/characters/compose',json=body)
        self.assertEqual(result.status_code,200)
        c=result.json();self.assertEqual(c['nome'],'Liora');self.assertEqual(c['contexto'],body['contexto'])
        self.assertEqual(c['version'],'5.1');self.assertIn('A própria prática',c['markdown'])
        self.assertNotIn('Conflito interno',c['layers']);self.assertIn('Conflito interno não definido',c['markdown'])
        self.assertEqual(c['guides'][0]['codigo'],'G06')
        explicit=client.post('/api/characters/compose',json={'codes':['D01','F01','V01','N21']}).json()
        self.assertIn('Conflito interno',explicit['layers'])
        for codes in (['D01','D02','V01'],['D01','F01','G01'],['D01','F01','V99']):
            self.assertEqual(client.post('/api/characters/compose',json={'codes':codes}).status_code,400)
        self.assertEqual(client.post('/api/characters/compose',json={'codes':['D01','F01','V01'],'guide_codes':['D02']}).status_code,400)

    def test_openapi_exposes_product_operations(self):
        schema=client.get('/api/openapi.json').json()
        self.assertEqual(schema['info']['version'],DECK['versao'])
        self.assertIn('pública sem contas',schema['info']['title'])
        self.assertIn('/api/characters/compose',schema['paths'])
        self.assertIn('/api/draw',schema['paths'])
        self.assertEqual(client.get('/api/docs').status_code,200)
        self.assertEqual(client.get('/api/nonexistent').status_code,404)

    def test_public_host_is_exact_and_local_health_remains_available(self):
        for host in ('personcard.runictools.com','127.0.0.1','localhost','testserver'):
            result=client.get('/api/health',headers={'host':host})
            self.assertEqual(result.status_code,200,host)
            self.assertEqual(result.json(),{'status':'ok','version':DECK['versao'],'cards':141})
        for host in ('example.com','sub.personcard.runictools.com','personcard.runictools.com.attacker.example'):
            self.assertEqual(client.get('/api/health',headers={'host':host}).status_code,400,host)

    def test_inspirations_catalog_and_exact_item(self):
        response=client.get('/api/inspirations')
        self.assertEqual(response.status_code,200)
        catalog=response.json()
        self.assertEqual(catalog['version'],'5.1')
        self.assertIn('não são eventos canônicos',catalog['disclaimer'])
        self.assertEqual(len(catalog['characters']),100)
        self.assertEqual(len({entry['id'] for entry in catalog['characters']}),100)
        for entry in catalog['characters']:
            self.assertIsNone(entry['character']['id'])
            self.assertTrue(entry['character']['finalized'])
            self.assertEqual(set(entry['rationale']),set(entry['character']['enabled']))
            self.assertTrue(all(isinstance(text,str) and len(text)>=35 for text in entry['rationale'].values()))
            for family,code in entry['character']['cards'].items():
                self.assertEqual(next(c for c in DECK['cartas'] if c['codigo']==code)['familia'],family)
        first=catalog['characters'][0]
        self.assertEqual(client.get('/api/inspirations/'+first['id']).json(),first)
        self.assertEqual(client.get('/api/inspirations/inexistente').status_code,404)
        self.assertEqual(sum(len(entry['rationale']) for entry in catalog['characters']),353)

    def test_inspirations_combined_filters_and_read_only_contract(self):
        found=client.get('/api/inspirations',params={'q':'hermione','medium':'Cinema','archetype':'Herói'}).json()['characters']
        self.assertEqual([entry['name'] for entry in found],['Hermione Granger'])
        accented=client.get('/api/inspirations',params={'q':'aneis'}).json()['characters']
        self.assertEqual(len(accented),4)
        self.assertEqual(client.get('/api/inspirations',params={'q':'zzzinexistente'}).json()['characters'],[])
        for params in ({'medium':'Podcast'},{'archetype':'Deus'},{'q':'x'*301}):
            self.assertEqual(client.get('/api/inspirations',params=params).status_code,422)
        self.assertEqual(client.post('/api/inspirations',json={'name':'Dado privado'}).status_code,405)
        schema=client.get('/api/openapi.json').json()
        self.assertEqual(set(schema['paths']['/api/inspirations']),{'get'})

if __name__=='__main__':unittest.main(verbosity=2)
