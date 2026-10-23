"""Check source-art coverage and the generated illustrated print PDFs."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
PRINT = ROOT / "skills/persona-cards/print"


def compact(text: str) -> str:
    return "".join(char.casefold() for char in text if char.isalnum())


def main() -> None:
    cards = json.loads((ROOT / "deck/persona-cards-5.1.json").read_text(encoding="utf-8"))["cartas"]
    sheets = json.loads((ROOT / "deck/illustration_sheets_5_1.json").read_text(encoding="utf-8"))["sheets"]
    expected = [card["codigo"] for card in cards]
    mapped = [code for sheet in sheets for code in sheet["codes"]]
    assert len(expected) == len(mapped) == len(set(mapped)) == 141
    assert set(mapped) == set(expected)
    for sheet in sheets:
        path = PRINT / "assets" / sheet["file"]
        with Image.open(path) as image:
            assert image.mode == "RGBA" and image.size == (1536, 1024), path
            alpha = image.getchannel("A")
            for slot, code in enumerate(sheet["codes"]):
                x, y = (slot % 3) * 512, (slot // 3) * 512
                cell = alpha.crop((x, y, x + 512, y + 512))
                opaque = sum(cell.histogram()[180:])
                assert opaque >= 1000, (code, path.name, opaque)
    paths = {
        "front": PRINT / "Persona-Cards-5.1-Ilustrado-Frentes-A4.pdf",
        "back": PRINT / "Persona-Cards-5.1-Ilustrado-Versos-A4.pdf",
        "duplex": PRINT / "Persona-Cards-5.1-Ilustrado-Duplex-A4.pdf",
        "manual": PRINT / "Persona-Cards-5.1-Ilustrado-Manual-Rapido.pdf",
    }
    readers = {key: PdfReader(str(path)) for key, path in paths.items()}
    assert {key: len(reader.pages) for key, reader in readers.items()} == {
        "front": 36, "back": 36, "duplex": 72, "manual": 2,
    }
    for key, reader in readers.items():
        for page in reader.pages:
            box = page.mediabox
            assert abs(float(box.width) - 595.276) < .2, key
            assert abs(float(box.height) - 841.89) < .2, key
    front = readers["front"]
    duplex = readers["duplex"]
    for index, card in enumerate(cards):
        page = index // 4
        for reader, page_number in ((front, page), (duplex, 2 * page)):
            rendered = compact(reader.pages[page_number].extract_text())
            for value in (card["codigo"], card["titulo"], card["leitura"]):
                assert compact(value) in rendered, (card["codigo"], page_number, value)
    report = json.loads((PRINT / "verificacao-impressao-5.1-ilustrado.json").read_text(encoding="utf-8"))
    assert report["cards"] == report["illustrations"] == 141
    assert report["spritesheets"] == 24
    assert min(item["body_pt"] for item in report["fit"]) >= 8.5
    assert min(item["art_pt"] for item in report["fit"]) >= 80
    print("OK: 141 artes visíveis, 24 spritesheets, textos e códigos, 36+36+72+2 páginas A4")


if __name__ == "__main__":
    main()
