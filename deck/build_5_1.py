"""Build the 5.1 editorial deck from the frozen 5.0 source and reviewed readings."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "deck/persona-cards-5.0.json"
READINGS = ROOT / "deck/leituras-5.1.json"
OUTPUTS = (
    ROOT / "deck/persona-cards-5.1.json",
    ROOT / "app/public/deck.json",
    ROOT / "skills/persona-cards/references/deck.json",
)


def main() -> None:
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
    deck["preservacao"] = (
        "Os 141 códigos, títulos, campos e módulos de 5.0 permanecem; "
        "5.1 acrescenta uma leitura editorial individual a cada carta."
    )
    deck["comparacao"] = (
        "O método D/F/V, a opção L/P e o critério de dois valores reais para N "
        "permanecem. U/G continuam fora do sorteio de personalidade."
    )
    output = json.dumps(deck, ensure_ascii=False, indent=2) + "\n"
    for path in OUTPUTS:
        path.write_bytes(output.encode("utf-8"))
    print(f"Built {len(codes)} cards in three identical copies")


if __name__ == "__main__":
    main()
