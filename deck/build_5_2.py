"""Build 5.2 from preserved sources, the 5.2.0 expansion and editorial patches."""
from collections import Counter
from copy import deepcopy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "deck/persona-cards-5.1.json"
EXPANSION = ROOT / "deck/expansao-5.2.json"
REVISION = ROOT / "deck/revisao-5.2.1.json"
JOURNEY_REVISION = ROOT / "deck/revisao-5.2.2.json"
OUTPUTS = (ROOT / "deck/persona-cards-5.2.json", ROOT / "app/public/deck.json",
           ROOT / "skills/persona-cards/references/deck.json")
FAMILIES = ["OR", "CV", "D", "F", "V", "L", "P", "N"]
GUIDE_REVISIONS = {"U01", "U02", "U06", "U08", "G06"}
EDITORIAL_REVISIONS = {"OR03", "N14", "P12", "L13", "D06", "G06", "U08"}
NEW_CODES = {"F21", "F22", "N23"}


def apply_editorial_revision(deck: dict) -> None:
    revision = json.loads(REVISION.read_text(encoding="utf-8"))
    if revision["versao"] != "5.2" or revision["revisao_editorial"] != "5.2.1":
        raise ValueError("Unsupported editorial revision")
    if set(revision["revisoes"]) != EDITORIAL_REVISIONS:
        raise ValueError("Unexpected editorial card revisions")
    by_code = {card["codigo"]: card for card in deck["cartas"]}
    for code, patch in revision["revisoes"].items():
        if not patch or not set(patch) <= {"titulo", "leitura", "campos"}:
            raise ValueError(f"Editorial revision cannot change identity: {code}")
        if any(not isinstance(value, str) or not value.strip() for key, value in patch.items() if key != "campos"):
            raise ValueError(f"Empty editorial text: {code}")
        if "campos" in patch and (not isinstance(patch["campos"], dict) or not patch["campos"] or
                                  any(not isinstance(value, str) or not value.strip() for value in patch["campos"].values())):
            raise ValueError(f"Invalid editorial fields: {code}")
        by_code[code].update(deepcopy(patch))
    additions = revision["cartas"]
    if len(additions) != 3 or {card["codigo"] for card in additions} != NEW_CODES:
        raise ValueError("The editorial expansion requires F21, F22 and N23 exactly once")
    for card in additions:
        family = "F" if card["codigo"] in {"F21", "F22"} else "N"
        expected_fields = {"Faço", "Ajuda", "Custa"} if family == "F" else {"Disputam", "Mostre", "Pergunte"}
        if (card["codigo"] in by_code or card["versao"] != "5.2" or card["familia"] != family or
                card["modulo"] != "expansao_5_2" or set(card["campos"]) != expected_fields or
                not card["titulo"].strip() or not card["leitura"].strip() or
                any(not isinstance(value, str) or not value.strip() for value in card["campos"].values())):
            raise ValueError(f"Invalid editorial addition: {card['codigo']}")
    deck["cartas"].extend(deepcopy(additions))


def apply_journey_revision(deck: dict) -> None:
    revision = json.loads(JOURNEY_REVISION.read_text(encoding="utf-8"))
    if (set(revision) != {"versao", "revisao_editorial", "revisoes"} or
            revision["versao"] != "5.2" or revision["revisao_editorial"] != "5.2.2" or
            set(revision["revisoes"]) != {"G07"}):
        raise ValueError("Journey revision may update G07 only")
    patch = revision["revisoes"]["G07"]
    if (set(patch) != {"leitura", "campos"} or set(patch["campos"]) != {"Fato", "Escolha"} or
            not isinstance(patch["leitura"], str) or not patch["leitura"].strip() or
            any(not isinstance(value, str) or not value.strip() for value in patch["campos"].values())):
        raise ValueError("Journey revision must preserve identity, five fields and d6 lists")
    guide = next(card for card in deck["cartas"] if card["codigo"] == "G07")
    guide["leitura"] = patch["leitura"]
    guide["campos"].update(deepcopy(patch["campos"]))


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
    apply_editorial_revision(deck)
    apply_journey_revision(deck)
    deck.update(versao="5.2", revisao_editorial="5.2.2", familias_sorteaveis=list(FAMILIES),
                modulos=dict(Counter(c["modulo"] for c in deck["cartas"])),
                modo_rapido="Uma OR/CV/D/F/V/L/P/N e G07: oito interpretações mais chamado, resposta, fato, crença e escolha.",
                criacao_completa={"familias": list(FAMILIES), "guia": "G07",
                                  "journey": ["call", "response", "fact", "belief", "choice"]},
                preservacao="Os códigos e módulos anteriores permanecem. A expansão 5.2.0 e o patch editorial 5.2.1 são fontes versionadas; este último acrescenta F21/F22/N23 e esclarece OR03/N14/P12/L13/D06/G06/U08. O patch 5.2.2 esclarece somente G07, preservando identidade, cinco campos e listas d6. As edições 5.0 e 5.1 ficam preservadas em seus arquivos históricos.",
                comparacao="5.2 exige oito famílias e Chamado e destino. OR não implica culpa; CV distingue fato, valor e regra; N exige dois valores genuínos, sem trauma ou redenção obrigatórios. Sorteio não garante coerência.")
    if len(deck["cartas"]) != 169 or sum(c["familia"] in FAMILIES for c in deck["cartas"]) != 153:
        raise ValueError("Expected 169 cards, 153 for creation and 16 guides")
    return deck


def main() -> None:
    output = (json.dumps(build_deck(), ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    for path in OUTPUTS:
        path.write_bytes(output)
    print("Built 169 cards (153 creation, 16 guides), revision 5.2.2, in three identical copies")


if __name__ == "__main__":
    main()
