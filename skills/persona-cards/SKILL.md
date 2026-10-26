---
name: persona-cards
description: Cria e aprofunda personagens de RPG e ficção com Persona Cards 5.2: oito famílias obrigatórias e o guia Chamado e destino.
---

# Persona Cards

Conecte passado, interpretação, intenção e escolha. As cartas são convites narrativos; não determinam respostas de jogadores, diagnóstico ou destino.

## Material e edição

Leia [manual e cartas](references/deck.md) na primeira aplicação; use o [índice](references/indice.md) e `scripts/cards.py` para consultas. A fonte é [deck.json](references/deck.json): **5.2, revisão 5.2.0, 166 cartas — 150 de criação e 16 guias**. Nunca invente códigos e títulos oficiais. Veja [exemplos](references/exemplos.md) e [limites](references/revisao.md).

Use **uma carta de cada família OR + CV + D + F + V + L + P + N**, além de **G07 — Chamado e destino**. As oito famílias são obrigatórias. U/G são consulta, nunca personalidade sorteada; G07 não é uma nona família de personalidade.

## Método

1. Extraia cenário, papel, tom e fatos estabelecidos. Separe fatos de propostas; não substitua a biografia para justificar um sorteio.
2. Conecte **OR** (antecedente) e **CV** (convicção) por “por isso”, “apesar disso” ou “mais tarde aprendi”. Origem não determina culpa ou trauma. CV pode ser crença factual, valor ou regra prática; somente proposições factuais recebem verdadeiro/falso.
3. Complete **D** com um resultado concreto, **F** com tentativa observável e **V** com fala, gesto, escrita ou sinais. CV não substitui objetivo, método nem expressão.
4. Complete **L** com um laço; se envolver pessoa viva, descreva sua vontade própria. Pessoa morta, objeto, entidade e pessoa viva não recebem a mesma agência. **P** é uma circunstância que muda a escolha, não traço de personalidade.
5. Complete **N** com **dois valores genuínos que a pessoa quer preservar**, colocados em disputa. Obstáculo, coerção, crueldade ou custo não bastam. Se a carta não cabe, troque ou ressorteie N; não omita a família nem force arrependimento, bondade ou redenção. G06 ajuda nessa distinção. Escolher um valor e sacrificar o outro é possível.
6. Consulte **G07** e registre cinco respostas: `call` (chamado), `response` (primeira resposta), `fact` (fato confirmável), `belief` (crença/interpretação) e `choice` (escolha agora). Escolha ou use 1d6 nas listas de chamado e resposta. Recusar, adiar ou renegociar são válidos. Profecia não obriga o desfecho.
7. Acrescente competência, prazer cotidiano e limite reconhecido — ou sua ausência. Faça uma cena com tentativa, resposta aberta e consequência possível. Registre o que mudou depois de jogar; não ressorteie o passado a cada sessão.

## Entrega e continuidade

Todo personagem novo completo inclui nome/papel, os oito códigos e interpretações, os cinco registros de G07, uma competência, um prazer cotidiano e uma tentativa concreta. Mostre reação à recusa; não determine escolhas dos jogadores. A escala do texto pode variar, sem eliminar famílias.

Em personagens existentes, preserve identidade e fatos. Novas OR/CV/N ou etapas da jornada precisam ser propostas explícitas se ainda não estabelecidas. Não declare a ficha completa enquanto faltar uma camada ou dois valores genuínos. Peça apenas informação indispensável quando não houver como preservar o recorte sem inventá-la.

Fichas pessoais 5.0/5.1 são preservadas como rascunhos pendentes quando faltam camadas, sem inventar automaticamente passados, convicções ou conflitos. A galeria web contém **105 leituras autorais completas 5.2**, com oito famílias, justificativas e G07; novas cenas e tensões são propostas explícitas, não fatos canônicos. Finalizar exige as oito famílias e G07. Aceitar uma importação não certifica coerência narrativa.

## Consulta portátil

Python 3 padrão, sem serviço externo:

```text
python scripts/cards.py get OR04 CV05 D03 F17 V09 L08 P04 N07 G07
python scripts/cards.py search conviccao
python scripts/cards.py draw --seed 42
python scripts/cards.py draw --families OR CV
```

O padrão sorteia as oito famílias. `--families` permite consultar ou ressorteiar camadas específicas; isso não torna uma combinação parcial uma ficha finalizada. Interprete, revise e troque cartas incompatíveis com fatos estabelecidos.

## Conferência

- Oito famílias e cinco registros de G07 preenchidos?
- OR é antecedente, CV interpretação, D resultado, F método e V expressão?
- L preserva a outra vontade e P descreve circunstância concreta?
- N tem dois valores genuínos, sem confundir adversidade com ambivalência?
- Fatos, crenças, propostas e escolhas separados, sem diagnóstico ou destino imposto?
- Vida cotidiana, agência e recusa preservadas, sem cura obrigatória do vilão?

## Impressão

[PDFs 5.2](print/README.md): 166 cartas em A4, quatro por folha, 92 × 130 mm. Use 100% e virar na borda longa; teste uma folha antes do lote. Edições 5.0/5.1 são históricas. Conferência digital não comprova impressão física nem eficácia em mesa.
