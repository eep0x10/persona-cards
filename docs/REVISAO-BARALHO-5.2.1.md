# Revisão editorial 5.2.1 do baralho

A edição continua sendo **5.2**, com oito famílias obrigatórias e o guia G07. A revisão editorial **5.2.1** acrescenta três cartas e atualiza sete existentes: cinco cartas e dois guias. O conjunto passa a **169 cartas**, sendo **153 de criação e 16 guias**. Esta revisão vem de um exercício autoral de 105 leituras, não de teste empírico com jogadores ou de impressão física.

## Fontes e reprodução

O gerador [build_5_2.py](../deck/build_5_2.py) compõe, nesta ordem:

1. A fonte histórica preservada [persona-cards-5.1.json](../deck/persona-cards-5.1.json).
2. A expansão aprovada [expansao-5.2.json](../deck/expansao-5.2.json), revisão 5.2.0, sem reescrever sua redação original.
3. O patch versionado [revisao-5.2.1.json](../deck/revisao-5.2.1.json).

Execute na raiz, com Python 3:

```sh
python -X utf8 deck/build_5_2.py
python -X utf8 -m unittest discover -s tests -p test_deck_5_2.py
```

O gerador grava três cópias idênticas: `deck/persona-cards-5.2.json`, `app/public/deck.json` e `skills/persona-cards/references/deck.json`. Não gera PDFs, artes, documentação derivada ou fichas. As edições 5.0 e 5.1 permanecem imutáveis; os códigos, famílias e módulos existentes continuam preservados. Há mudanças de título explicitamente registradas em OR03, P12 e L13.

## Três cartas novas

| Código | Título | Operação e fronteira |
| --- | --- | --- |
| F21 | Ensino para que você tente | Demonstra uma parte, acompanha a tentativa e devolve uma observação. O aprendiz pode recusar ou adaptar: não é planejar por ele, ordenar ou exigir imitação. |
| F22 | Escuto antes de propor | Pede a versão da pessoa, confere o entendimento e reformula a proposta. É um método que altera a ação seguinte, não apenas uma voz delicada ou garantia de bondade. |
| N23 | Prazer imediato / projeto | Duas realizações desejadas em horizontes diferentes: a satisfação disponível pode comprometer um projeto também valorizado. Não exige ética, arrependimento ou uma regra de autocontrole anterior. |

F21 e F22 usam `Faço`, `Ajuda` e `Custa`; N23 usa `Disputam`, `Mostre` e `Pergunte`. As três pertencem ao módulo `expansao_5_2`, agora com 27 cartas. O texto integral está no patch e no deck gerado.

A necessidade de ensinar ficou visível nas leituras de Iroh, Piccolo e Blue: preparar exercícios ou mediar posições não é a mesma operação que transferir uma habilidade. A escuta apareceu nas propostas de reparação de Katara, apoio de Tifa e ajuda questionável de Superman: ouvir só se demonstra como método quando pode mudar a proposta. O conflito entre prazer e projeto apareceu nas cenas autorais de Muzan, Sephiroth e Gus. Esses exemplos motivam opções de criação; não certificam uma psicologia canônica completa nem obrigam reclassificação automática do catálogo.

## Esclarecimentos existentes

| Carta | Mudança | Erro que evita |
| --- | --- | --- |
| OR03 — Um papel foi traçado para mim | Distingue formação, expectativa, programação e mandato; atribuição não pressupõe que todos ocorreram. | Inventar treinamento passado só porque alguém foi nomeado para um papel. Uma profissão livremente escolhida, sozinha, ainda não basta. |
| N14 — Controle / entrega | Os campos exigem espontaneidade ou iniciativa de **outra pessoa**, alinhados à leitura. | Confundir entrega à ação alheia com o próprio prazer de improvisar. |
| P12 — Duas demandas, um recurso | Aceita demandas originadas de promessa, urgência, ordem ou vontade, sem lhes atribuir igual legitimidade. | Inventar uma segunda promessa para uma emergência ou disputa de agenda. |
| L13 — Inimigo que contraria meu projeto | O adversário possui objetivo próprio e pode contrariar algo importante sem definir toda a identidade do protagonista. | Impor admiração, jogo justo ou centralidade identitária a qualquer inimizade. |
| D06 — Resolver uma pergunta | A evidência pode provocar revisão, adiamento, negação, ocultação ou mudança de investigação. Suas consequências permanecem. | Confundir desejo de resolver uma pergunta com honestidade ou abertura obrigatórias de CV07. |
| G06 — Orientação sem conflito ativo | Mantém N obrigatório, permite conflito potencial e esclarece fronteiras entre famílias. | Tratar impedimento, custo ou coerção sem adesão como segundo valor; fabricar trauma, bondade ou um limite anterior. |
| U08 — Elenco variado | Inclui F21–22 e N23 na relação de códigos da expansão 5.2. | Omitir as três cartas novas ao organizar ou variar o elenco. |

G06 também conserva três distinções: **F19** exige nota, ritual ou instrução externa, não simples lembrança mental; **F15** exige insistência depois de um custo observável, não qualquer repetição; **D23** deseja a prática, enquanto **CV12** valoriza o encontro finito mesmo sem ganho duradouro. Essas fronteiras não mudam o significado de F19, F15, D23 ou CV12.

## Oito famílias sem biografia inventada

OR registra um antecedente; CV, uma regra interpretativa; D, o resultado procurado; F, a tentativa; V, sua expressão; L, o vínculo; P, a circunstância; N, duas vontades genuinamente valorizadas. G07 separa chamado, resposta, fato, crença e escolha. Na criação original, as cartas propõem elementos para desenvolver. Num personagem existente, o recorte pode não demonstrar tudo: troque a carta incompatível ou identifique uma situação como variação autoral. Preencher oito campos não transforma a proposta em fato canônico, e N continua obrigatório para concluir.

N18 permanece adequado quando há uma vontade recorrente e um limite próprio reconhecido, como a linha ética de Edward na cena revisada. N23 não deve substituir automaticamente N18, N11 ou N22: dois desejos, prudência diante de oportunidade, limite escolhido e vida fora da vocação são relações diferentes.

## Limites e validação

A distribuição de cartas entre as 105 leituras foi um instrumento de diagnóstico editorial. Frequência, ausência ou concentração não demonstram, isoladamente, uma lacuna universal, equilíbrio entre cartas ou eficácia em mesa. As hipóteses de convicção sobre autoridade e desejo de concluir uma criação permanecem fora desta revisão; não receberam códigos oficiais.

Os testes focais conferem contagens, códigos, módulos, fontes históricas, aplicação restrita do patch, listas d6 de G07, contrato de oito famílias e reprodução determinística das três cópias. Essas verificações estruturais não substituem leitura editorial independente, validação visual dos impressos ou teste com jogadores. A sincronização de catálogo, skill, aplicação, artes e PDFs pertence às etapas de integração da revisão.

Na geração desta revisão, os **cinco testes focais passaram**, inclusive após sincronizar U08. As três cópias geradas têm SHA256 `4dae5bb05ba6376bd09ac3d7bcf16a6307e159a236b66f1bef457fce4b897128`; o pós-voo de sintaxe e diff terminou sem falhas. Os quatro links relativos deste relatório foram conferidos no filesystem. Não houve teste com jogadores, impressão física, geração de PDF ou publicação por este gerador.
