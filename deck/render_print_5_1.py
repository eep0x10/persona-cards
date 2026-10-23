"""Shared print helpers for the 5.1 deck and its preserved art prototype.

The production renderer is render_print_illustrated_5_1.py; this module owns no
card geometry or drawing pipeline.
"""
from __future__ import annotations

from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from pypdf import PdfReader, PdfWriter

INK = colors.HexColor("#22362F")
PAPER = colors.HexColor("#F8F3E9")
PALETTE = {
    "D": ("DESEJO", "#AC4C32"),
    "F": ("FORMA DE AGIR", "#27674E"),
    "N": ("CONFLITO INTERNO", "#715783"),
    "L": ("VÍNCULO", "#9D6B30"),
    "V": ("EXPRESSÃO", "#253F72"),
    "P": ("PRESSÃO", "#386B7C"),
    "U": ("GUIA DE USO", "#5C665A"),
    "G": ("GUIA DE CONTEXTO", "#5C665A"),
}


def setup_fonts() -> None:
    fonts = Path("C:/Windows/Fonts")
    for name, file in (
        ("Georgia", "georgia.ttf"),
        ("Georgia-Bold", "georgiab.ttf"),
        ("Georgia-Italic", "georgiai.ttf"),
        ("Arial", "arial.ttf"),
        ("Arial-Bold", "arialbd.ttf"),
    ):
        pdfmetrics.registerFont(TTFont(name, str(fonts / file)))
    pdfmetrics.registerFontFamily(
        "Georgia", normal="Georgia", bold="Georgia-Bold", italic="Georgia-Italic"
    )
    pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold")


def rule(canvas: Canvas, x1: float, y: float, x2: float, color, width=0.65) -> None:
    canvas.setStrokeColor(color)
    canvas.setLineWidth(width)
    canvas.line(x1, y, x2, y)


def paragraph(text: str, font: str, size: float, leading: float, width: float, align=TA_LEFT):
    style = ParagraphStyle(
        name=f"{font}-{size}-{align}", fontName=font, fontSize=size,
        leading=leading, textColor=INK, alignment=align, spaceBefore=0, spaceAfter=0,
        splitLongWords=False,
    )
    p = Paragraph(escape(text), style)
    _, h = p.wrap(width, 1000)
    return p, h


def build_duplex(front: Path, back: Path, output: Path) -> None:
    fronts, backs = PdfReader(str(front)), PdfReader(str(back))
    if len(fronts.pages) != len(backs.pages):
        raise ValueError("Front and back sheet counts differ")
    writer = PdfWriter()
    for page_front, page_back in zip(fronts.pages, backs.pages):
        writer.add_page(page_front)
        writer.add_page(page_back)
    with output.open("wb") as handle:
        writer.write(handle)
