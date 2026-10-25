"""Build 5.2 from the preserved 5.1 deck and the approved OR/CV expansion."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "deck/persona-cards-5.1.json"
EXPANSION = ROOT / "deck/expansao-5.2.json"
OUTPUTS = (ROOT / "deck/persona-cards-5.2.json", ROOT / "app/public/deck.json",
           ROOT / "skills/persona-cards/references/deck.json")
FAMILIES = ["OR", "CV", "D", "F", "V", "L", "P", "N"]
GUIDE_REVISIONS = {"U01", "U02", "U06", "U08", "G06"}


def build_deck() -> dict:
    deck = json.loads(SOURCE.read_text(encoding="utf-8"))
    expansion = json.loads(EXPANSION.read_text(encoding="utf-8"))
    if expansion["versao"] != "5.2" or expansion["revisao_editorial"] != "5.2.0":
        raise ValueError("Unsupported expansion revision")
    expected = {f"{family}{n:02d}" for family in ("OR", "CV") for n in range(1, 13)} | {"G07"}
    additions = expansion["cartas"]
    if len(additions) != 25 or {c["codigo"] for c in additions} != expected:
        raise ValueError("The expansion requires OR01–12, CV01–12 and G07 exactly once")
    revisions = expansion["revisoes_guias"]
    if set(revisions) != GUIDE_REVISIONS:
        raise ValueError("Only the five creation-orientation guides may be revised")
    by_code = {c["codigo"]: c for c in deck["cartas"]}
    if len(by_code) != 141:
        raise ValueError("Expected the preserved 141-card source")
    for code, patch in revisions.items():
        if not set(patch) <= {"campos", "leitura"} or not patch:
            raise ValueError(f"Guide identity cannot change: {code}")
        by_code[code].update(deepcopy(patch))
    for card in deck["cartas"]:
        card["versao"] = "5.2"
    for card in additions:
        if card["versao"] != "5.2" or not card["leitura"].strip():
            raise ValueError("Expansion cards require version and reading")
        family = card["familia"]
        if card["codigo"] == "G07":
            if family != "G" or card["modulo"] != "guia_contexto":
                raise ValueError("G07 must remain a context guide")
            if list(card["campos"]) != ["Chamado", "Resposta", "Fato", "Crença", "Escolha"]:
                raise ValueError("Unexpected G07 fields")
            for field in ("Chamado", "Resposta"):
                lines = card["campos"][field].splitlines()
                if len(lines) != 6 or any(not line.startswith(f"{n}. ") for n, line in enumerate(lines, 1)):
                    raise ValueError("G07 requires two numbered d6 lists")
        elif family not in ("OR", "CV") or card["modulo"] != "expansao_5_2" or set(card["campos"]) != {"Pergunte", "Mostre", "Contraste"}:
            raise ValueError("Invalid OR/CV card contract")
    deck["cartas"].extend(deepcopy(additions))
    deck.update(versao="5.2", revisao_editorial="5.2.0", familias_sorteaveis=list(FAMILIES),
                modulos=dict(Counter(c["modulo"] for c in deck["cartas"])),
                modo_rapido="Uma OR/CV/D/F/V/L/P/N e G07: oito interpretações mais chamado, resposta, fato, crença e escolha.",
                criacao_completa={"familias": list(FAMILIES), "guia": "G07",
                                  "journey": ["call", "response", "fact", "belief", "choice"]},
                preservacao="Os 141 códigos, títulos e módulos anteriores permanecem. Somente os guias U01/U02/U06/U08/G06 recebem orientação de criação 5.2. As edições 5.0 e 5.1 ficam preservadas em seus arquivos históricos.",
                comparacao="5.2 exige oito famílias e Chamado e destino. OR não implica culpa; CV distingue fato, valor e regra; N exige dois valores genuínos, sem trauma ou redenção obrigatórios. Sorteio não garante coerência.")
    if len(deck["cartas"]) != 166 or sum(c["familia"] in FAMILIES for c in deck["cartas"]) != 150:
        raise ValueError("Expected 166 cards, 150 for creation and 16 guides")
    return deck


def main() -> None:
    output = (json.dumps(build_deck(), ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    for path in OUTPUTS:
        path.write_bytes(output)
    print("Built 166 cards (150 creation, 16 guides), revision 5.2.0, in three identical copies")


if __name__ == "__main__":
    main()
