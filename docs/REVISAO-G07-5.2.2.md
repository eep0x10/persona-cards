# G07: recusar, negociar e mudar de resposta

A revisão editorial **5.2.2**, na edição **5.2**, esclarece somente **G07 — Chamado e destino**. Permanecem **169 cartas: 153 de criação e 16 guias**, com as oito famílias obrigatórias. Nenhuma carta foi acrescentada, retirada ou recodificada. O ajuste nasce da leitura de ensaios autorais; não é prova de eficácia com jogadores.

## O que mudou na carta

O guia pede que se responda ao chamado **concreto**, distingue rejeitar uma condição de rejeitar o chamado e permite mudança posterior com registro da ordem. `Fato` ajuda a identificar o pedido, a oferta ou a situação. `Escolha` distingue:

- **Recuso:** não assumo o chamado.
- **Negocio:** considero assumi-lo se as condições mudarem.

O título, o código, o módulo, as cinco chaves `Chamado`, `Resposta`, `Fato`, `Crença` e `Escolha`, as seis opções de cada lista d6 e seus números continuam idênticos. O campo `Crença` também não mudou. Os rótulos da lista são pontos de partida; não substituem a descrição da ação nem decidem seu resultado.

## Quatro casos para interpretar a resposta

| Situação concreta | Primeira resposta | O que a distingue |
| --- | --- | --- |
| Uma cultivadora convida a capitã para uma festa. A capitã responde: “Não vou.” | Recuso | Ela não assume aquele convite. Pode desejar a amizade ou a festa e ainda assim não ir. |
| O convite inclui preparar a infusão com todos os brotos disponíveis. A capitã responde: “Vou se reservarmos brotos para o viveiro.” | Negocio as condições | Ela considera participar e propõe mudar a condição material. Ainda não existe acordo nem reserva garantida. |
| Alguém pede ensinar um enxerto fazendo todo o trabalho pelo aprendiz. A instrutora responde: “Não farei por você; posso demonstrar uma parte e acompanhar sua tentativa.” | Não recusa necessariamente ensinar | Ela rejeita o modo de execução pedido e propõe outro. Se ensinar era o chamado, considerar ensiná-lo sob novas condições é negociação. Se o pedido concreto era executar a peça, a recusa pode ter esse objeto: registre qual era o pedido, sem trocá-lo depois. |
| A capitã primeiro diz “Não vou”; após outra proposta, concorda em comparecer reservando brotos. | Recuso; depois negocio e aceito | A mudança é permitida. Registre a sequência e o que a motivou; não reescreva a primeira resposta como se sempre tivesse sido aceitação condicionada. |

Recusar não exige indiferença, e negociar não exige gentileza. Uma pessoa pode recusar uma ordem coercitiva ou negociar condições nocivas aos demais. Recusar uma condição, um meio, uma etapa ou uma execução não demonstra, sozinho, recusa do objetivo ou do chamado mais amplo.

## Registro em G07

1. **Chamado:** qual possibilidade surgiu? Identifique seu objeto concreto em vez de registrar apenas “convite” ou “dever”.
2. **Resposta:** qual foi a primeira postura diante desse chamado? Mostre uma fala, ação ou decisão compatível com o rótulo escolhido ou sorteado.
3. **Fato:** o que aconteceu e pode ser conferido? Separe contexto estabelecido, premissa autoral e resultado ainda incerto.
4. **Crença:** quem interpreta ou prevê o quê, com qual evidência? Uma previsão de fracasso não garante esse fracasso.
5. **Escolha:** qual ação cabe agora, que condições estão em discussão e o que continua aberto? Se houver resposta posterior diferente, anote-a depois da primeira, com a causa da mudança.

“Tento impedir o futuro” continua sendo uma postura inicial: tentar evitar uma previsão não a torna fato nem assegura seu impedimento. O guia não obriga aceitar o chamado, manter para sempre a primeira resposta ou sortear o desfecho.

Os arquivos dos ensaios anteriores permanecem primeiras versões para auditoria. Esta explicação não corrige retroativamente uma resposta incompatível nem transforma qualquer “não” em recusa do chamado: o objeto, o momento e a ação precisam sustentar a classificação.

## Fontes preservadas e reprodução

O [gerador](../deck/build_5_2.py) compõe a fonte histórica 5.1, a [expansão 5.2.0](../deck/expansao-5.2.json), o [patch 5.2.1](../deck/revisao-5.2.1.json) e, por último, o [patch exclusivo de G07](../deck/revisao-5.2.2.json). As três fontes anteriores não são reescritas. Os outros 168 objetos de carta permanecem idênticos em conteúdo à revisão 5.2.1.

```sh
python -X utf8 deck/build_5_2.py
python -X utf8 -m unittest discover -s tests -p test_deck_5_2.py
```

O teste focal confere preservação dos 168 objetos por SHA256 da serialização canônica, hashes das fontes congeladas, identidade de G07, ordem das cinco chaves, listas d6 e três cópias ativas idênticas. Também rejeita patches que tentem alterar outra carta ou a lista de respostas. Isso não substitui revisão semântica, inspeção visual dos PDFs ou leitura em mesa.
