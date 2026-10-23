"""Build the complete individually illustrated Persona Cards 5.1 A4 set."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from render_print_5_1 import (
    INK, PALETTE, PAPER, build_duplex, paragraph, rule, setup_fonts,
)


ROOT = Path(__file__).resolve().parents[1]
PRINT = ROOT / "skills/persona-cards/print"
DECK = ROOT / "deck/persona-cards-5.1.json"
MANIFEST = ROOT / "deck/illustration_sheets_5_1.json"
ASSETS = PRINT / "assets"
BACK_ART = ASSETS / "folk-verso-botanico.png"
PAGE_W, PAGE_H = A4
CARD_W, CARD_H = 92 * mm, 130 * mm
GAP_X, GAP_Y = 8 * mm, 9 * mm
LEFT = (PAGE_W - 2 * CARD_W - GAP_X) / 2
BOTTOM = (PAGE_H - 2 * CARD_H - GAP_Y) / 2
ART: dict[str, tuple[Path, int]] = {}
# A few generated cells touch a neighboring cell's art at the atlas gutter.
# Clip only those cells inside their own transparent padding.
SAFE_CROPS = {"N04": (0.0, 0.0, 0.12, 0.0),
              "U02": (0.09, 0.0, 0.11, 0.0),
              "G02": (0.09, 0.09, 0.13, 0.0)}
BACK = colors.HexColor("#173D33")
BACK_RED = colors.HexColor("#C75A3E")
BACK_CREAM = colors.HexColor("#F5EBDD")


def load_art(cards: list[dict]) -> None:
    ART.clear()
    for sheet in json.loads(MANIFEST.read_text(encoding="utf-8"))["sheets"]:
        path = ASSETS / sheet["file"]
        if not path.is_file() or len(sheet["codes"]) > 6:
            raise ValueError(f"Invalid illustration sheet: {path}")
        for slot, code in enumerate(sheet["codes"]):
            if code in ART:
                raise ValueError(f"Duplicate illustration: {code}")
            ART[code] = path, slot
    codes = {card["codigo"] for card in cards}
    if set(ART) != codes:
        raise ValueError(f"Illustrations: missing {sorted(codes-set(ART))}; extra {sorted(set(ART)-codes)}")


def draw_art(canvas: Canvas, code: str, atlas: Path, slot: int,
             x: float, y: float, size: float) -> None:
    col, row = slot % 3, slot // 3
    left, right, top, bottom = SAFE_CROPS.get(code, (0, 0, 0, 0))
    canvas.saveState()
    clip = canvas.beginPath()
    clip.rect(x+left*size, y+bottom*size,
              size*(1-left-right), size*(1-top-bottom))
    canvas.clipPath(clip, stroke=0, fill=0)
    canvas.drawImage(ImageReader(str(atlas)), x - col * size, y - (1 - row) * size,
                     width=3 * size, height=2 * size, mask="auto")
    canvas.restoreState()


def fit_card(card: dict, y: float) -> dict:
    card_w, card_h = CARD_W, CARD_H
    width = card_w - 40
    title_size = 16 if len(card["titulo"]) < 27 else 14.8
    title, title_h = paragraph(card["titulo"], "Georgia-Bold", title_size,
                                    title_size * 1.16, width, TA_CENTER)
    title_top = y + card_h - 38
    candidates = []
    for art_size in (128, 116, 104, 92, 80):
        art_y = title_top - title_h - 12 - art_size
        for read_size in (9.7, 9.35, 9.0):
            reading, read_h = paragraph(card["leitura"], "Georgia-Italic",
                                             read_size, read_size * 1.28, card_w - 44, TA_CENTER)
            read_top = art_y - 6
            divider = read_top - read_h - 7
            for body_size in (8.5, 8.2, 7.9, 7.6, 7.3):
                cursor, blocks = divider - 10, []
                for label, value in card["campos"].items():
                    heading, head_h = paragraph(label.upper(), "Arial-Bold", 7, 8.3, width)
                    body, body_h = paragraph(value, "Arial", body_size,
                                                  body_size * 1.29, width)
                    blocks.append((heading, head_h, body, body_h, cursor))
                    cursor -= head_h + body_h + 6
                if cursor >= y + 24:
                    candidates.append(dict(title=title, title_h=title_h, title_top=title_top,
                                art_size=art_size, art_y=art_y, reading=reading,
                                read_h=read_h, read_top=read_top, divider=divider,
                                blocks=blocks, lowest=cursor-y, body_size=body_size,
                                read_size=read_size))
    if candidates:
        return max(candidates, key=lambda f: f["art_size"]
                   + 50*(f["body_size"]-7.3) + 10*(f["read_size"]-9.0))
    raise ValueError(f"Card {card['codigo']} does not fit at 92 x 130 mm")


def draw_front(canvas: Canvas, card: dict, x: float, y: float) -> dict:
    label, hex_color = PALETTE[card["familia"]]
    accent = colors.HexColor(hex_color)
    fit = fit_card(card, y)
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(x - mm, y - mm, CARD_W + 2*mm, CARD_H + 2*mm,
                stroke=0, fill=1)
    canvas.setFillColor(accent)
    canvas.rect(x+17, y+CARD_H-10, CARD_W-34, 1.8, stroke=0, fill=1)
    canvas.setFont("Arial-Bold", 7.8)
    canvas.drawString(x+17, y+CARD_H-21, label)
    canvas.drawRightString(x+CARD_W-17, y+CARD_H-21, card["codigo"])
    rule(canvas, x+17, y+CARD_H-29, x+CARD_W-17, INK, 0.5)
    fit["title"].drawOn(canvas, x+20, fit["title_top"]-fit["title_h"])
    art_x = x+(CARD_W-fit["art_size"])/2
    atlas, slot = ART[card["codigo"]]
    draw_art(canvas, card["codigo"], atlas, slot, art_x, fit["art_y"], fit["art_size"])
    fit["reading"].drawOn(canvas, x+22, fit["read_top"]-fit["read_h"])
    rule(canvas, x+28, fit["divider"], x+CARD_W-28, accent, 0.7)
    for heading, head_h, body, body_h, top in fit["blocks"]:
        heading.drawOn(canvas, x+20, top-head_h)
        body.drawOn(canvas, x+20, top-head_h-body_h-1)
    rule(canvas, x+16, y+18, x+CARD_W-16, accent, 0.45)
    canvas.setFont("Arial", 6.5)
    canvas.setFillColor(INK)
    canvas.drawString(x+17, y+9, "PERSONA CARDS  /  EDIÇÃO ILUSTRADA")
    canvas.drawRightString(x+CARD_W-17, y+9, card["codigo"])
    canvas.restoreState()
    return dict(code=card["codigo"], art_pt=fit["art_size"],
                body_pt=fit["body_size"], reading_pt=fit["read_size"],
                lowest_pt=round(fit["lowest"], 2), atlas=atlas.name, slot=slot)


def draw_back(canvas: Canvas, x: float, y: float) -> None:
    canvas.saveState()
    canvas.setFillColor(BACK)
    canvas.rect(x-mm, y-mm, CARD_W+2*mm, CARD_H+2*mm,
                stroke=0, fill=1)
    cx, cy = x+CARD_W/2, y+CARD_H/2
    for angle in (0, 180):
        canvas.saveState()
        canvas.translate(cx, cy)
        canvas.rotate(angle)
        canvas.drawImage(ImageReader(str(BACK_ART)), -62, 38, width=124, height=124,
                         mask="auto")
        canvas.restoreState()
    canvas.setFillColor(BACK_CREAM)
    canvas.setFont("Georgia-Bold", 13.5)
    canvas.drawCentredString(cx, cy+2, "PERSONA CARDS")
    rule(canvas, cx-62, cy-10, cx+62, BACK_RED, 1.1)
    canvas.setFont("Georgia-Italic", 8)
    canvas.drawCentredString(cx, cy-24, "Personagens vivos · escolhas reais")
    canvas.restoreState()


def sheet_footer(canvas: Canvas, sheet: int, kind: str) -> None:
    canvas.setFillColor(INK)
    canvas.setFont("Arial", 7)
    canvas.drawString(LEFT, PAGE_H-6*mm,
                      f"PERSONA CARDS / ILUSTRADO 5.1 / FOLHA {sheet:02d} DE 36")
    canvas.drawRightString(PAGE_W-LEFT, PAGE_H-6*mm, kind)
    canvas.drawCentredString(PAGE_W/2, 5*mm,
                            "A4 / 100% / 92 x 130 mm / DUPLEX: BORDA LONGA")


def build_manual(path: Path) -> None:
    """A compact two-page guide with a scale ruler and correct illustrated size."""
    pages = [
        ("LER E CRIAR", [
            ("Comece com três cartas", "Separe D (Desejo), F (Forma de agir) e V (Expressão). Leia a abertura de cada uma em voz alta. Complete as referências entre colchetes com pessoas e situações da campanha."),
            ("Transforme em cena", "Diga o que a pessoa quer agora, o que faz para tentar e como se expressa. Mostre uma resposta possível à recusa, sem decidir a ação do interlocutor."),
            ("Aprofunde quando ajudar", "L traz um vínculo com vontade própria; P muda a circunstância. Use N apenas se o personagem valorizar de fato os dois lados do conflito. U e G são guias de consulta e ficam fora do sorteio de personalidade."),
            ("Deixe espaço para a vida", "Acrescente um prazer cotidiano, uma competência, um limite e uma relação que exista além do problema. Cartas são propostas narrativas, não diagnósticos nem destinos."),
            ("Depois da escolha", "Anote a ação e a consequência observada. Na próxima cena, preserve os fatos estabelecidos e mude apenas o que a história alterou."),
        ]),
        ("IMPRIMIR E CORTAR", [
            ("Formato", "A4 retrato; quatro cartas por folha; cada carta mede 92 x 130 mm. São 36 folhas, ou 72 páginas duplex alternadas. A última folha tem uma carta e três espaços vazios."),
            ("Duplex automático", "Imprima o arquivo Duplex em tamanho real / 100%, virando na borda longa. Desative ajuste à página e livreto. Teste somente as páginas 1 e 2 antes do lote."),
            ("Frentes e versos separados", "Combine a folha de frente e a folha de verso com o mesmo número. Os versos já espelham as colunas. A reinserção manual depende da impressora: marque topo e face em uma folha de teste."),
            ("Acabamento", "Corte nas marcas externas. Há 1 mm de sangria e 8-9 mm de distância entre cartas. Papel fosco de 180-250 g/m² serve somente se a impressora aceitar. Confira alinhamento e tamanho com régua."),
            ("Alcance da validação", "Arquivos, textos, páginas, encaixe e alinhamento foram verificados digitalmente. Uma prova física de impressão e leitura em mesa ainda deve ser feita antes de produção em lote."),
        ]),
    ]
    canvas = Canvas(str(path), pagesize=A4)
    for number, (heading, sections) in enumerate(pages, 1):
        canvas.setFillColor(PAPER)
        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        canvas.setFillColor(BACK)
        canvas.rect(0, PAGE_H-38*mm, PAGE_W, 38*mm, stroke=0, fill=1)
        canvas.setFillColor(BACK_CREAM)
        canvas.setFont("Arial-Bold", 9)
        canvas.drawString(23*mm, PAGE_H-19*mm, "PERSONA CARDS / EDIÇÃO ILUSTRADA 5.1")
        canvas.setFont("Georgia-Bold", 24)
        canvas.drawString(23*mm, PAGE_H-31*mm, heading)
        cursor = PAGE_H-55*mm
        for title, body in sections:
            canvas.setFillColor(BACK_RED)
            canvas.setFont("Georgia-Bold", 14)
            canvas.drawString(23*mm, cursor, title)
            cursor -= 7*mm
            p, h = paragraph(body, "Arial", 10.5, 15, PAGE_W-46*mm)
            p.drawOn(canvas, 23*mm, cursor-h)
            cursor -= h+12*mm
        if number == 2:
            line_y = 40*mm
            rule(canvas, 23*mm, line_y, 123*mm, BACK, 1.2)
            for i in (0, 25, 50, 75, 100):
                xx = (23+i)*mm
                canvas.line(xx, line_y-2*mm, xx, line_y+2*mm)
            canvas.setFont("Arial", 8)
            canvas.setFillColor(INK)
            canvas.drawString(23*mm, line_y-6*mm, "Régua de 100 mm para conferir a escala")
        rule(canvas, 23*mm, 24*mm, PAGE_W-23*mm, BACK)
        canvas.setFont("Arial", 8)
        canvas.drawString(23*mm, 18*mm, "141 cartas / 126 de criação + 15 guias")
        canvas.drawRightString(PAGE_W-23*mm, 18*mm, f"{number:02d} / 02")
        canvas.showPage()
    canvas.save()


def place(row: int, col: int) -> tuple[float, float]:
    return LEFT + col * (CARD_W + GAP_X), BOTTOM + (1 - row) * (CARD_H + GAP_Y)


def trim_marks(canvas: Canvas) -> None:
    canvas.setStrokeColor(colors.HexColor("#6E746B"))
    canvas.setLineWidth(0.35)
    for row in range(2):
        for col in range(2):
            x, y = place(row, col)
            for xx, sign in ((x, -1), (x + CARD_W, 1)):
                for yy, ysign in ((y, -1), (y + CARD_H, 1)):
                    canvas.line(xx + sign * 1.2 * mm, yy, xx + sign * 3.4 * mm, yy)
                    canvas.line(xx, yy + ysign * 1.2 * mm, xx, yy + ysign * 3.4 * mm)


def build_sheets(cards: list[dict], path: Path, backs=False) -> list[dict]:
    canvas = Canvas(str(path), pagesize=A4, pageCompression=1)
    fit_report = []
    for start in range(0, len(cards), 4):
        sheet = start // 4 + 1
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
        for pos, card in enumerate(cards[start:start + 4]):
            row, col = divmod(pos, 2)
            # Long-edge duplex mirrors the back's columns.
            x, y = place(row, 1 - col if backs else col)
            if backs:
                draw_back(canvas, x, y)
            else:
                fit_report.append(draw_front(canvas, card, x, y))
        trim_marks(canvas)
        sheet_footer(canvas, sheet, "VERSO ESPELHADO" if backs else "FRENTE")
        canvas.showPage()
    canvas.save()
    return fit_report

def main() -> None:
    setup_fonts()
    PRINT.mkdir(parents=True, exist_ok=True)
    cards = json.loads(DECK.read_text(encoding="utf-8"))["cartas"]
    load_art(cards)
    front = PRINT / "Persona-Cards-5.1-Ilustrado-Frentes-A4.pdf"
    back = PRINT / "Persona-Cards-5.1-Ilustrado-Versos-A4.pdf"
    duplex = PRINT / "Persona-Cards-5.1-Ilustrado-Duplex-A4.pdf"
    manual = PRINT / "Persona-Cards-5.1-Ilustrado-Manual-Rapido.pdf"
    fit = build_sheets(cards, front)
    build_sheets(cards, back, backs=True)
    build_duplex(front, back, duplex)
    build_manual(manual)
    report = {
        "deck_sha256": hashlib.sha256(DECK.read_bytes()).hexdigest(),
        "manifest_sha256": hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        "cards": len(cards), "illustrations": len(ART),
        "spritesheets": len({p for p, _ in ART.values()}),
        "size_mm": [92, 130], "sheets": (len(cards)+3)//4,
        "fit": fit,
        "files": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (front, back, duplex, manual)},
    }
    (PRINT / "verificacao-impressao-5.1-ilustrado.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(f"Rendered {len(cards)} cards, {report['spritesheets']} spritesheets; "
          f"smallest art {min(x['art_pt'] for x in fit)} pt, "
          f"smallest body {min(x['body_pt'] for x in fit)} pt")


if __name__ == "__main__":
    main()
