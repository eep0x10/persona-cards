"""Build the 5.1 editorial deck from the frozen 5.0 source and reviewed readings."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "deck/persona-cards-5.0.json"
READINGS = ROOT / "deck/leituras-5.1.json"
EDITORIAL = ROOT / "deck/editorial-5.1.1.json"
EDITORIAL_CODES = frozenset({"U08", "D10", "D13"})
OUTPUTS = (
    ROOT / "deck/persona-cards-5.1.json",
    ROOT / "app/public/deck.json",
    ROOT / "skills/persona-cards/references/deck.json",
)


def apply_editorial_overlay(deck: dict, overlay: dict) -> None:
    """Apply the reviewed correction surface; never accept identity changes."""
    if set(overlay) != {"versao", "revisao_editorial", "alteracoes"}:
        raise ValueError("Unexpected editorial metadata")
    if overlay["versao"] != "5.1" or overlay["revisao_editorial"] != "5.1.1":
        raise ValueError("Unsupported editorial revision")
    changes = overlay["alteracoes"]
    if not isinstance(changes, dict) or set(changes) != EDITORIAL_CODES:
        raise ValueError("Only U08, D10 and D13 are approved for revision 5.1.1")
    by_code = {card["codigo"]: card for card in deck["cartas"]}
    for code, patch in changes.items():
        expected_keys = {"campos"} if code == "U08" else {"leitura", "campos"}
        if not isinstance(patch, dict) or set(patch) != expected_keys:
            raise ValueError(f"Unsupported editorial fields for {code}")
        fields = patch["campos"]
        expected_labels = {"Distribua", "Contraste", "Confira"} if code == "U08" else {"Quero", "Mostre", "Interação"}
        if not isinstance(fields, dict) or set(fields) != expected_labels:
            raise ValueError(f"Unexpected field labels for {code}")
        if any(not isinstance(value, str) or not value.strip() for value in fields.values()):
            raise ValueError(f"Empty or invalid editorial text for {code}")
        # Openings have a single canonical value in readings and in the overlay.
        if "leitura" in patch and patch["leitura"] != by_code[code]["leitura"]:
            raise ValueError(f"Editorial reading differs from the reviewed readings: {code}")
    for code, patch in changes.items():
        by_code[code].update(patch)
    deck["revisao_editorial"] = overlay["revisao_editorial"]


def build_deck() -> dict:
    deck = json.loads(SOURCE.read_text(encoding="utf-8"))
    readings = json.loads(READINGS.read_text(encoding="utf-8"))["leituras"]
    codes = [card["codigo"] for card in deck["cartas"]]
    if len(codes) != len(set(codes)) or set(codes) != set(readings):
        raise ValueError("The 5.1 readings must cover each official code exactly once")
    if len(set(readings.values())) != len(readings):
        raise ValueError("Each card needs its own reading")
    for card in deck["cartas"]:
        reading = readings[card["codigo"]].strip()
        if not 25 <= len(reading) <= 180:
            raise ValueError(f"Reading length outside review range: {card['codigo']}")
        card["versao"] = "5.1"
        card["leitura"] = reading
    deck["versao"] = "5.1"
    apply_editorial_overlay(deck, json.loads(EDITORIAL.read_text(encoding="utf-8")))
    deck["preservacao"] = (
        "Os 141 códigos, títulos e módulos de 5.0 permanecem; 5.1 acrescenta uma leitura "
        "individual a cada carta. A revisão editorial 5.1.1 corrige os campos de U08, D10 "
        "e D13 e as leituras de D10 e D13; os campos das outras 138 cartas são preservados. "
        "O arquivo 5.0 permanece congelado."
    )
    deck["comparacao"] = (
        "O método D/F/V, a opção L/P e o critério de dois valores reais para N "
        "permanecem. U/G continuam fora do sorteio de personalidade."
    )
    return deck


def main() -> None:
    deck = build_deck()
    output = json.dumps(deck, ensure_ascii=False, indent=2) + "\n"
    for path in OUTPUTS:
        path.write_bytes(output.encode("utf-8"))
    print(f"Built {len(deck['cartas'])} cards, revision {deck['revisao_editorial']}, in three identical copies")


if __name__ == "__main__":
    main()
