"""Stateless Persona Cards API; personal drafts stay in the browser."""
from pathlib import Path
from typing import Literal
import json
import secrets
import unicodedata

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, Field
from starlette.middleware.trustedhost import TrustedHostMiddleware

HERE=Path(__file__).resolve().parent
DECK_PATH=HERE/'public/deck.json'
DECK=json.loads(DECK_PATH.read_text(encoding='utf-8'))
BY_CODE={c['codigo']:c for c in DECK['cartas']}
INSPIRATIONS=json.loads((HERE/'public/inspirations.json').read_text(encoding='utf-8'))
INSPIRATIONS_BY_ID={c['id']:c for c in INSPIRATIONS['characters']}
Family=Literal['D','F','N','L','V','P']
Module=Literal['nucleo','expansao','expansao_5']
Medium=Literal['Anime','Cinema','Animação','Quadrinhos','Séries','Jogos']
Archetype=Literal['Herói','Vilão','Ambíguo','Coadjuvante']

class InspirationSource(BaseModel):
    label:str
    url:str

class InspirationAudit(BaseModel):
    fit:Literal['direto','adaptado']
    note:str
    gapTags:list[str]

class InspirationTemplate(BaseModel):
    id:str|None
    name:str
    role:str
    context:str
    cards:dict[Family,str]
    fields:dict[Family,str]
    locks:list[Family]
    enabled:list[Family]
    notes:str
    portrait:Literal['']
    finalized:bool

class Inspiration(BaseModel):
    id:str
    name:str
    franchise:str
    medium:Medium
    archetype:Archetype
    excerpt:str
    sources:list[InspirationSource]
    character:InspirationTemplate
    audit:InspirationAudit
    rationale:dict[Family,str]

class InspirationCatalog(BaseModel):
    version:Literal['5.1']
    disclaimer:str
    characters:list[Inspiration]

class Card(BaseModel):
    versao:str
    codigo:str
    titulo:str
    leitura:str
    familia:Literal['D','F','N','L','V','P','U','G']
    campos:dict[str,str]
    modulo:Literal['nucleo','expansao','expansao_5','guia','guia_contexto']

class Deck(BaseModel):
    model_config=ConfigDict(extra='allow')
    nome:str
    versao:str
    cartas:list[Card]
    modulos:dict[str,int]

class DrawRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    families:list[Family]=Field(default_factory=lambda:['D','F','V'],min_length=1,max_length=6)
    modules:list[Module]=Field(default_factory=lambda:['nucleo','expansao','expansao_5'],min_length=1,max_length=3)
    excluded_codes:list[str]=Field(default_factory=list,max_length=126)

class DrawResponse(BaseModel):
    version:Literal['5.1']='5.1'
    cards:list[Card]

class ComposeRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    nome:str=Field(default='Sem nome',max_length=120)
    papel:str=Field(default='',max_length=300)
    contexto:str=Field(default='',max_length=4000)
    codes:list[str]=Field(min_length=3,max_length=6)
    guide_codes:list[str]=Field(default_factory=list,max_length=15)

class Character(BaseModel):
    version:Literal['5.1']='5.1'
    nome:str
    papel:str
    contexto:str
    cards:list[Card]
    guides:list[Card]
    layers:dict[str,str]
    markdown:str

app=FastAPI(title='Persona Cards — API pública sem contas',version=DECK['versao'],
            docs_url='/api/docs',redoc_url=None,openapi_url='/api/openapi.json',
            description='Explore as cartas, sorteie combinações e componha fichas a partir de prompts. '
            'Operações sem estado e sem geração por IA. Personagens salvos e rascunhos pertencem ao navegador, '
            'não são armazenados ou acessíveis por esta API. Acesso público sem contas ou autenticação; '
            'composição devolve o resultado sem salvar dados no servidor.')
app.add_middleware(TrustedHostMiddleware,
                   allowed_hosts=['personcard.runictools.com','127.0.0.1','localhost','testserver'])

def normalize(text:str)->str:
    return ''.join(c for c in unicodedata.normalize('NFKD',text.casefold()) if not unicodedata.combining(c))

def known(codes:list[str])->list[dict]:
    unknown=[c for c in codes if c not in BY_CODE]
    if unknown:raise HTTPException(400,detail={'message':'Códigos inexistentes','codes':unknown})
    return [BY_CODE[c] for c in codes]

@app.get('/api/health',tags=['Serviço'])
def health():
    return {'status':'ok','version':DECK['versao'],'cards':len(BY_CODE)}

@app.get('/api/deck',response_model=Deck,tags=['Cartas'])
def get_deck():
    return DECK

@app.get('/api/inspirations',response_model=InspirationCatalog,tags=['Inspirações'],
         summary='Consulta leituras autorais de personagens; não acessa fichas do navegador')
def list_inspirations(q:str=Query(default='',max_length=300),
                      medium:Medium|None=None,archetype:Archetype|None=None):
    query=normalize(q)
    characters=[entry for entry in INSPIRATIONS['characters']
                if (not medium or entry['medium']==medium)
                and (not archetype or entry['archetype']==archetype)
                and (not query or query in normalize(' '.join([
                    entry['name'],entry['franchise'],entry['excerpt'],entry['character']['role']])))]
    return {'version':INSPIRATIONS['version'],'disclaimer':INSPIRATIONS['disclaimer'],
            'characters':characters}

@app.get('/api/inspirations/{inspiration_id}',response_model=Inspiration,tags=['Inspirações'],
         responses={404:{'description':'Inspiração não encontrada'}})
def get_inspiration(inspiration_id:str):
    if inspiration_id not in INSPIRATIONS_BY_ID:
        raise HTTPException(404,'Inspiração não encontrada')
    return INSPIRATIONS_BY_ID[inspiration_id]

@app.get('/api/cards',response_model=list[Card],tags=['Cartas'])
def list_cards(q:str=Query(default='',max_length=300),
               family:Literal['D','F','N','L','V','P','U','G']|None=None,
               module:Literal['nucleo','expansao','expansao_5','guia','guia_contexto']|None=None):
    query=normalize(q)
    return [c for c in DECK['cartas']
            if (not family or c['familia']==family) and (not module or c['modulo']==module)
            and (not query or query in normalize(' '.join([c['codigo'],c['titulo'],c['leitura'],*c['campos'].values()])))]

@app.get('/api/cards/{code}',response_model=Card,tags=['Cartas'])
def get_card(code:str):
    if code not in BY_CODE:raise HTTPException(404,'Carta não encontrada')
    return BY_CODE[code]

@app.post('/api/draw',response_model=DrawResponse,tags=['Criação'],
          responses={400:{'description':'Família repetida, código desconhecido ou família sem carta disponível'}})
def draw(request:DrawRequest):
    if len(set(request.families))!=len(request.families):raise HTTPException(400,'Escolha cada família uma única vez')
    known(request.excluded_codes)
    excluded=set(request.excluded_codes)
    drawn=[]
    for family in request.families:
        pool=[c for c in DECK['cartas'] if c['familia']==family and c['modulo'] in request.modules and c['codigo'] not in excluded]
        if not pool:raise HTTPException(400,f'Nenhuma carta disponível na família {family}')
        drawn.append(secrets.choice(pool))
    return {'version':DECK['versao'],'cards':drawn}

@app.post('/api/characters/compose',response_model=Character,tags=['Criação'],
          responses={400:{'description':'Códigos inválidos, família repetida, guia como personalidade ou ausência de D/F/V'}})
def compose(request:ComposeRequest):
    selected=known(request.codes);guides=known(request.guide_codes)
    families=[c['familia'] for c in selected]
    if any(f not in 'DFNLVP' for f in families):raise HTTPException(400,'U/G são consulta, não camadas da personalidade')
    if len(set(families))!=len(families):raise HTTPException(400,'Use uma carta por família')
    if not set('DFV').issubset(families):raise HTTPException(400,'A ficha rápida precisa de D, F e V')
    if any(g['familia'] not in ('U','G') for g in guides):raise HTTPException(400,'Consulta aceita apenas U/G')
    if len(set(request.guide_codes))!=len(guides):raise HTTPException(400,'Não repita guias')
    labels={'D':'Objetivo','F':'Método','V':'Expressão','L':'Vínculo','P':'Pressão','N':'Conflito interno'}
    selected.sort(key=lambda c:'DFVLPN'.index(c['familia']))
    layers={labels[c['familia']]:next(iter(c['campos'].values())) for c in selected}
    name=request.nome.strip() or 'Sem nome'
    md=[f'# {name}','',request.papel.strip(),request.contexto.strip(),'','Persona Cards 5.1 · prompts para completar, sem geração por IA.','']
    for c in selected:
        md += [f"## {labels[c['familia']]} — {c['codigo']} · {c['titulo']}"]
        md += [c['leitura'], '']
        md += [f'**{label}:** {text}' for label,text in c['campos'].items()]
        md.append('')
    if 'N' not in families:md += ['Conflito interno não definido. Não inventar dois valores para preencher uma camada.','']
    if guides:
        md += ['## Guias de consulta']
        for g in guides:md.append(f"- {g['codigo']} · {g['titulo']}")
    return {'version':DECK['versao'],'nome':name,'papel':request.papel,'contexto':request.contexto,
            'cards':selected,'guides':guides,'layers':layers,'markdown':'\n'.join(md)}

@app.get('/{path:path}',include_in_schema=False)
def frontend(path:str):
    if path.startswith('api/'):raise HTTPException(404,'Operação inexistente')
    root=HERE/'dist'
    if path=='exploracoes.html' and not (root/path).is_file():
        return FileResponse(HERE/'public/exploracoes.html')
    target=(root/(path or 'index.html')).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise HTTPException(404 if path else 503,'Interface em preparação' if not path else 'Arquivo não encontrado')
    return FileResponse(target)
