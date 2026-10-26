"""Verify 5.2 source/art bytes, complete PDF text and readable print layout."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from PIL import Image
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
PRINT=ROOT/'skills/persona-cards/print'

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def compact(text):return ''.join(c.casefold() for c in text if c.isalnum())

def main():
    deck_path=ROOT/'deck/persona-cards-5.2.json'
    cards=json.loads(deck_path.read_text(encoding='utf8'))['cartas']
    manifest_path=ROOT/'deck/illustration_sheets_5_2.json'
    sheets=json.loads(manifest_path.read_text(encoding='utf8'))['sheets']
    codes=[c['codigo'] for c in cards]
    mapped=[c for s in sheets for c in s['codes']]
    assert len(codes)==len(mapped)==len(set(mapped))==169 and set(codes)==set(mapped)
    assert len(sheets)==30
    for sheet in sheets:
        path=PRINT/'assets'/sheet['file']
        assert digest(path)==digest(ROOT/'app/public/art'/sheet['file']),path
        columns,rows=sheet.get('columns',3),sheet.get('rows',2)
        with Image.open(path) as image:
            assert image.mode=='RGBA' and image.width*rows==image.height*columns,path
            alpha=image.getchannel('A')
            assert alpha.getextrema()[0]==0,path
            size=image.width//columns
            for slot,code in enumerate(sheet['codes']):
                x,y=(slot%columns)*size,(slot//columns)*size
                cell=alpha.crop((x,y,x+size,y+size))
                assert sum(cell.histogram()[180:])>=1000,(code,path)
    paths={key:PRINT/f'Persona-Cards-5.2-Ilustrado-{suffix}.pdf' for key,suffix in dict(front='Frentes-A4',back='Versos-A4',duplex='Duplex-A4',manual='Manual-Rapido').items()}
    readers={key:PdfReader(str(path)) for key,path in paths.items()}
    assert {key:len(reader.pages) for key,reader in readers.items()}==dict(front=43,back=43,duplex=86,manual=3)
    text={key:[compact(p.extract_text()) for p in reader.pages] for key,reader in readers.items()}
    for key,reader in readers.items():
        for page in reader.pages:
            assert abs(float(page.mediabox.width)-595.276)<.2,key
            assert abs(float(page.mediabox.height)-841.89)<.2,key
    for index,card in enumerate(cards):
        for rendered in (text['front'][index//4],text['duplex'][2*(index//4)]):
            for value in (card['codigo'],card['titulo'],card['leitura'],*card['campos'].values()):
                assert compact(value) in rendered,(card['codigo'],value)
    manual=''.join(text['manual'])
    for marker in ['OR','CV','D','F','V','L','P','N','Chamado','Fato','Crença','Escolha','169','43','86','92 x 130']:
        assert compact(marker) in manual,marker
    report=json.loads((PRINT/'verificacao-impressao-5.2-ilustrado.json').read_text(encoding='utf8'))
    assert report['deck_sha256']==digest(deck_path)
    assert report['manifest_sha256']==digest(manifest_path)
    assert report['revisao_editorial']=='5.2.2'
    assert report['cards']==report['illustrations']==169
    assert min(f['body_pt'] for f in report['fit'])>=8.5
    assert all(f['art_pt']>=80 for f in report['fit'] if not f['code'].startswith(('G','U')))
    assert all(f['art_pt']>=44 for f in report['fit'])
    for path in paths.values():
        assert report['files'][path.name]==digest(path)
        assert path.stat().st_size<100*1024*1024,('GitHub file limit',path)
    print('PRINT_VERIFY_5_2_OK: 169 texts/artworks, 30 sheets, 43/43/86/3 A4 pages, body >=8.5pt, web/print assets identical')

if __name__=='__main__':main()
