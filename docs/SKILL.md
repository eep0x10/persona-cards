# Skill Persona Cards 5.2

[Projeto](../README.md) · [Método canônico](../skills/persona-cards/SKILL.md)

Copie a pasta inteira `skills/persona-cards/` para `~/.codex/skills/persona-cards/` e inicie uma conversa que reconheça a skill. `SKILL.md` fica diretamente dentro da pasta. Outros clientes dependem do próprio suporte; a instalação não se propaga entre conversas.

```text
Use $persona-cards 5.2 para aprofundar este NPC preservando os fatos da campanha.
Escolha e interprete OR/CV/D/F/V/L/P/N e registre G07:
chamado, resposta, fato, crença e escolha.
N precisa de dois valores genuínos; troque a carta se representar só um obstáculo.
Marque como proposta qualquer novo passado ou convicção não estabelecido.
```

Sem suporte a skills, anexe ou cole as [instruções, cartas e exemplos autocontidos](persona-cards-gpt.md) na mesma conversa. Não é uma instalação para outras sessões.

## Consulta Python

Da raiz, sem dependências externas:

```sh
python skills/persona-cards/scripts/cards.py get OR04 CV05 D03 F17 V09 L08 P04 N07 G07
python skills/persona-cards/scripts/cards.py search conviccao
python skills/persona-cards/scripts/cards.py draw --seed 42
python skills/persona-cards/scripts/cards.py draw --families OR CV
```

O padrão sorteia oito famílias; uma consulta parcial ou ressorteio não dispensa as demais numa ficha finalizada. Guias U/G não são sorteados como personalidade. G07 é consultado em toda criação.

OR é antecedente; CV pode ser crença factual, valor ou regra prática. N sempre contém dois valores genuínos. Não confunda coerção com consentimento, custo com conflito interno nem firmeza com falta de profundidade. Uma disputa interna pode terminar sem conciliação ou redenção.

Fichas 5.0/5.1 e exemplos históricos preservam textos, mas não estão automaticamente completos em 5.2. Proponha as camadas faltantes explicitamente e deixe pendências enquanto não houver informação suficiente. O assistente não recebe autorização para reescrever fatos da campanha.

## Impressão e prova

O pacote inclui [166 cartas e manual 5.2](../skills/persona-cards/print/README.md). Validação de códigos e exemplos autorais não comprova facilidade com leitores ou jogadores; não prometa diagnóstico, tempo de criação ou qualidade universal.
