"""Render 5.2 with the established folk layout; retain the historical renderer."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

import render_print_illustrated_5_1 as base
from render_print_5_1 import paragraph, rule, setup_fonts, build_duplex
from lossless_pdf import optimize

ROOT=Path(__file__).resolve().parents[1]
PRINT=ROOT/'skills/persona-cards/print'
DECK=ROOT/'deck/persona-cards-5.2.json'
MANIFEST=ROOT/'deck/illustration_sheets_5_2.json'
EDITION='5.2.0'
PALETTE={**base.PALETTE,'OR':('ORIGEM','#55705A'),'CV':('CONVICÇÃO','#9A573F')}
LAYOUT={}
SAFE_CROPS={**base.SAFE_CROPS,'CV02':(.04,0,0,0)}


def fit_card(card:dict,y:float)->dict:
    """Favor readable 8.5pt body text over illustration size on dense cards."""
    width=base.CARD_W-40
    title_size=16 if len(card['titulo'])<27 else 14.8
    title,title_h=paragraph(card['titulo'],'Georgia-Bold',title_size,title_size*1.16,width,TA_CENTER)
    title_top=y+base.CARD_H-38
    candidates=[]
    sizes=(128,116,104,92,80,68,56,44) if card['familia'] in ('U','G') else (128,116,104,92,80)
    for art_size in sizes:
        art_y=title_top-title_h-9-art_size
        for read_size in (9.7,9.35,9.0):
            reading,read_h=paragraph(card['leitura'],'Georgia-Italic',read_size,read_size*1.25,base.CARD_W-44,TA_CENTER)
            read_top=art_y-4
            divider=read_top-read_h-5
            for body_size in (9.0,8.7,8.5):
                cursor,blocks=divider-8,[]
                for label,value in card['campos'].items():
                    heading,head_h=paragraph(label.upper(),'Arial-Bold',7,7.8,width)
                    body,body_h=paragraph(value.replace('\n','; '),'Arial',body_size,body_size*1.24,width)
                    blocks.append((heading,head_h,body,body_h,cursor))
                    cursor-=head_h+body_h+4
                if cursor>=y+24:
                    candidates.append(dict(title=title,title_h=title_h,title_top=title_top,art_size=art_size,art_y=art_y,reading=reading,read_h=read_h,read_top=read_top,divider=divider,blocks=blocks,lowest=cursor-y,body_size=body_size,read_size=read_size))
    if not candidates:
        raise ValueError(f"Card {card['codigo']} cannot fit with a readable 8.5pt body")
    return max(candidates,key=lambda f:f['art_size']+45*(f['body_size']-8.5)+10*(f['read_size']-9))


def draw_art(canvas,code,atlas,slot,x,y,size):
    cols,rows=LAYOUT[code]
    col,row=slot%cols,slot//cols
    left,right,top,bottom=SAFE_CROPS.get(code,(0,0,0,0))
    canvas.saveState()
    clip=canvas.beginPath()
    clip.rect(x+left*size,y+bottom*size,size*(1-left-right),size*(1-top-bottom))
    canvas.clipPath(clip,stroke=0,fill=0)
    canvas.drawImage(ImageReader(str(atlas)),x-col*size,y-(rows-1-row)*size,width=cols*size,height=rows*size,mask='auto')
    canvas.restoreState()


def sheet_footer(canvas,sheet,kind):
    count=math.ceil(len(json.loads(DECK.read_text(encoding='utf8'))['cartas'])/4)
    canvas.setFillColor(base.INK)
    canvas.setFont('Arial',7)
    canvas.drawString(base.LEFT,base.PAGE_H-6*mm,f'PERSONA CARDS / ILUSTRADO {EDITION} / FOLHA {sheet:02d} DE {count}')
    canvas.drawRightString(base.PAGE_W-base.LEFT,base.PAGE_H-6*mm,kind)
    canvas.drawCentredString(base.PAGE_W/2,5*mm,'A4 / 100% / 92 x 130 mm / DUPLEX: BORDA LONGA')


def build_manual(path):
    deck=json.loads(DECK.read_text(encoding='utf8'))
    guide=next(c for c in deck['cartas'] if c['codigo']=='G07')
    pages=[('CRIAR COM OITO CARTAS',[
        ('Uma de cada família','Separe OR (Origem), CV (Convicção), D (Desejo), F (Forma de agir), V (Expressão), L (Vínculo), P (Pressão) e N (Conflito interno). Escolha ou sorteie uma de cada. Todas são obrigatórias na criação 5.2; U/G são consulta.'),
        ('Conecte passado e escolha','Diga o que aconteceu em OR e ligue à CV por “por isso”, “apesar disso” ou “mais tarde aprendi”. CV pode ser crença factual, valor ou regra prática. Origem não atribui culpa; nem toda convicção é uma mentira.'),
        ('Faça a cena existir','Concretize desejo, método e expressão. Pessoas do vínculo têm vontade própria; objetos e memórias seguem o alcance do cenário. P muda a situação; N pede dois valores reais e uma escolha em disputa. Se não cabe, reveja carta ou situação.'),
        ('Complete Chamado e destino','Use G07 e registre chamado, primeira resposta, fato confirmado, crença ou interpretação e margem de escolha. O guia completo está na página seguinte. As cinco respostas também são obrigatórias.'),
        ('Viva além do problema','Dê uma competência, um prazer cotidiano e um limite real. Sorteio não garante coerência nem exige trauma ou redenção. Depois da cena, preserve fatos e altere somente o que as escolhas mudaram.'),
    ]),('CHAMADO E DESTINO',[
        ('De onde vem? Escolha ou use 1d6',guide['campos']['Chamado'].replace('\n','; ')+'.'),
        ('Primeira resposta: escolha ou use 1d6',guide['campos']['Resposta'].replace('\n','; ')+'.'),
        ('Fato confirmado','O que está estabelecido no mundo? Uma cheia sazonal pode ser real sem que seja verdade a exigência de sacrificar alguém para detê-la. Natureza e passagem do tempo não precisam ter intenção.'),
        ('Crença e evidência','Quem interpreta o acontecimento como sinal, dever ou profecia? Separe relato, previsão e fato. Uma crença factual pode ser verdadeira, falsa, parcial ou desconhecida; um valor não é um fato a refutar.'),
        ('Escolha e consequência','Diga a primeira ação e o que ela preserva. Recusar não equivale a covardia, aceitar não garante bondade. O dado sugere a postura inicial; não decide o futuro nem a ação de jogadores. Preserve o que ainda pode ser escolhido.'),
    ]),('IMPRIMIR E CORTAR',[
        ('Formato','A4 retrato, quatro cartas por folha, 92 x 130 mm por carta. São 166 cartas, 42 folhas de frentes, 42 de versos e 84 páginas duplex alternadas. A última folha tem duas cartas e dois espaços vazios.'),
        ('Duplex automático','Imprima em tamanho real / 100%, virando na borda longa. Desative ajuste à página e livreto. Teste primeiro as páginas 1 e 2; confira tamanho, alinhamento e orientação antes do lote.'),
        ('Frentes e versos separados','Combine folhas com o mesmo número. Os versos já espelham as colunas. A reinserção manual depende da impressora: marque topo e face na folha de teste.'),
        ('Acabamento','Corte pelas marcas externas. Há 1 mm de sangria e espaço de 8–9 mm entre cartas. Use papel fosco de 180–250 g/m² somente se sua impressora aceitar. Confira a régua de escala.'),
        ('Limites da conferência','Conteúdo, páginas, encaixe e artes são conferidos digitalmente. Prova física e uso com jogadores ainda precisam ser observados. Documentos e partidas da 5.0/5.1 continuam históricos; novas criações completas seguem a regra 5.2.'),
    ])]
    canvas=Canvas(str(path),pagesize=A4,pageCompression=1)
    for number,(heading,sections) in enumerate(pages,1):
        canvas.setFillColor(base.PAPER);canvas.rect(0,0,base.PAGE_W,base.PAGE_H,stroke=0,fill=1)
        canvas.setFillColor(base.BACK);canvas.rect(0,base.PAGE_H-38*mm,base.PAGE_W,38*mm,stroke=0,fill=1)
        canvas.setFillColor(base.BACK_CREAM);canvas.setFont('Arial-Bold',9)
        canvas.drawString(23*mm,base.PAGE_H-19*mm,f'PERSONA CARDS / EDIÇÃO ILUSTRADA {EDITION}')
        canvas.setFont('Georgia-Bold',22);canvas.drawString(23*mm,base.PAGE_H-31*mm,heading)
        cursor=base.PAGE_H-53*mm
        for title,text in sections:
            canvas.setFillColor(base.BACK_RED);canvas.setFont('Georgia-Bold',13)
            canvas.drawString(23*mm,cursor,title);cursor-=6*mm
            p,h=paragraph(text,'Arial',10,14,base.PAGE_W-46*mm)
            p.drawOn(canvas,23*mm,cursor-h);cursor-=h+8*mm
        if number==3:
            ruler_y=38*mm
            rule(canvas,23*mm,ruler_y,123*mm,base.BACK,1.2)
            for i in (0,25,50,75,100):
                xx=(23+i)*mm;canvas.line(xx,ruler_y-2*mm,xx,ruler_y+2*mm)
            canvas.setFont('Arial',8);canvas.setFillColor(base.INK)
            canvas.drawString(23*mm,ruler_y-6*mm,'Régua de 100 mm para conferir a escala')
        if cursor<(47*mm if number==3 else 29*mm):
            raise ValueError(f'Manual page {number} overflow')
        rule(canvas,23*mm,24*mm,base.PAGE_W-23*mm,base.BACK)
        canvas.setFont('Arial',8);canvas.setFillColor(base.INK)
        canvas.drawString(23*mm,18*mm,'166 cartas / 150 de criação + 16 guias')
        canvas.drawRightString(base.PAGE_W-23*mm,18*mm,f'{number:02d} / 03')
        canvas.showPage()
    canvas.save()


def main():
    setup_fonts()
    cards=json.loads(DECK.read_text(encoding='utf8'))['cartas']
    sheets=json.loads(MANIFEST.read_text(encoding='utf8'))['sheets']
    base.ART.clear();LAYOUT.clear()
    for sheet in sheets:
        cols,rows=sheet.get('columns',3),sheet.get('rows',2)
        if len(sheet['codes'])>cols*rows:raise ValueError('Atlas capacity exceeded')
        for slot,code in enumerate(sheet['codes']):
            if code in base.ART:raise ValueError(f'Duplicate artwork {code}')
            base.ART[code]=(base.ASSETS/sheet['file'],slot);LAYOUT[code]=(cols,rows)
    if set(base.ART)!={c['codigo'] for c in cards}:raise ValueError('Artwork coverage differs from deck')
    # Reuse the established sheet/back geometry without changing its source.
    base.EDITION=EDITION;base.PALETTE=PALETTE
    base.fit_card=fit_card;base.draw_art=draw_art;base.sheet_footer=sheet_footer
    front=PRINT/'Persona-Cards-5.2-Ilustrado-Frentes-A4.pdf'
    back=PRINT/'Persona-Cards-5.2-Ilustrado-Versos-A4.pdf'
    duplex=PRINT/'Persona-Cards-5.2-Ilustrado-Duplex-A4.pdf'
    manual=PRINT/'Persona-Cards-5.2-Ilustrado-Manual-Rapido.pdf'
    fit=base.build_sheets(cards,front)
    base.build_sheets(cards,back,backs=True)
    compression={front.name:optimize(front),back.name:optimize(back)}
    build_duplex(front,back,duplex)
    build_manual(manual)
    report=dict(revisao_editorial=EDITION,deck_sha256=hashlib.sha256(DECK.read_bytes()).hexdigest(),
                manifest_sha256=hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),cards=len(cards),
                illustrations=len(base.ART),spritesheets=len(sheets),size_mm=[92,130],sheets=math.ceil(len(cards)/4),fit=fit,
                lossless_encoding=compression,
                files={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (front,back,duplex,manual)})
    (PRINT/'verificacao-impressao-5.2-ilustrado.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f"PRINT_5_2_OK {len(cards)} cards, {len(sheets)} sheets; min body {min(f['body_pt'] for f in fit)}pt")


if __name__=='__main__':main()
