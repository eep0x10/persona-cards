"""Generate human-readable references from the active 5.1 JSON deck."""

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
DECK = json.loads((ROOT / "deck/persona-cards-5.1.json").read_text(encoding="utf-8"))
LABELS = {
    "D": "Desejo — o que quer agora",
    "F": "Forma de agir — como tenta",
    "V": "Expressão — como comunica",
    "L": "Vínculo — quem também quer algo",
    "P": "Pressão — o que muda a situação",
    "N": "Conflito interno — dois valores reais",
    "U": "Guias de uso",
    "G": "Guias de contexto",
}
ORDER = "DFVLPNUG"


def main() -> None:
    cards = DECK["cartas"]
    revision = DECK["revisao_editorial"]
    manual = [
        f"# Persona Cards 5.1 — revisão editorial {revision}", "",
        "**141 cartas em português: 126 de criação e 15 guias.** O formato 5.1 mantém os códigos, títulos e módulos de 5.0 e acrescenta uma leitura individual para cada carta. O deck 5.0 permanece congelado como histórico.", "",
        "## Correções da revisão 5.1.1", "",
        "- **U08:** apresenta os três módulos e os intervalos diferentes da expansão 5.0 por família; P termina em P18.",
        "- **D10:** descreve poder sobre uma decisão sem exigir cooperação ou um limite moral reconhecido. A margem real de recusa dos demais deve ficar explícita.",
        "- **D13:** admite sobrevivência imediata ou proteção duradoura da própria vida; esse desejo não determina os meios empregados.",
        "As correções alteram somente campos de U08/D10/D13 e aberturas de D10/D13. As outras 138 cartas permanecem iguais à edição de leitura anterior. Nenhum código novo foi criado; D06 não foi revisada. O campo `versao` continua 5.1 para compatibilidade, e `revisao_editorial` identifica 5.1.1.", "",
        "## Como começar", "",
        "1. Escolha ou sorteie **D + F + V**. Leia a abertura da carta; complete o objetivo, a forma de agir e a expressão com detalhes de sua campanha.",
        "2. Dê nome, papel, competência, prazer cotidiano e limite ao personagem. Mostre uma tentativa concreta em cena e deixe a resposta do interlocutor aberta.",
        "3. Acrescente **L + P** quando o vínculo ou a circunstância mudarem a escolha. Preserve a vontade própria de outras pessoas.",
        "4. Use **N somente quando o personagem valoriza dois lados em disputa**. Custo, coerção e obstáculo externo não bastam. U/G são consulta, nunca personalidade sorteada.",
        "5. Depois da cena, registre a ação e a consequência observada. Preserve os fatos jogados; adapte ou troque uma carta que contradiga a continuidade.", "",
        "As aberturas convidam a interpretar, não atribuem diagnóstico, trauma, bondade, redenção ou resultado garantido. Desejo não é método; expressão não é identidade; pressão não é conflito interno. O método não substitui as regras do RPG usado pela mesa.", "",
        "## Famílias", "",
    ]
    for family in ORDER:
        count = sum(c["familia"] == family for c in cards)
        manual.append(f"- **{family} — {LABELS[family]}:** {count} cartas.")
    manual += ["", "## Cartas completas", ""]
    index = [f"# Índice oficial 5.1 — revisão editorial {revision}", "", "Leitura individual, correções U08/D10/D13 e campos completos: [manual](deck.md).", ""]
    for family in ORDER:
        manual += [f"## {LABELS[family]}", ""]
        index += [f"## {LABELS[family]}", ""]
        for card in (c for c in cards if c["familia"] == family):
            manual += [
                f"### {card['codigo']} — {card['titulo']} ({card['modulo']})", "",
                f"> {card['leitura']}", "",
            ]
            for name, value in card["campos"].items():
                manual += [f"**{name}:** {value}", ""]
            index.append(f"- {card['codigo']} — {card['titulo']} ({card['modulo']})")
        index.append("")
    rendered = "\n".join(manual).rstrip() + "\n"
    (ROOT / "deck/manual-5.1.md").write_text(rendered, encoding="utf-8")
    (ROOT / "skills/persona-cards/references/deck.md").write_text(rendered, encoding="utf-8")
    (ROOT / "skills/persona-cards/references/indice.md").write_text("\n".join(index), encoding="utf-8")
    skill = (ROOT / "skills/persona-cards/SKILL.md").read_text(encoding="utf-8")
    skill = skill.split("---", 2)[-1].strip()
    skill = skill.replace("](references/", "](../skills/persona-cards/references/")
    skill = skill.replace("](print/", "](../skills/persona-cards/print/")
    gpt = f"# Persona Cards 5.1 — revisão editorial {revision} — instruções e referência para GPT\n\n"
    gpt += "O método da skill e as 141 cartas completas estão reunidos abaixo.\n\n"
    gpt += skill + "\n\n---\n\n" + rendered
    (ROOT / "docs/persona-cards-gpt.md").write_text(gpt, encoding="utf-8")
    print("Generated manual, skill reference, index and self-contained GPT reference")


if __name__ == "__main__":
    main()
