"""Local Persona Cards API; personal drafts stay in the browser."""
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
Family=Literal['D','F','N','L','V','P']
Module=Literal['nucleo','expansao','expansao_5']

class Card(BaseModel):
    versao:str
    codigo:str
    titulo:str
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
    version:Literal['5.0']='5.0'
    cards:list[Card]

class ComposeRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    nome:str=Field(default='Sem nome',max_length=120)
    papel:str=Field(default='',max_length=300)
    contexto:str=Field(default='',max_length=4000)
    codes:list[str]=Field(min_length=3,max_length=6)
    guide_codes:list[str]=Field(default_factory=list,max_length=15)

class Character(BaseModel):
    version:Literal['5.0']='5.0'
    nome:str
    papel:str
    contexto:str
    cards:list[Card]
    guides:list[Card]
    layers:dict[str,str]
    markdown:str

app=FastAPI(title='Persona Cards — protótipo local',version='5.0',
            docs_url='/api/docs',redoc_url=None,openapi_url='/api/openapi.json',
            description='Explore as cartas, sorteie combinações e componha fichas a partir de prompts. '
            'Operações sem estado e sem geração por IA. Personagens salvos e rascunhos pertencem ao navegador, '
            'não são armazenados ou acessíveis por esta API. Serviço local, sem contas; inicialização em 127.0.0.1.')
app.add_middleware(TrustedHostMiddleware,allowed_hosts=['127.0.0.1','localhost','testserver'])

def normalize(text:str)->str:
    return ''.join(c for c in unicodedata.normalize('NFKD',text.casefold()) if not unicodedata.combining(c))

def known(codes:list[str])->list[dict]:
    unknown=[c for c in codes if c not in BY_CODE]
    if unknown:raise HTTPException(400,detail={'message':'Códigos inexistentes','codes':unknown})
    return [BY_CODE[c] for c in codes]

@app.get('/api/health',tags=['Serviço'])
def health():
    return {'status':'ok','version':'5.0','cards':len(BY_CODE)}

@app.get('/api/deck',response_model=Deck,tags=['Cartas'])
def get_deck():
    return DECK

@app.get('/api/cards',response_model=list[Card],tags=['Cartas'])
def list_cards(q:str=Query(default='',max_length=300),
               family:Literal['D','F','N','L','V','P','U','G']|None=None,
               module:Literal['nucleo','expansao','expansao_5','guia','guia_contexto']|None=None):
    query=normalize(q)
    return [c for c in DECK['cartas']
            if (not family or c['familia']==family) and (not module or c['modulo']==module)
            and (not query or query in normalize(' '.join([c['codigo'],c['titulo'],*c['campos'].values()])))]

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
    return {'version':'5.0','cards':drawn}

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
    md=[f'# {name}','',request.papel.strip(),request.contexto.strip(),'','Persona Cards 5.0 · prompts para completar, sem geração por IA.','']
    for c in selected:
        md += [f"## {labels[c['familia']]} — {c['codigo']} · {c['titulo']}"]
        md += [f'**{label}:** {text}' for label,text in c['campos'].items()]
        md.append('')
    if 'N' not in families:md += ['Conflito interno não definido. Não inventar dois valores para preencher uma camada.','']
    if guides:
        md += ['## Guias de consulta']
        for g in guides:md.append(f"- {g['codigo']} · {g['titulo']}")
    return {'version':'5.0','nome':name,'papel':request.papel,'contexto':request.contexto,
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
