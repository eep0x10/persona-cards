import unittest
from fastapi.testclient import TestClient
from server import app, DECK

client=TestClient(app)

class Contracts(unittest.TestCase):
    def test_52_draw_defaults_and_expansion_filters(self):
        response=client.post('/api/draw',json={})
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json()['version'],'5.2')
        self.assertEqual([c['familia'] for c in response.json()['cards']],['OR','CV','D','F','V','L','P','N'])
        expanded=client.get('/api/cards',params={'module':'expansao_5_2'}).json()
        self.assertEqual(len(expanded),24)
        self.assertEqual(client.get('/api/cards/CV04').json()['titulo'],'Não vou repetir aquele dano')
        self.assertEqual(client.get('/api/cards/G07').json()['titulo'],'Chamado e destino')
        self.assertEqual(client.post('/api/draw',json={'families':['OR','CV'],'modules':['expansao_5_2']}).status_code,200)
        excluded=[c['codigo'] for c in expanded if c['familia']=='OR']
        self.assertEqual(client.post('/api/draw',json={'families':['OR'],'excluded_codes':excluded}).status_code,400)

    def test_52_complete_creation_requires_all_eight_families_and_five_journey_answers(self):
        families=['OR','CV','D','F','V','L','P','N']
        codes=[f+'01' for f in families]
        journey={'call':'Uma coincidência no cais','response':'Escolho renegociar um turno de trabalho',
                 'fact':'Recebi uma proposta verificável','belief':'Talvez seja uma oportunidade, não uma profecia',
                 'choice':'Peço uma condição e aguardo a resposta'}
        body={'nome':'Lina','codes':codes,'journey':journey,
              'fields':{family:f'Interpretação específica de {family} para a travessia de Lina' for family in families}}
        result=client.post('/api/characters/compose',json=body)
        self.assertEqual(result.status_code,200)
        data=result.json()
        self.assertTrue(data['finalized'])
        self.assertEqual(data['version'],'5.2')
        self.assertEqual(data['journey'],journey)
        self.assertEqual(data['fields'],body['fields'])
        self.assertEqual(client.post('/api/characters/compose',json={**body,'fields':{}}).status_code,400)
        self.assertEqual(client.post('/api/characters/compose',json={**body,'nome':' '}).status_code,400)
        for family in families:
            self.assertEqual(client.post('/api/characters/compose',json={**body,'fields':{**body['fields'],family:' '}}).status_code,400,family)
        original_prompt=next(c for c in DECK['cartas'] if c['codigo']=='OR01')['campos']['Pergunte']
        self.assertEqual(client.post('/api/characters/compose',json={**body,'fields':{**body['fields'],'OR':original_prompt}}).status_code,400)
        self.assertEqual([c['familia'] for c in data['cards']],families)
        self.assertIn('G07',[g['codigo'] for g in data['guides']])
        for missing in codes:
            self.assertEqual(client.post('/api/characters/compose',json={**body,'codes':[c for c in codes if c!=missing]}).status_code,400,missing)
        for key in journey:
            self.assertEqual(client.post('/api/characters/compose',json={**body,'journey':{**journey,key:'  '}}).status_code,400,key)
        self.assertEqual(client.post('/api/characters/compose',json={'codes':codes}).status_code,400)

    def test_draft_and_both_legacy_versions_preserve_text_without_filling_history(self):
        for version in ['5.0','5.1','5.2']:
            body={'version':version,'finalized':False,'codes':['D01'],'fields':{'D':'x'*20000},
                  'papel':'Ofício preservado','contexto':'A cena anterior continua válida'}
            result=client.post('/api/characters/compose',json=body)
            self.assertEqual(result.status_code,200)
            data=result.json()
            self.assertEqual(data['version'],'5.2')
            self.assertEqual(data['source_version'],version)
            self.assertFalse(data['finalized'])
            self.assertEqual(data['fields'],body['fields'])
            self.assertEqual(data['papel'],body['papel'])
            self.assertEqual(data['contexto'],body['contexto'])
            self.assertEqual({c['codigo'] for c in data['cards']},{'D01'})
            self.assertTrue(all(value=='' for value in data['journey'].values()))
        self.assertEqual(client.post('/api/characters/compose',json={'codes':[],'finalized':False}).status_code,200)

    def test_deck_and_search(self):
        self.assertEqual(client.get('/api/deck').json(),DECK)
        self.assertEqual(len(DECK['cartas']),166)
        self.assertEqual(client.get('/api/cards/D19').json()['titulo'],'Punir quem causou o dano')
        self.assertIn('Punir e reparar',client.get('/api/cards/D19').json()['leitura'])
        self.assertEqual(client.get('/api/cards/N99').status_code,404)
        hits=client.get('/api/cards',params={'q':'obrigacao','family':'D'}).json()
        self.assertIn('D21',[c['codigo'] for c in hits])
        self.assertIn('D19',[c['codigo'] for c in client.get('/api/cards',params={'q':'punir e reparar','family':'D'}).json()])
        self.assertEqual(client.get('/api/cards',params={'family':'G'}).json().__len__(),7)
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

    def test_legacy_compose_normalizes_without_inventing_missing_layers(self):
        body={'version':'5.1','nome':'Liora','papel':'Padeira','contexto':'Uma festa local','codes':['D23','F08','V09'],'guide_codes':['G06']}
        result=client.post('/api/characters/compose',json=body)
        self.assertEqual(result.status_code,200)
        c=result.json();self.assertEqual(c['nome'],'Liora');self.assertEqual(c['contexto'],body['contexto'])
        self.assertEqual(c['version'],'5.2');self.assertEqual(c['source_version'],'5.1');self.assertFalse(c['finalized']);self.assertIn('A própria prática',c['markdown'])
        self.assertNotIn('Conflito interno',c['layers']);self.assertIn('Rascunho:',c['markdown']);self.assertNotIn('Origem',c['layers']);self.assertEqual(c['journey']['fact'],'')
        self.assertEqual(c['guides'][0]['codigo'],'G06')
        explicit=client.post('/api/characters/compose',json={'version':'5.0','codes':['D01','F01','V01','N21']}).json()
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
            self.assertEqual(result.json(),{'status':'ok','version':DECK['versao'],'cards':166})
        for host in ('example.com','sub.personcard.runictools.com','personcard.runictools.com.attacker.example'):
            self.assertEqual(client.get('/api/health',headers={'host':host}).status_code,400,host)

    def test_inspirations_catalog_and_exact_item(self):
        response=client.get('/api/inspirations')
        self.assertEqual(response.status_code,200)
        catalog=response.json()
        self.assertEqual(catalog['version'],'5.2')
        self.assertIn('não são eventos canônicos',catalog['disclaimer'])
        self.assertEqual(len(catalog['characters']),100)
        self.assertEqual(len({entry['id'] for entry in catalog['characters']}),100)
        for entry in catalog['characters']:
            self.assertIsNone(entry['character']['id'])
            self.assertTrue(entry['character']['finalized'])
            self.assertEqual(entry['character']['enabled'],['OR','CV','D','F','V','L','P','N'])
            self.assertEqual(set(entry['character']['journey']),{'call','response','fact','belief','choice'})
            self.assertTrue(all(len(text.strip())>=20 for text in entry['character']['journey'].values()))
            self.assertGreater(len(entry['journeyRationale']),35)
            self.assertEqual(set(entry['rationale']),set(entry['character']['enabled']))
            self.assertTrue(all(isinstance(text,str) and len(text)>=35 for text in entry['rationale'].values()))
            for family,code in entry['character']['cards'].items():
                self.assertEqual(next(c for c in DECK['cartas'] if c['codigo']==code)['familia'],family)
        first=catalog['characters'][0]
        self.assertEqual(client.get('/api/inspirations/'+first['id']).json(),first)
        self.assertEqual(client.get('/api/inspirations/inexistente').status_code,404)
        self.assertEqual(sum(len(entry['rationale']) for entry in catalog['characters']),800)

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
