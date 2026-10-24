---
name: persona-cards
description: Cria e aprofunda personagens vivos para RPG e ficção usando Persona Cards 5.1. Use ao criar NPCs, protagonistas, antagonistas, elencos, vozes, vínculos, cenas e arcos, ou melhorar personagens existentes preservando contexto e continuidade.
---

# Persona Cards

Transforme cartas em comportamento específico, escolhas e consequências. Profundidade vem da interpretação em contexto, não da quantidade de camadas.

## Material

Leia [manual e cartas](references/deck.md) na primeira aplicação. Use [índice](references/indice.md) e `scripts/cards.py` para consultas direcionadas. A fonte oficial é [deck.json](references/deck.json): 141 cartas, 126 de criação e 15 guias. Cada carta 5.1 tem uma abertura editorial (`leitura`) para ser lida ao puxar, seguida dos campos de ação; não trate a abertura como biografia pronta. Consulte campos reais; nunca invente códigos e títulos oficiais. Veja [exemplos](references/exemplos.md) e [revisão](references/revisao.md).

## Método

A revisão editorial **5.1.1** mantém o formato 5.1, os 141 códigos, títulos e módulos. Corrige somente U08/D10/D13; o deck 5.0 permanece congelado.

- **D10 — autoridade:** o desejo é ter poder sobre uma decisão. Pode envolver participação, influência ou domínio; não exige cooperação, consentimento ou limite moral reconhecido. Descreva a margem real de recusa dos demais. F13/F14 distinguem coerção e encenação do objetivo.
- **D13 — sobrevivência:** pode orientar saída de perigo imediato ou proteção duradoura da própria vida. Diga qual horizonte move a próxima ação; desejar sobreviver não determina meios ou bondade. D04 continua protegendo alguém ou lugar.
- **U08 — módulos:** núcleo 01–12; expansão 13–18; expansão 5.0 D19–D24/F19–F20/N19–N22/L19–L20/V19–V22. P termina em P18. U/G continuam sendo consulta.

1. Extraia contexto, tom, papel e fatos estabelecidos. Separe fatos de propostas. Resolva detalhes rotineiros com escolhas adequadas; pergunte só pelo indispensável. Preserve agência dos jogadores e continuidade.
2. Escolha **D + F + V**: o que quer agora, como tenta obter e como se expressa. Selecione por significado em criação intencional; sorteie quando o pedido for surpresa. Substitua espaços por pessoas, objetos e situações concretas.
3. Acrescente vida cotidiana: uma competência, um prazer ou hábito, uma relação com vontade própria e uma reação reconhecível. Faça objetivo, tática e voz se influenciar. Não transforme todos os detalhes em trauma, segredo ou gancho épico.
4. Use **L + P** quando vínculo e pressão ajudarem. **N somente com dois valores reais que o personagem quer preservar.** Obstáculo, custo e crueldade não provam ambivalência. Orientação dominante ou conflito desconhecido são válidos: consulte G06.
5. Consulte **G01–G05** quando memória, percepção, influência externa, mandato ou identidade importarem. Separe fato, crença e incerteza; esses mecanismos não substituem personalidade. **U e G nunca entram no sorteio de personalidade.**
6. Teste em cena: objetivo imediato, tentativa, resposta aberta do interlocutor e consequência possível. Mostre ação e fala ou outra forma de expressão, além de adjetivos. Não determine escolhas dos jogadores.
7. Revise e entregue material pronto para usar. Troque cartas incompatíveis se necessário; diga quando o encaixe exige adaptação e preserve lacunas reais.

## Entrega proporcional

NPC rápido: nome/papel, D/F/V, objetivo agora, ação visível, expressão, detalhe cotidiano e reação à recusa. Um parágrafo e uma fala bastam. Personagem central: acrescente vínculos, pressão, tensão real quando houver, limites, condições de mudança e cena curta. Registre códigos numa linha discreta para rastreabilidade, sem sobrecarregar a narrativa.

Personagem existente: preserve primeiro seu núcleo e fatos; identifique o genérico e torne isso observável. Marque novos detalhes como propostas. Não reescreva o passado para justificar uma carta.

Histórias: mapeie intenções relevantes, deixe cada personagem tentar algo por métodos diferentes e construa consequências dessas tentativas. Arcos são possibilidades condicionais, não redenção obrigatória. Atualize somente o que as cenas alteraram.

Elencos: varie objetivos, métodos, vozes, vínculos e reações sob pressão, além de nomes e estética. Uma carta compartilhada não torna dois personagens iguais.

## Revisão

- Quer algo específico e consegue agir sem esperar o protagonista?
- Tem comportamento e expressão reconhecíveis, além de rótulos?
- Camadas produzem uma escolha em cena com respostas abertas?
- Vínculos preservam a vontade própria dos outros?
- N demonstra dois valores? Se não, omita.
- Há vida além do problema, sem trauma, segredo ou heroísmo obrigatórios?
- Fatos, percepção e propostas estão separados? Não inferiu diagnóstico?
- Respeita tom, cânone e agência?

## Consulta portátil

Python 3 padrão, sem rede nem dependências extras:

```text
python scripts/cards.py get D19 F20 V22
python scripts/cards.py search vocacao
python scripts/cards.py draw --seed 42
python scripts/cards.py draw --families D F V L P --modules nucleo expansao expansao_5
```

O padrão sorteia D/F/V; N exige inclusão intencional. U/G são consultáveis, mas rejeitados no sorteio. Combinação aleatória não garante compatibilidade: interprete e revise.

## Cartas para imprimir

A pasta [print](print/README.md) contém as 141 cartas 5.1 em PDF de leitura ampliada: duplex A4, frentes, versos e manual rápido. Os PDFs 5.0 de 63 × 88 mm permanecem como histórico. Use 100% e virar na borda longa; teste uma folha antes do lote.
