"""Generate 5.2 documentation only; preserve historical manuals, JSON and PDFs."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ORDER = ("OR", "CV", "D", "F", "V", "L", "P", "N", "U", "G")
LABELS = {"OR": "Origem — o que aconteceu antes", "CV": "Convicção — como interpreta e orienta escolhas",
          "D": "Desejo — o que quer agora", "F": "Forma de agir — como tenta", "V": "Expressão — como comunica",
          "L": "Vínculo — quem também quer algo", "P": "Pressão — o que muda a situação",
          "N": "Conflito interno — dois valores genuínos", "U": "Guias de uso", "G": "Guias de contexto"}


def main() -> None:
    deck = json.loads((ROOT / "deck/persona-cards-5.2.json").read_text(encoding="utf-8"))
    cards = deck["cartas"]
    if deck["versao"] != "5.2" or deck["revisao_editorial"] != "5.2.1":
        raise ValueError("Expected the approved 5.2 / 5.2.1 deck")
    if len(cards) != 169 or len({c["codigo"] for c in cards}) != 169:
        raise ValueError("Expected 169 unique cards")
    if sum(c["familia"] in ORDER[:8] for c in cards) != 153 or set(c["familia"] for c in cards) != set(ORDER):
        raise ValueError("Expected 153 creation cards, 16 guides and all eight creation families")
    guide = next(c for c in cards if c["codigo"] == "G07")
    if set(guide["campos"]) != {"Chamado", "Resposta", "Fato", "Crença", "Escolha"}:
        raise ValueError("G07 must provide the five approved journey fields")
    manual = ["# Persona Cards 5.2 — revisão 5.2.1", "",
        "**169 cartas em português: 153 de criação e 16 guias.** A criação completa usa uma carta OR, CV, D, F, V, L, P e N, mais G07 — Chamado e destino. As oito famílias são obrigatórias; U/G são consulta, nunca personalidade sorteada.", "",
        "## Como jogar", "",
        "1. Separe as famílias e escolha ou sorteie OR + CV + D + F + V + L + P + N. Leia a abertura e os campos reais de cada carta.",
        "2. Conecte OR e CV por por isso, apesar disso ou mais tarde aprendi. Origem não determina culpa, trauma ou uma única convicção.",
        "3. Diga o resultado D, a tentativa F e a expressão V. Em L, respeite a vontade de pessoas vivas e o alcance estabelecido para objetos, entidades ou memória de mortos. Concretize P como circunstância que muda a escolha.",
        "4. N exige dois valores genuínos que a pessoa quer preservar. Se só descreve um obstáculo ou não cabe no recorte, troque ou ressorteie N; não omita a família. Não force culpa, conciliação ou redenção.",
        "5. Consulte G07: registre chamado, resposta, fato, crença e escolha. Escolha ou use 1d6 nas listas abaixo. Recusar e renegociar continuam possíveis; destino não determina o resultado.",
        "6. Acrescente nome, papel, competência e prazer cotidiano. Mostre uma tentativa em cena, aceite a resposta dos demais e registre a consequência observada.", "",
        "## Chamado e destino — G07", "",
        "O guia acompanha toda criação completa. As oito cartas descrevem a pessoa; G07 organiza sua resposta à situação. Escolha ou role 1d6 em cada uma das duas listas.", ""]
    for label, value in guide["campos"].items():
        manual += [f"### {label}", "", value, ""]
    manual += ["No aplicativo, esses registros são `journey.call`, `response`, `fact`, `belief` e `choice`. Podem ser anotados em papel. Um valor não é uma afirmação factual: questione sua aplicação sem declará-lo um fato falso.", "",
        "## Compatibilidade e histórico", "",
        "Fichas 5.0/5.1 conservam nomes, textos, códigos e fotos, mas ficam como rascunhos pendentes no método 5.2 quando não têm as oito famílias e G07. Não se inventam novos passados ou valores na importação. A galeria de 105 inspirações oferece leituras autorais completas 5.2, com oito cartas, justificativas e G07; suas novas cenas são propostas, não eventos canônicos. Copiar uma base permite adaptar essa interpretação, sem alterar fichas existentes.", "",
        "Os arquivos 5.0/5.1 são históricos. A edição 5.2 acrescenta OR/CV/G07 e atualiza orientações dos guias. Não se reescrevem retroativamente as avaliações anteriores como prova do novo método.", "", "## Famílias", ""]
    for family in ORDER:
        manual.append(f"- **{family} — {LABELS[family]}:** {sum(c['familia'] == family for c in cards)} cartas.")
    manual += ["", "## Cartas completas", ""]
    index = ["# Índice Persona Cards 5.2 — revisão 5.2.1", "", "Oito famílias obrigatórias e G07: [manual e cartas](deck.md).", ""]
    for family in ORDER:
        manual += [f"## {LABELS[family]}", ""]
        index += [f"## {LABELS[family]}", ""]
        for card in (c for c in cards if c["familia"] == family):
            manual += [f"### {card['codigo']} — {card['titulo']} ({card['modulo']})", "", f"> {card['leitura']}", ""]
            for label, value in card["campos"].items():
                if "\n" in value:
                    manual += [f"**{label}:**", "", value, ""]
                else:
                    manual += [f"**{label}:** {value}", ""]
            index.append(f"- {card['codigo']} — {card['titulo']} ({card['modulo']})")
        index.append("")
    rendered = "\n".join(manual).rstrip() + "\n"
    (ROOT / "deck/manual-5.2.md").write_text(rendered, encoding="utf-8")
    (ROOT / "skills/persona-cards/references/deck.md").write_text(rendered, encoding="utf-8")
    (ROOT / "skills/persona-cards/references/indice.md").write_text("\n".join(index), encoding="utf-8")
    skill = (ROOT / "skills/persona-cards/SKILL.md").read_text(encoding="utf-8").split("---", 2)[-1].strip()
    skill = skill.replace("](references/", "](../skills/persona-cards/references/").replace("](print/", "](../skills/persona-cards/print/")
    examples = (ROOT / "skills/persona-cards/references/exemplos.md").read_text(encoding="utf-8")
    gpt = "# Persona Cards 5.2 — instruções, cartas e exemplos\n\nMétodo completo de oito famílias e G07; fontes 5.0/5.1 são históricas.\n\n"
    gpt += skill + "\n\n---\n\n" + rendered + "\n\n---\n\n" + examples
    (ROOT / "docs/persona-cards-gpt.md").write_text(gpt, encoding="utf-8")
    print("DOCS_5_2_OK: 169 cards; manual, skill reference, index and GPT text synchronized")


if __name__ == "__main__":
    main()
