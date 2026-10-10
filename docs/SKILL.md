# Skill Persona Cards

[Projeto](../README.md) · [Método e referências](../skills/persona-cards/SKILL.md)

Copie `skills/persona-cards/` para o diretório de skills do assistente; no Codex, o caminho habitual é `~/.codex/skills/persona-cards/`. Inicie uma sessão que descubra essa pasta e invoque `$persona-cards`. A disponibilidade em outros clientes depende do suporte deles; a instalação não se propaga automaticamente entre chats.

```text
Use $persona-cards para aprofundar este NPC preservando os fatos da campanha.
Mostre objetivo, método, expressão, vínculo e uma reação à recusa.
Só inclua conflito interno se houver dois valores reais em disputa.
```

Para um GPT/chat sem skills, forneça [instruções e referência autocontidas](persona-cards-gpt.md). O arquivo contém método, cartas e exemplos; o script de consulta e o índice são opcionais do pacote.

Consulta portátil na raiz, sem dependências externas:

```sh
python skills/persona-cards/scripts/cards.py get D19 F20 V22
python skills/persona-cards/scripts/cards.py search vocacao
python skills/persona-cards/scripts/cards.py draw --seed 42
python skills/persona-cards/scripts/cards.py draw --families D F V L P --modules nucleo expansao expansao_5
```

O padrão é D/F/V. Guias U/G são consultáveis, mas não sorteáveis. N é opcional; combinação aleatória precisa de interpretação e revisão. A skill não promete diagnóstico psicológico, qualidade universal nem compatibilidade mecânica com um sistema de RPG.
