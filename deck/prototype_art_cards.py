"""Build an open-composition folk prototype with distinct illustrations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

from render_print_5_1 import INK, PALETTE, PAPER, paragraph, setup_fonts


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "deck/previews"
ATLAS = ROOT / "skills/persona-cards/print/assets/folk-d001-d006.png"
CARD_W, CARD_H = 92 * mm, 130 * mm
GAP_X, GAP_Y = 8 * mm, 9 * mm
LEFT = (A4[0] - 2 * CARD_W - GAP_X) / 2
BOTTOM = (A4[1] - 2 * CARD_H - GAP_Y) / 2


def draw_atlas_cell(canvas: Canvas, cell: int, x: float, y: float, size: float, atlas: Path) -> None:
    col, row = cell % 3, cell // 3
    canvas.saveState()
    clip = canvas.beginPath()
    clip.rect(x, y, size, size)
    canvas.clipPath(clip, stroke=0, fill=0)
    canvas.drawImage(
        ImageReader(str(atlas)),
        x - col * size,
        y - (1 - row) * size,
        width=3 * size,
        height=2 * size,
        mask="auto",
    )
    canvas.restoreState()


def draw_card(canvas: Canvas, card: dict, x: float, y: float, cell: int, atlas: Path) -> None:
    color = colors.HexColor(PALETTE[card["familia"]][1])
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(x - 1 * mm, y - 1 * mm, CARD_W + 2 * mm, CARD_H + 2 * mm, stroke=0, fill=1)
    canvas.setFillColor(color)
    canvas.rect(x + 17, y + CARD_H - 10, CARD_W - 34, 1.8, stroke=0, fill=1)
    canvas.setFont("Arial-Bold", 7.8)
    canvas.drawString(x + 17, y + CARD_H - 21, PALETTE[card["familia"]][0])
    canvas.drawRightString(x + CARD_W - 17, y + CARD_H - 21, card["codigo"])
    canvas.setLineWidth(0.55)
    canvas.line(x + 17, y + CARD_H - 29, x + CARD_W - 17, y + CARD_H - 29)

    title, title_h = paragraph(card["titulo"], "Georgia-Bold", 16.1, 18.5, CARD_W - 38, TA_CENTER)
    title.drawOn(canvas, x + 19, y + CARD_H - 37 - title_h)

    art_size = 128
    art_y = y + CARD_H - 78 - art_size
    art_x = x + (CARD_W - art_size) / 2
    draw_atlas_cell(canvas, cell, art_x, art_y, art_size, atlas)

    reading, read_h = paragraph(card["leitura"], "Georgia-Italic", 9.7, 12.4, CARD_W - 44, TA_CENTER)
    read_top = art_y - 12
    reading.drawOn(canvas, x + 22, read_top - read_h)
    divider = read_top - read_h - 8
    canvas.setStrokeColor(color)
    canvas.setLineWidth(0.7)
    canvas.line(x + 28, divider, x + CARD_W - 28, divider)

    chosen = None
    for body_size in (8.4, 8.1, 7.8, 7.5):
        cursor = divider - 10
        blocks = []
        for label, value in card["campos"].items():
            heading, head_h = paragraph(label.upper(), "Arial-Bold", 7.0, 8.3, CARD_W - 40)
            body, body_h = paragraph(value, "Arial", body_size, body_size * 1.31, CARD_W - 40)
            blocks.append((heading, head_h, body, body_h, cursor))
            cursor -= head_h + body_h + 7
        if cursor >= y + 22:
            chosen = (blocks, cursor)
            break
    if chosen is None:
        raise ValueError(f"Prototype text too low: {card['codigo']} ({cursor-y:.1f} pt)")
    blocks, cursor = chosen
    for heading, head_h, body, body_h, top in blocks:
        heading.drawOn(canvas, x + 20, top - head_h)
        body.drawOn(canvas, x + 20, top - head_h - body_h - 1)

    canvas.setStrokeColor(color)
    canvas.setLineWidth(0.45)
    canvas.line(x + 16, y + 18, x + CARD_W - 16, y + 18)
    canvas.setFillColor(INK)
    canvas.setFont("Arial", 6.5)
    canvas.drawString(x + 17, y + 9, "PERSONA CARDS  /  EDIÇÃO ILUSTRADA")
    canvas.drawRightString(x + CARD_W - 17, y + 9, card["codigo"])
    canvas.restoreState()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--codes", nargs=4)
    parser.add_argument("--atlas", type=Path, default=ATLAS)
    parser.add_argument("--name", default="arte-folk-aberta-d01-d04-a4")
    args = parser.parse_args()
    setup_fonts()
    deck = json.loads((ROOT / "deck/persona-cards-5.1.json").read_text(encoding="utf-8"))["cartas"]
    cards = ([next(card for card in deck if card["codigo"] == code) for code in args.codes]
             if args.codes else deck[args.start_index:args.start_index + 4])
    OUTPUT.mkdir(parents=True, exist_ok=True)
    output = OUTPUT / f"{args.name}.pdf"
    canvas = Canvas(str(output), pagesize=A4)
    for i, card in enumerate(cards):
        row, col = divmod(i, 2)
        x = LEFT + col * (CARD_W + GAP_X)
        y = BOTTOM + (1 - row) * (CARD_H + GAP_Y)
        draw_card(canvas, card, x, y, i, args.atlas)
    canvas.save()
    print(output)


if __name__ == "__main__":
    main()
