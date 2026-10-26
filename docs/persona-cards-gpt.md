# Persona Cards 5.2 — instruções, cartas e exemplos

Método completo de oito famílias e G07; fontes 5.0/5.1 são históricas.

# Persona Cards

Conecte passado, interpretação, intenção e escolha. As cartas são convites narrativos; não determinam respostas de jogadores, diagnóstico ou destino.

## Material e edição

Leia [manual e cartas](../skills/persona-cards/references/deck.md) na primeira aplicação; use o [índice](../skills/persona-cards/references/indice.md) e `scripts/cards.py` para consultas. A fonte é [deck.json](../skills/persona-cards/references/deck.json): **5.2, revisão 5.2.0, 166 cartas — 150 de criação e 16 guias**. Nunca invente códigos e títulos oficiais. Veja [exemplos](../skills/persona-cards/references/exemplos.md) e [limites](../skills/persona-cards/references/revisao.md).

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

[PDFs 5.2](../skills/persona-cards/print/README.md): 166 cartas em A4, quatro por folha, 92 × 130 mm. Use 100% e virar na borda longa; teste uma folha antes do lote. Edições 5.0/5.1 são históricas. Conferência digital não comprova impressão física nem eficácia em mesa.

---

# Persona Cards 5.2 — revisão 5.2.0

**166 cartas em português: 150 de criação e 16 guias.** A criação completa usa uma carta OR, CV, D, F, V, L, P e N, mais G07 — Chamado e destino. As oito famílias são obrigatórias; U/G são consulta, nunca personalidade sorteada.

## Como jogar

1. Separe as famílias e escolha ou sorteie OR + CV + D + F + V + L + P + N. Leia a abertura e os campos reais de cada carta.
2. Conecte OR e CV por por isso, apesar disso ou mais tarde aprendi. Origem não determina culpa, trauma ou uma única convicção.
3. Diga o resultado D, a tentativa F e a expressão V. Em L, respeite a vontade de pessoas vivas e o alcance estabelecido para objetos, entidades ou memória de mortos. Concretize P como circunstância que muda a escolha.
4. N exige dois valores genuínos que a pessoa quer preservar. Se só descreve um obstáculo ou não cabe no recorte, troque ou ressorteie N; não omita a família. Não force culpa, conciliação ou redenção.
5. Consulte G07: registre chamado, resposta, fato, crença e escolha. Escolha ou use 1d6 nas listas abaixo. Recusar e renegociar continuam possíveis; destino não determina o resultado.
6. Acrescente nome, papel, competência e prazer cotidiano. Mostre uma tentativa em cena, aceite a resposta dos demais e registre a consequência observada.

## Chamado e destino — G07

O guia acompanha toda criação completa. As oito cartas descrevem a pessoa; G07 organiza sua resposta à situação. Escolha ou role 1d6 em cada uma das duas listas.

### Chamado

1. Pedido de alguém
2. Papel ou herança
3. Risco concreto
4. Encontro ou convite
5. Presságio ou profecia
6. Natureza, tempo ou finitude

### Resposta

1. Aceito
2. Recuso
3. Adio e investigo
4. Negocio as condições
5. Tento impedir o futuro
6. Busco cumprir por outro caminho

### Fato

O que está confirmado no mundo?

### Crença

Quem interpreta ou prevê algo, e com qual evidência?

### Escolha

O que você decide e o que ainda pode escolher? Não sorteie um desfecho.

No aplicativo, esses registros são `journey.call`, `response`, `fact`, `belief` e `choice`. Podem ser anotados em papel. Um valor não é uma afirmação factual: questione sua aplicação sem declará-lo um fato falso.

## Compatibilidade e histórico

Fichas 5.0/5.1 conservam nomes, textos, códigos e fotos, mas ficam como rascunhos pendentes no método 5.2 quando não têm as oito famílias e G07. Não se inventam novos passados ou valores na importação. A galeria de 105 inspirações oferece leituras autorais completas 5.2, com oito cartas, justificativas e G07; suas novas cenas são propostas, não eventos canônicos. Copiar uma base permite adaptar essa interpretação, sem alterar fichas existentes.

Os arquivos 5.0/5.1 são históricos. A edição 5.2 acrescenta OR/CV/G07 e atualiza orientações dos guias. Não se reescrevem retroativamente as avaliações anteriores como prova do novo método.

## Famílias

- **OR — Origem — o que aconteceu antes:** 12 cartas.
- **CV — Convicção — como interpreta e orienta escolhas:** 12 cartas.
- **D — Desejo — o que quer agora:** 24 cartas.
- **F — Forma de agir — como tenta:** 20 cartas.
- **V — Expressão — como comunica:** 22 cartas.
- **L — Vínculo — quem também quer algo:** 20 cartas.
- **P — Pressão — o que muda a situação:** 18 cartas.
- **N — Conflito interno — dois valores genuínos:** 22 cartas.
- **U — Guias de uso:** 9 cartas.
- **G — Guias de contexto:** 7 cartas.

## Cartas completas

## Origem — o que aconteceu antes

### OR01 — Uma ausência ficou (expansao_5_2)

> Alguém ou algo deixou de fazer parte da sua vida. A ausência continua tendo um lugar, mesmo quando você segue adiante.

**Pergunte:** O que se perdeu e o que você conserva? Perda não significa culpa; diga se existe alguma responsabilidade demonstrada.

**Mostre:** Mostre um costume, objeto ou escolha que ainda carrega essa presença.

**Contraste:** Pode sustentar cuidado com quem ficou ou uma tentativa de governar a vida dos outros para impedir novas perdas.

### OR02 — Eu deixei uma marca (expansao_5_2)

> Uma decisão sua mudou a vida de alguém. O que aconteceu continua existindo fora da versão que você conta.

**Pergunte:** O que você fez, que alternativa conhecia e quem sofreu ou ganhou com isso? Separe responsabilidade de remorso.

**Mostre:** Apresente uma consequência que outra pessoa ainda enfrenta; ela pode discordar da sua explicação.

**Contraste:** Pode gerar reparação concreta ou a defesa orgulhosa de um ato nocivo. Arrependimento não vem na carta.

### OR03 — Fui preparado para um papel (expansao_5_2)

> Antes de você escolher, alguém já dizia quem deveria ser. Parte do que aprendeu ainda serve; parte talvez já não caiba.

**Pergunte:** Quem ensinou esse papel, o que esperava e o que você incorporou, recusou ou ainda não decidiu?

**Mostre:** Mostre uma habilidade aprendida e uma expectativa que reaparece.

**Contraste:** Pode formar um sucessor dedicado, um dissidente ou alguém que impõe a outros o mesmo papel.

### OR04 — Alguém ficou ao meu lado (expansao_5_2)

> Houve quem lhe oferecesse tempo, abrigo ou confiança quando isso fez diferença. Esse gesto não determina o que você deve fazer agora.

**Pergunte:** O que recebeu e que significado deu ao gesto? Não presuma dívida nem reciprocidade.

**Mostre:** Mostre como recebe ajuda hoje: acolhe, desconfia, oferece a outra pessoa ou tenta comandar a relação.

**Contraste:** Pode inspirar solidariedade ou transformar cuidado recebido em sentimento de superioridade e proteção possessiva.

### OR05 — Saí quando esperavam que ficasse (expansao_5_2)

> Você atravessou uma porta que outras pessoas julgavam fechada. Sua saída abriu algo e deixou consequências para trás.

**Pergunte:** Do que saiu, por qual motivo e quem interpretou sua partida de outro jeito?

**Mostre:** Faça uma exigência antiga voltar por meio de uma pessoa com vontade própria.

**Contraste:** Pode ser emancipação legítima ou abandono de responsabilidades; a carta não absolve nem condena por antecipação.

### OR06 — Fiquei quando outros partiram (expansao_5_2)

> Você continuou onde a vida de outros seguiu outro caminho. Permanecer preservou alguma coisa e também mudou você.

**Pergunte:** O que escolheu sustentar e quais alternativas realmente tinha? Não trate quem partiu como covarde por padrão.

**Mostre:** Mostre algo que só existe porque você ficou, e alguém que deseja mudá-lo.

**Contraste:** Pode sustentar uma comunidade ou virar justificativa para cobrar obediência de quem chegou depois.

### OR07 — Meu esforço não bastou (expansao_5_2)

> Você tentou algo importante e não alcançou o resultado. O fracasso aconteceu; a explicação que lhe deu pode continuar em disputa.

**Pergunte:** Faltaram capacidade, recursos, informação, oportunidade ou controle? Não transforme resultado em medida de valor pessoal.

**Mostre:** Apresente uma situação parecida e mostre o que faz diferente — ou insiste em repetir.

**Contraste:** Pode ensinar prudência e colaboração ou produzir ressentimento e punição de pessoas usadas como culpadas.

### OR08 — O êxito cobrou um preço (expansao_5_2)

> Você conseguiu o que buscava. Nem tudo que veio com a vitória tinha sido escolhido ou pago por você.

**Pergunte:** Qual foi o ganho, quem arcou com o custo e o que você sabe disso hoje?

**Mostre:** Ofereça uma nova vantagem que repita parte desse custo.

**Contraste:** Pode gerar gratidão e responsabilidade ou a crença de que vencer justifica repetir qualquer método.

### OR09 — Conheci um mundo seguro (expansao_5_2)

> Você teve um lugar onde podia existir sem provar seu valor o tempo todo. Isso pode ser uma força real, sem tragédia escondida.

**Pergunte:** O que tornava esse cotidiano bom e o que você aprendeu com ele?

**Mostre:** Mostre um hábito simples que tenta levar a outro ambiente.

**Contraste:** Pode ampliar hospitalidade ou sustentar a exigência de que todos vivam sob uma única ideia de ordem e normalidade.

### OR10 — Aprendi duas formas de viver (expansao_5_2)

> Você conheceu modos diferentes de habitar o mundo. Nenhum precisa virar caricatura para que a diferença importe.

**Pergunte:** Que práticas ou critérios entram em contraste, e onde você encontrou lugar entre eles?

**Mostre:** Mostre uma decisão em que reconhece mais de uma resposta possível.

**Contraste:** Pode formar uma ponte entre pessoas ou alguém que explora divisões para se tornar indispensável.

### OR11 — O tempo mudou o que eu conhecia (expansao_5_2)

> O mundo seguiu enquanto você seguia também. Uma coisa que parecia duradoura mudou antes que percebesse seu valor.

**Pergunte:** O que passou, o que só entendeu depois e o que ainda pode viver agora?

**Mostre:** Reencontre um lugar, costume ou pessoa sem exigir que permaneça como na lembrança.

**Contraste:** Pode abrir atenção ao presente ou alimentar uma tentativa autoritária de congelar o mundo.

### OR12 — Descobri algo que me prende à vida (expansao_5_2)

> Uma prática, descoberta ou encontro fez o mundo ficar maior. Nem todo começo precisa vir de uma ferida.

**Pergunte:** O que despertou esse interesse e por que ainda importa? Ele não precisa ser um chamado heroico.

**Mostre:** Mostre o prazer de fazer algo bem, mesmo sem público ou recompensa.

**Contraste:** Pode sustentar dedicação generosa ou uma obsessão que trata outras pessoas como matéria da própria obra.

## Convicção — como interpreta e orienta escolhas

### CV01 — Sem controle, tudo se perde (expansao_5_2)

> Você procura segurança em poder antecipar e dirigir o que acontece. Resta saber quanto controle a situação permite e quem fica sem escolha.

**Pergunte:** Em que situação essa regra parece necessária? O que faria diante de alguém capaz que não obedece?

**Mostre:** Outra pessoa resolve um problema de um jeito que você não autorizou. Mostre sua resposta.

**Contraste:** Pode orientar preparação responsável ou domínio coercitivo. Crenças factuais sobre controle podem ser confrontadas; a preferência por ordem é um valor.

### CV02 — Meu valor precisa ser conquistado (expansao_5_2)

> Você mede parte de quem é por uma prova que ainda precisa passar. Talvez ninguém de fora tenha pedido essa prova.

**Pergunte:** O que contaria como suficiente, quem definiu esse critério e o que um fracasso significaria para você?

**Mostre:** Alguém lhe oferece consideração antes da conquista. Diga o que faz com isso.

**Contraste:** Pode mover dedicação ou uma busca de prestígio que humilha quem ameaça o reconhecimento.

### CV03 — Cuidar é estar presente (expansao_5_2)

> Para você, cuidado precisa caber em tempo e gesto. Outra pessoa pode desejar um cuidado diferente do que oferece.

**Pergunte:** Por quem quer estar disponível e como percebe quando presença vira intromissão?

**Mostre:** Um vínculo pede espaço quando você queria ajudar.

**Contraste:** Pode produzir apoio atento ou vigilância possessiva. O valor do cuidado não prova que seu método ajuda.

### CV04 — Não vou repetir aquele dano (expansao_5_2)

> Há um tipo de consequência que você decidiu não produzir nem ajudar a repetir. Essa decisão precisa aparecer no meio que aceita usar.

**Pergunte:** Qual dano quer evitar e em que situação seria difícil sustentar esse limite?

**Mostre:** Surge uma solução eficaz que repete parte do dano. Declare a escolha e quem assume seu custo.

**Contraste:** Pode sustentar um limite ético ou uma prevenção extrema que faz inocentes pagar por um risco.

### CV05 — Ninguém escolhe por mim (expansao_5_2)

> Você quer reconhecer a própria mão nas decisões da sua vida. Isso não torna a vontade dos outros uma extensão da sua.

**Pergunte:** Que escolha reivindica e que escolhas alheias está disposto a respeitar?

**Mostre:** Alguém apresenta uma obrigação, uma previsão ou um conselho como se já fosse sua decisão.

**Contraste:** Pode sustentar emancipação ou a exigência de liberdade apenas para si.

### CV06 — Há algo a preservar em cada vida (expansao_5_2)

> Você reconhece valor numa existência para além da utilidade que ela tem agora. O alcance desse valor se revela nas decisões difíceis.

**Pergunte:** Quem costuma ficar fora da sua atenção e o que preservar uma vida exige neste contexto?

**Mostre:** Uma pessoa hostil fica dependente de uma decisão sua.

**Contraste:** Pode sustentar compaixão ou ser usado para justificar aprisionamento e tutela contra a vontade de alguém. Não implica pacifismo automático.

### CV07 — É melhor saber do que viver enganado (expansao_5_2)

> Você atribui valor a compreender o que acontece, mesmo quando a descoberta pode tirar um consolo ou uma vantagem.

**Pergunte:** A quem deve essa verdade, que acesso considera legítimo e o que faria diante de incerteza?

**Mostre:** Uma informação útil também expõe alguém que não autorizou sua divulgação.

**Contraste:** Pode sustentar investigação responsável ou uma cruzada que desconsidera privacidade e consequências.

### CV08 — Depender de alguém me deixa à mercê (expansao_5_2)

> Quando precisa de outra pessoa, você enxerga também a possibilidade de perder espaço, proteção ou saída.

**Pergunte:** Que risco prevê e que experiência o faz acreditar nisso? É previsão factual, não verdade decretada pela carta.

**Mostre:** Recebe ajuda que não consegue retribuir imediatamente. Mostre o que tenta manter sob seu controle.

**Contraste:** Pode orientar cautela e limites ou isolamento, manipulação e desconfiança mesmo sem evidência suficiente.

### CV09 — A palavra vale mais que a vantagem (expansao_5_2)

> O compromisso que assumiu continua pesando quando aparece uma oportunidade melhor. Nem toda promessa foi livre, justa ou possível.

**Pergunte:** Que compromisso reconhece como seu e o que considera motivo legítimo para renegociá-lo?

**Mostre:** Outra pessoa pede que reveja um acordo que a prejudica.

**Contraste:** Pode sustentar confiabilidade ou fidelidade a uma ordem nociva. Não declara que cumprir sempre é a escolha correta.

### CV10 — Viver também é deixar partir (expansao_5_2)

> Você tenta continuar sem exigir que tudo permaneça sob a mesma forma. Aceitar uma perda não apaga o que importou.

**Pergunte:** O que pode soltar, o que ainda pode reparar e como distingue aceitação de abandono?

**Mostre:** Uma oportunidade de conservar algo cobra impedir a vida de outra pessoa.

**Contraste:** Pode sustentar despedida e renovação ou servir de desculpa para descartar pessoas e fugir de reparações possíveis.

### CV11 — O fim dá sentido ao custo (expansao_5_2)

> Você aceita pagar por um resultado que considera grande. A decisão muda quando o preço deixa de ser só seu.

**Pergunte:** Quem escolhe o objetivo, quem paga e quem pode recusar? Diga se existe um limite real; não invente um.

**Mostre:** Alguém atingido pelo plano rejeita o sacrifício que você considera necessário.

**Contraste:** Pode orientar um risco pessoal voluntário ou uma doutrina que transforma vidas alheias em recurso.

### CV12 — O que termina também pode valer (expansao_5_2)

> Uma experiência não precisa durar para sempre para merecer seu tempo. Você ainda escolhe em que presença investir.

**Pergunte:** O que vale viver mesmo sabendo que vai acabar, e por que isso importa agora?

**Mostre:** Surge um encontro breve que não favorece seu projeto de longo prazo.

**Contraste:** Pode sustentar atenção e coragem diante da finitude ou justificar gratificação que ignora compromissos e consequências.

## Desejo — o que quer agora

### D01 — Ter meu lugar (nucleo)

> Você procura um lugar onde sua presença conte, não apenas um convite para entrar.

**Quero:** Entrar em [grupo] com direito a [participação].

**Mostre:** Assume uma tarefa comum e pede um lugar à mesa.

**Pedido:** Peça uma apresentação; ofereça uma contribuição.

### D02 — Assinar uma conquista (nucleo)

> Há uma conquista sua que ainda leva outro nome. O que mudaria se fosse reconhecida?

**Quero:** Receber crédito por [feito] de [pessoa].

**Mostre:** Mostra uma amostra do que sabe fazer.

**Pedido:** Peça testemunhas ou uma chance; ofereça seu talento.

### D03 — Escolher meu caminho (nucleo)

> O caminho está posto, mas você quer poder escolhê-lo por conta própria.

**Quero:** Decidir sobre [assunto] sem [imposição].

**Mostre:** Compara condições antes de aceitar.

**Pedido:** Peça uma alternativa; diga qual compromisso aceita.

### D04 — Garantir proteção (nucleo)

> Algo importa o bastante para você vigiar o risco e preparar um abrigo.

**Quero:** Manter [alguém ou lugar] seguro até [marco].

**Mostre:** Confere um risco e prepara ajuda.

**Pedido:** Peça um recurso; ouça quem será protegido.

### D05 — Obter reparação (nucleo)

> Um dano pede resposta concreta. Que reparação seria suficiente para você?

**Quero:** Reparar [dano] por meio de [medida].

**Mostre:** Apresenta o prejuízo e uma reparação possível.

**Pedido:** Peça apoio ou prova; diga quando bastará.

### D06 — Resolver uma pergunta (nucleo)

> Uma pergunta não o deixa em paz. Siga a pista, mesmo se ela contrariar sua hipótese.

**Quero:** Descobrir por que [fenômeno] acontece.

**Mostre:** Testa uma hipótese e aceita evidência contrária.

**Pedido:** Peça acesso; ofereça compartilhar a descoberta.

### D07 — Fazer algo durar (nucleo)

> Você quer que uma obra sobreviva às suas mãos. A quem confiaria o próximo passo?

**Quero:** Deixar [obra ou prática] nas mãos de [sucessor].

**Mostre:** Ensina um passo ou restaura uma parte.

**Pedido:** Peça material ou aprendiz; entregue conhecimento.

### D08 — Ter recursos suficientes (nucleo)

> Você sabe o que falta para realizar um projeto. Quanto será bastante?

**Quero:** Reunir [quantidade] para realizar [projeto].

**Mostre:** Conta o que falta e propõe uma troca.

**Pedido:** Peça trabalho ou recurso; defina quanto é suficiente.

### D09 — Viver uma experiência (nucleo)

> Existe algo que você quer viver, sem transformá-lo em prêmio ou obrigação.

**Quero:** Viver [experiência] com [companhia].

**Mostre:** Prepara uma pequena amostra do prazer esperado.

**Pedido:** Convide o grupo; ofereça uma experiência concreta.

### D10 — Ampliar minha influência (nucleo)

> Você quer ter poder sobre uma decisão. Que autoridade procura, e quem poderá contestá-la?

**Quero:** Obter [autoridade] para decidir [assunto].

**Mostre:** Busca apoio, acesso ou posição que lhe permita decidir; descreva como usa esse poder.

**Interação:** Declare a autoridade pretendida e a margem real de recusa dos demais. Só atribua um limite se a pessoa o reconhecer.

### D11 — Cumprir minha palavra (nucleo)

> Sua palavra criou uma expectativa. O que ainda precisa fazer para cumpri-la?

**Quero:** Entregar [promessa] a [pessoa] até [marco].

**Mostre:** Confere o que ainda falta cumprir.

**Pedido:** Peça ajuda específica; diga o que já prometeu.

### D12 — Abrir um horizonte (nucleo)

> Uma possibilidade ainda não existe para essas pessoas. Você tenta abri-la.

**Quero:** Abrir [rota ou possibilidade] para [pessoas].

**Mostre:** Experimenta um caminho ainda indisponível.

**Pedido:** Peça parceiros para um primeiro teste.

### D13 — Continuar vivo (expansao)

> Uma ameaça pesa sobre sua continuidade. Você tenta atravessar este perigo ou impedir que ele volte a alcançá-lo?

**Quero:** Preservar minha vida diante de [ameaça], buscando [condição de sobrevivência].

**Mostre:** Procura uma saída imediata ou uma proteção duradoura; diga qual delas orienta a próxima ação.

**Interação:** Peça, exija ou procure o recurso necessário. Não presuma que desejar sobreviver determina os meios ou um limite moral.

### D14 — Encontrar intimidade (expansao)

> Você deseja se aproximar. O convite pode ser sincero sem exigir resposta igual.

**Quero:** Construir proximidade com [pessoa] sem presumir reciprocidade.

**Mostre:** Oferece presença ou revela algo pessoal.

**Interação:** Faça um convite; a outra pessoa pode não querer o mesmo.

### D15 — Entender quem sou (expansao)

> A ideia que tinha de si talvez não baste. O que sua experiência mostra?

**Quero:** Reconhecer que papel ou identidade corresponde à minha experiência.

**Mostre:** Compara uma crença sobre si com o que vive.

**Interação:** Peça uma prova, escuta ou espaço para experimentar.

### D16 — Reparar minha própria falta (expansao)

> Você reconhece uma falta sua e procura responder por ela. A outra pessoa decide o que aceita.

**Quero:** Responder pelo que fiz e viver de outro modo.

**Mostre:** Nomeia uma responsabilidade e tenta um gesto de reparação.

**Interação:** Defina o que assume; perdão alheio não é garantido.

### D17 — Reaver o que considero meu (expansao)

> Algo lhe foi tirado, ou você crê que lhe pertence. Sua reivindicação pode ser contestada.

**Quero:** Recuperar [objeto, lugar ou posição] pelo valor que tem em si.

**Mostre:** Persegue uma pista ou impede que alguém leve o alvo.

**Interação:** Declare a reivindicação; ela pode ser contestada.

### D18 — Romper uma ordem (expansao)

> Uma ordem sustenta o que você quer desfazer. Qual apoio dela pode ser atingido?

**Quero:** Desfazer [regra, sistema ou crença coletiva] que quero ver cair.

**Mostre:** Ataca um apoio concreto dessa ordem.

**Interação:** Provoque uma reação; não exige querer governar depois.

### D19 — Punir quem causou o dano (expansao_5)

> Você quer que o responsável pague pelo dano. Punir e reparar não são a mesma escolha.

**Quero:** Fazer [responsável] pagar por [dano], por meio de [punição pretendida].

**Mostre:** Escolhe o alvo e a forma de retribuição; reparar a vítima pode ser outro objetivo.

**Pergunte:** Que resultado encerraria a busca? Pode não haver limite reconhecido nem encerramento possível.

### D20 — Sair de um fardo (expansao_5)

> Há um peso que você não consegue continuar carregando. Nomeie o que precisa cessar sem decidir a saída por antecipação.

**Quero:** Deixar de suportar [papel, lembrança ou condição] que tornou a continuidade insuportável.

**Mostre:** Tenta escapar, desaparecer ou interromper uma obrigação; registre a intenção concreta sem presumir desejo de viver.

**Pergunte:** O que quer que cesse? Que saída percebe e que possibilidades desconhece? Não determine a saída nem imponha recuperação.

### D21 — Cumprir uma obrigação (expansao_5)

> Um dever orienta seus passos. Descubra de onde veio e quanto espaço deixa para sua interpretação.

**Quero:** Executar [dever] recebido de [papel, instituição, herança ou programação], até [condição de cumprimento].

**Mostre:** Consulta o mandato e age pelo que ele exige, mesmo sem promessa pessoal.

**Pergunte:** É escolha, obrigação ou protocolo? Quanto pode interpretar, recusar ou aprender? Não atribua vontade autônoma sem evidência.

### D22 — Provar meu valor a mim (expansao_5)

> A prova que você busca é para si. O aplauso de outros talvez não resolva nada.

**Quero:** Conseguir [feito ou decisão] que me permita reconhecer [qualidade própria], mesmo sem aplauso.

**Mostre:** Escolhe uma medida pessoal de dignidade, capacidade ou respeito por si.

**Pergunte:** Que prova aceitaria? Não confunda reconhecimento público, descoberta de identidade e valor pessoal.

### D23 — Exercer minha vocação (expansao_5)

> A própria prática lhe dá sentido. Onde ela cabe entre as outras partes da sua vida?

**Quero:** Viver ou praticar [atividade] porque fazê-la dá sentido à minha vida.

**Mostre:** Procura tempo, meios ou ocasião para praticar, mesmo sem prêmio ou fama.

**Pergunte:** O que a prática oferece que o reconhecimento não substitui? Ela pode nutrir ou consumir outras partes da vida.

### D24 — Controlar a imagem que deixo (expansao_5)

> Você quer governar a imagem que deixam de você. Quem conhece outra versão?

**Quero:** Fazer [público ou pessoa] acreditar que sou [imagem], independentemente do que ocorreu.

**Mostre:** Seleciona sinais, relatos e comparações que sustentem sua reputação ou versão da história.

**Pergunte:** Que impressão precisa manter? Quem pode contradizê-la? Objetivo de imagem não implica querer descobrir ou revelar identidade.

## Forma de agir — como tenta

### F01 — Planejo antes (nucleo)

> Você organiza antes de agir. Quando o preparo protege, e quando faz perder a hora?

**Faço:** Divido a tarefa em etapas e preparo recursos.

**Ajuda:** As pessoas sabem o próximo passo.

**Custa:** A preparação pode consumir a oportunidade.

### F02 — Faço uma troca (nucleo)

> Você oferece algo em troca de algo. Deixe claro o acordo antes de cobrar.

**Faço:** Ofereço algo e estabeleço o retorno.

**Ajuda:** Interesses diferentes podem virar acordo.

**Custa:** A cobrança pode romper confiança; diga o que ficou explícito.

### F03 — Defendo um princípio (nucleo)

> Você declara um princípio e o segue. Que caso concreto desafia essa firmeza?

**Faço:** Nomeio uma convicção e ajo por ela.

**Ajuda:** Minha posição fica compreensível.

**Custa:** Posso ignorar uma exceção ou um custo que contraria a convicção.

### F04 — Faço disso uma disputa (nucleo)

> Você transforma a tarefa em disputa. Lembre o que pretendia fazer antes de querer vencer.

**Faço:** Transformo uma tarefa em disputa por resultado ou posição.

**Ajuda:** A comparação mobiliza esforço.

**Custa:** Posso tratar um parceiro como obstáculo ou perder o motivo da tarefa.

### F05 — Aproveito o momento (nucleo)

> Você percebe o prazer possível agora. Ele pode alimentar a ação ou adiá-la.

**Faço:** Trago um prazer presente para a decisão.

**Ajuda:** As pessoas celebram e percebem o momento.

**Custa:** Uma tarefa necessária pode ser adiada.

### F06 — Aposto na possibilidade (nucleo)

> Você tenta mesmo sem garantia. Nomeie o risco e quem o divide com você.

**Faço:** Tento uma possibilidade antes de ter garantia.

**Ajuda:** Um caminho novo pode aparecer.

**Custa:** Defina a perda possível e quem assume o risco comigo.

### F07 — Aproximo as partes (nucleo)

> Você procura uma linguagem comum para lados diferentes. Sua própria posição também importa.

**Faço:** Traduzo o que cada parte está pedindo.

**Ajuda:** Um impasse pode virar negociação.

**Custa:** Posso adiar a posição que alguém precisa de mim.

### F08 — Ofereço primeiro (nucleo)

> Você começa oferecendo ajuda. Verifique o que é seu para oferecer.

**Faço:** Entrego uma ajuda antes de pedir.

**Ajuda:** A colaboração começa por uma prova concreta.

**Custa:** Posso prometer recursos compartilhados sem consultar.

### F09 — Guardo meu espaço (nucleo)

> Você guarda tempo, informação ou intimidade. Diga onde termina o seu limite.

**Faço:** Declaro o que compartilho e o que reservo.

**Ajuda:** Preservo foco, tempo e autonomia.

**Custa:** Alguém pode ficar sem informação necessária.

### F10 — Vou ao que funciona (nucleo)

> Você pergunta o que funciona. Observe também o que o procedimento significa para os outros.

**Faço:** Escolho pelo resultado observável.

**Ajuda:** O problema avança sem depender de prestígio ou ritual.

**Custa:** Posso ignorar o efeito simbólico ou humano do procedimento.

### F11 — Mudo conforme o terreno (nucleo)

> Você muda o plano quando o terreno muda. Avise quem contava com a decisão anterior.

**Faço:** Explico o que mudou e ajusto o método.

**Ajuda:** O plano responde a novas informações.

**Custa:** Alguém pode ter contado com minha decisão anterior.

### F12 — Sustento os meus (nucleo)

> Você permanece ao lado dos seus. Apoio e favorecimento podem se parecer de longe.

**Faço:** Fico ao lado de quem assumiu laço comigo.

**Ajuda:** As pessoas têm apoio também quando falham.

**Custa:** Posso favorecer os próximos num caso injusto.

### F13 — Pressiono e controlo (expansao)

> Você usa a vantagem para obter obediência. O resultado não transforma coerção em acordo.

**Faço:** Uso ameaça, restrição ou poder para obter uma conduta.

**Ajuda:** Posso conseguir obediência enquanto mantenho a vantagem.

**Custa:** Consentimento não é garantido; oposição pode crescer.

### F14 — Oculto e enceno (expansao)

> Você escolhe o que mostrar e o que ocultar. Toda encenação deixa uma borda exposta.

**Faço:** Escondo intenção ou represento um papel para produzir uma impressão.

**Ajuda:** Consigo acesso, proteção ou influência pela aparência.

**Custa:** Uma contradição pode expor a encenação e romper confiança.

### F15 — Insisto além do custo (expansao)

> Você insiste depois que o custo aparece. O que continua avançando, e quem está pagando?

**Faço:** Repito a tentativa mesmo quando o desgaste se torna visível.

**Ajuda:** Posso avançar onde outros já teriam parado.

**Custa:** Corpo, relações ou recursos pagam a insistência.

### F16 — Avalio perigos (expansao)

> Você procura perigos antes do primeiro passo. Separe sinal observado de suspeita.

**Faço:** Procuro sinais de risco e testo se a saída é segura.

**Ajuda:** Percebo ameaças que passariam despercebidas.

**Custa:** Posso paralisar, controlar demais ou suspeitar sem prova.

### F17 — Tomo a frente (expansao)

> Você toma a frente quando falta direção. Deixe espaço para quem também terá de agir.

**Faço:** Distribuo tarefas e decido como a ação começa.

**Ajuda:** Dou direção quando falta coordenação.

**Custa:** Posso retirar espaço de decisão ou errar por não ouvir.

### F18 — Sigo ao pé da letra (expansao)

> Você segue os termos exatos. Uma ordem clara ainda pode deixar uma intenção de fora.

**Faço:** Executo instrução ou regra segundo seus termos explícitos.

**Ajuda:** Entregas ficam previsíveis e verificáveis.

**Custa:** Uma intenção implícita ou exceção pode passar despercebida.

### F19 — Uso âncoras externas (expansao_5)

> Você usa notas, rituais ou instruções para seguir. Confira quem fez a âncora e se ainda vale.

**Faço:** Registro, consulto ou repito [nota, ritual ou instrução] para orientar minha próxima ação.

**Ajuda:** Posso agir quando lembrar, ordenar ou conferir tudo internamente não é viável.

**Custa:** Uma âncora incompleta, desatualizada ou manipulada pode orientar mal. Registre autoria e acesso sem garantir que o registro seja verdadeiro.

### F20 — Recuo para suportar (expansao_5)

> Você se afasta do que não consegue enfrentar agora. A distância pode proteger e também deixar algo sem resposta.

**Faço:** Evito, interrompo ou me afasto de uma exposição que não consigo enfrentar agora.

**Ajuda:** Ganho distância, alívio ou tempo para continuar.

**Custa:** Uma necessidade pode permanecer sem resposta e alguém pode não saber por que me afastei. Pode ser proteção sob coerção, não decisão plenamente livre.

## Expressão — como comunica

### V01 — Perguntas que delimitam (nucleo)

> Você recorta a conversa com perguntas precisas. Cada resposta abre a próxima.

**Faça:** Pergunta curta; aponta uma condição de cada vez.

**Ensaie:** “Até quando? Quem pode autorizar?”

**Subtexto:** Pode esclarecer, testar ou ganhar tempo.

### V02 — Cuidado pelas mãos (nucleo)

> Suas mãos fazem parte da fala. Um pequeno cuidado pode dizer muito.

**Faça:** Cuide de algo com as mãos; a fala pode ser breve ou ausente.

**Ensaie:** Ajuste a alça, aproxime o objeto e espere; ou diga: “Eu seguro.”

**Subtexto:** O gesto pode acolher, reparar ou evitar exposição.

### V03 — Imagens do cotidiano (nucleo)

> Você traduz uma ideia em objeto ou imagem cotidiana que ambos conhecem.

**Faça:** Compara com algo do cotidiano; usa um objeto.

**Ensaie:** “Esse acordo é ponte: precisa apoiar dos dois lados.”

**Subtexto:** Pode explicar, persuadir ou diminuir tensão.

### V04 — Conclusão primeiro (nucleo)

> Você entrega a conclusão primeiro e deixa o silêncio carregar a reação.

**Faça:** Entregue a conclusão em poucas palavras; pause antes do motivo.

**Ensaie:** “Saímos hoje.” Aponte a rota e espere a reação.

**Subtexto:** Pode orientar, proteger ou encerrar uma discussão.

### V05 — Termos cuidadosos (nucleo)

> Você escolhe os termos com atenção. Uma palavra corrigida muda a promessa.

**Faça:** Escolhe termos e corrige uma palavra.

**Ensaie:** “Posso garantir o acesso. O resultado, ainda não.”

**Subtexto:** Pode limitar promessa, negociar ou esconder insegurança.

### V06 — Lembrança breve (nucleo)

> Você traz uma lembrança breve para iluminar o que acontece agora.

**Faça:** Conta uma lembrança curta; volta ao presente.

**Ensaie:** “Na última travessia faltou corda. Trouxe duas.”

**Subtexto:** Pode alertar, criar intimidade ou justificar cautela.

### V07 — Raciocínio em voz alta (nucleo)

> Você pensa em voz alta e permite que a hipótese mude diante de outros.

**Faça:** Expõe uma hipótese e a revê em voz alta.

**Ensaie:** “Se o selo é novo... então alguém voltou aqui.”

**Subtexto:** Pode investigar, convidar ajuda ou buscar confirmação.

### V08 — Atenção pessoal (nucleo)

> Você se lembra de um detalhe pessoal. Use-o com atenção à pessoa, não apenas ao argumento.

**Faça:** Retome um detalhe pessoal que ouviu.

**Ensaie:** “Você falou da sua irmã. Isso muda sua resposta?”

**Subtexto:** Pode cuidar, investigar ou usar o detalhe como argumento.

### V09 — Entusiasmo que convida (nucleo)

> Sua energia abre uma tarefa compartilhada. Convide para uma parte concreta.

**Faça:** Fala com energia; oferece participação concreta.

**Ensaie:** “Tenho uma ideia! Você testa e eu preparo o resto?”

**Subtexto:** Pode mobilizar, compartilhar prazer ou pedir coragem.

### V10 — Humor que muda o ângulo (nucleo)

> Seu humor muda o ângulo da cena. Veja se alguém riu com você.

**Faça:** Mude o ângulo com humor e observe a reação.

**Ensaie:** “A porta venceu. Tentamos a janela?”

**Subtexto:** Pode aliviar, criticar, disfarçar ou marcar superioridade.

### V11 — Passo a passo (nucleo)

> Você organiza o pensamento em passos que o outro consegue acompanhar.

**Faça:** Enumera passos; marca cada um com os dedos.

**Ensaie:** “Primeiro guardamos isto. Depois ouvimos os dois.”

**Subtexto:** Pode ensinar, organizar ou recuperar controle.

### V12 — Convite à participação (nucleo)

> Sua proposta deixa uma abertura real para a resposta e para a mudança.

**Faça:** Deixa espaço real para a resposta.

**Ensaie:** “É minha proposta. O que precisa mudar para você?”

**Subtexto:** Pode incluir, negociar ou dividir responsabilidade.

### V13 — Silêncio que comunica (expansao)

> Você pode dizer muito sem palavras. Dê tempo para o gesto receber resposta.

**Faça:** Use olhar, distância, gesto ou objeto no lugar de fala.

**Ensaie:** Estenda a mão, recue ou entregue algo; espere a resposta.

**Subtexto:** Pode reservar, desejar, recusar ou pedir sem palavras.

### V14 — Literalidade (expansao)

> Você leva as palavras ao pé da letra e pede a precisão de que precisa.

**Faça:** Responda aos termos exatos, com pouca inferência social.

**Ensaie:** “A ordem é proteger. Defina quem não pode ser ferido.”

**Subtexto:** Pode buscar precisão, obedecer ou mostrar desencontro.

### V15 — Fala cerimonial (expansao)

> Sua fala dá forma pública a um papel, voto ou compromisso.

**Faça:** Use cadência solene e referências ao papel que representa.

**Ensaie:** “Por este compromisso, assumo a guarda da passagem.”

**Subtexto:** Pode legitimar, inspirar ou sustentar uma identidade.

### V16 — Encanto calculado (expansao)

> Você mede o ritmo e a atenção da conversa para conduzi-la.

**Faça:** Cuide do ritmo, da atenção e da oferta para conduzir a conversa.

**Ensaie:** “Tenho o que deseja. Antes, uma pergunta sobre você.”

**Subtexto:** Pode seduzir, negociar ou intimidar com cortesia.

### V17 — Registros alternados (expansao)

> Seu registro muda com a posição que ocupa. Mostre o contraste sem inventar sua causa.

**Faça:** Mude pronome, ritmo ou vocabulário ao mudar de posição.

**Ensaie:** Repita a questão em dois tons; deixe claro o contraste.

**Subtexto:** Pode mostrar papel encenado ou posições internas em conflito.

### V18 — Fala contida (expansao)

> Você reduz, pausa ou corrige a fala antes de se expor demais.

**Faça:** Use pausa, correção ou frase curta para conter exposição.

**Ensaie:** “Eu... posso tentar. Não é isso que quero dizer.”

**Subtexto:** Pode esconder receio, controlar emoção ou pedir espaço.

### V19 — Língua em sinais (expansao_5)

> Você se expressa em língua de sinais completa. Defina quem compreende o que comunica.

**Faça:** Comunica intenção por uma língua de sinais com estrutura própria; defina o que a outra pessoa compreende.

**Ensaie:** Descreva o conteúdo comunicado e se há confirmação ou tradução, sem inventar sinais reais.

**Subtexto:** Expressão, ritmo e escolha do conteúdo podem mostrar intenção. Língua de sinais não é ausência de linguagem nem sinônimo de silêncio.

### V20 — Palavras que ficam (expansao_5)

> Você deixa palavras para serem recebidas em outro tempo. A distância também faz parte da mensagem.

**Faça:** Escreve, grava ou consulta palavras destinadas a outro momento ou interlocutor.

**Ensaie:** Registre destinatário, conteúdo, autoria e distância entre escrever e reler.

**Subtexto:** Uma carta ou nota pode dizer o que ainda não consegue declarar. O meio não garante memória fiel, sinceridade ou leitura imediata.

### V21 — Imagens que carregam sentido (expansao_5)

> Uma imagem ou um ritmo comunica aquilo que a explicação direta empobreceria.

**Faça:** Usa uma imagem poética, ritmo ou associação sensorial para dizer algo que a exposição direta empobreceria.

**Ensaie:** Escolha uma imagem coerente com sua experiência e diga o que ela deixa implícito; não copie uma fala conhecida.

**Subtexto:** Pode mostrar assombro, despedida ou distância. Não precisa de cerimônia, autoridade ou metáfora cotidiana.

### V22 — Vocabulário próprio (expansao_5)

> Seu vocabulário revela repertório e pertencimento. Crie-o sem caricaturar um grupo real.

**Faça:** Emprega palavras, gírias ou combinações recorrentes ligadas à sua comunidade ou repertório pessoal.

**Ensaie:** Defina duas escolhas de linguagem, uma ocasião de uso e o que o interlocutor entende.

**Subtexto:** O vocabulário situa pertencimento, estilo ou poder. Evite caricatura de grupo real; escolha expressões originais sem copiar bordões.

## Vínculo — quem também quer algo

### L01 — Amizade que descansa (nucleo)

> Há alguém com quem você pode simplesmente estar. O que essa pessoa quer hoje?

**Laço:** Amigo com quem divide uma rotina ou um prazer.

**Outra pessoa:** Pergunte o que ele quer agora, mesmo fora da amizade.

**Em cena:** Que tempo, ritual ou limite esse pedido afeta?

### L02 — Rival que admiro (nucleo)

> Você disputa com alguém cuja qualidade reconhece. A rivalidade não apaga o respeito.

**Laço:** Alguém disputa um objetivo e tem uma qualidade que respeita.

**Outra pessoa:** Defina o que quer vencer e qual regra aceita.

**Em cena:** Que resultado aproxima ou afasta vocês?

### L03 — Sócio de outra ideia (nucleo)

> Vocês fizeram algo juntos e agora imaginam futuros diferentes para o que construíram.

**Laço:** Vocês construíram algo juntos e divergem do próximo passo.

**Outra pessoa:** Defina seu projeto e o recurso compartilhado.

**Em cena:** Como cada um pretende usar o que pertence aos dois?

### L04 — Favor com história (nucleo)

> Uma ajuda antiga chega à conversa de hoje. Foi presente, acordo ou dívida?

**Laço:** Uma ajuda passada deixou gratidão ou dívida.

**Outra pessoa:** Defina o pedido atual e o que considera devido.

**Em cena:** A ajuda era presente, acordo ou foi entendida de outro jeito?

### L05 — Quem viu minha mudança (nucleo)

> Essa pessoa conheceu quem você era. Ela vê quem você se tornou?

**Laço:** Alguém conhece uma versão anterior de você.

**Outra pessoa:** Defina o que quer hoje e o que pensa que ainda é igual.

**Em cena:** Que hábito atual confirma ou desfaz essa impressão?

### L06 — Quem aprendeu comigo (nucleo)

> Você ensinou; a outra pessoa aprendeu e escolhe o que fazer com isso.

**Laço:** Alguém recebeu seu ensino e agora tenta algo próprio.

**Outra pessoa:** Defina sua aplicação, inclusive uma que você desaprove.

**Em cena:** Você apoia, impõe condição ou tenta impedir? Por quê?

### L07 — Quem me orienta (nucleo)

> Alguém oferece direção por experiência ou poder. Onde começa a sua decisão?

**Laço:** Uma pessoa orienta você por experiência ou autoridade.

**Outra pessoa:** Defina seu projeto e os critérios que defende.

**Em cena:** Que conselho aceita e onde começa sua decisão?

### L08 — Companhia de estrada (nucleo)

> Vocês seguem pela mesma estrada com prioridades que podem não coincidir.

**Laço:** Vocês dividem uma jornada ou missão.

**Outra pessoa:** Defina destino, prioridade ou limite próprio.

**Em cena:** Que parte da rota ou do plano precisa combinar?

### L09 — Responsabilidade escolhida (nucleo)

> Você escolheu cuidar de alguém. A pessoa cuidada ainda pode escolher por si.

**Laço:** Você assumiu cuidado ou proteção de alguém.

**Outra pessoa:** Defina uma decisão que essa pessoa quer tomar.

**Em cena:** Onde cuidado vira interferência, abandono ou apoio?

### L10 — Afeto com divergência (nucleo)

> Você gosta de alguém que discorda de você. O afeto não precisa encerrar a discussão.

**Laço:** Uma pessoa querida pensa diferente sobre algo importante.

**Outra pessoa:** Defina o que quer, sem exigir concordância.

**Em cena:** Como a discordância afeta a relação e a decisão?

### L11 — Quem está ausente (nucleo)

> Alguém vivo está longe. Separe o que sabe do que imagina sobre sua vontade.

**Laço:** Uma pessoa viva está longe ou fora de contato.

**Outra pessoa:** Defina o que sabe de sua vontade; o resto é incerto.

**Em cena:** Como responde a distância, silêncio ou mensagem?

### L12 — Estranho que me marcou (nucleo)

> Um encontro breve deixou marca. A pessoa de hoje pode surpreender sua lembrança.

**Laço:** Um encontro breve deixou uma impressão duradoura.

**Outra pessoa:** Defina algo atual que você ainda não conhece.

**Em cena:** Como a primeira impressão ajuda ou engana?

### L13 — Inimigo que me define (expansao)

> Seu adversário toca em algo central para você. Descubra o que ele próprio busca.

**Laço:** Um adversário ameaça um objetivo, crença ou identidade importante.

**Outra parte:** Defina o que quer de você; admiração e jogo justo são opcionais.

**Em cena:** Que reação tenta provocar, impedir ou explorar?

### L14 — Autoridade e dependência (expansao)

> Há poder desigual entre vocês. Qual recusa é realmente possível?

**Laço:** Uma pessoa pode autorizar, limitar ou punir a outra.

**Outra parte:** Defina quem detém poder e do que depende cada parte.

**Em cena:** Mostre ordem, condição e possibilidade real de recusa.

### L15 — Aliança por interesse (expansao)

> A aliança funciona enquanto interesses distintos se encontram. O que cada parte oferece?

**Laço:** Vocês cooperam por objetivos distintos, sem confiança obrigatória.

**Outra parte:** Defina o que busca e o que oferece ou esconde.

**Em cena:** O que mantém a aliança e o que a faria terminar?

### L16 — Alguém que morreu (expansao)

> Alguém morreu e continua presente na memória ou no legado, não em uma vontade inventada.

**Laço:** Uma pessoa morta continua significativa por memória ou legado.

**Outra parte:** Use apenas o que foi vivido, registrado ou imaginado como tal.

**Em cena:** Que lembrança afeta a escolha? Não invente vontade atual do morto.

### L17 — Afeto que busco (expansao)

> Você deseja proximidade com alguém que pode querer outra coisa.

**Laço:** Você deseja proximidade com alguém que tem vontade própria.

**Outra parte:** Defina o que essa pessoa quer e o que você ainda não sabe.

**Em cena:** Mostre aproximação, distância ou desencontro sem garantir reciprocidade.

### L18 — Objeto que me prende (expansao)

> Um objeto ou lugar concentra seu apego. O que muda quando precisa soltá-lo?

**Laço:** Um objeto ou lugar concentra apego, identidade ou fixação.

**Outra parte:** Ele não tem vontade própria, salvo se isso existir no cenário.

**Em cena:** Que gesto revela o apego e o que custa deixá-lo?

### L19 — Vínculo por obrigação (expansao_5)

> Um papel lhe atribuiu responsabilidade por alguém. Dever, afeto e consentimento não se confundem.

**Laço:** Um papel familiar, profissional, herdado ou programado atribui a você cuidado ou dever em relação a alguém.

**Outra parte:** Defina sua vontade e a margem que tem diante desse papel; receber cuidado não implica consentir com interferência.

**Em cena:** O que é obrigação, afeto, autoridade ou escolha? O papel pode persistir mesmo sem proximidade ou acordo voluntário.

### L20 — Afeto misturado a domínio (expansao_5)

> Há afeto e há controle nessa relação. Observe os dois sem chamar domínio de cuidado.

**Laço:** Proximidade, apego ou desejo de vínculo se mistura a posse, dependência ou controle.

**Outra parte:** Pode desejar distância, recusar a relação ou querer algo que contrarie seu plano.

**Em cena:** Registre o que há de afeto demonstrado e de controle exercido. Se só existe domínio, use autoridade ou inimigo; não invente amor.

## Pressão — o que muda a situação

### P01 — Crédito em disputa (nucleo)

> Uma disputa por crédito altera quem é visto, ouvido ou recompensado.

**Acontece:** Disputa por crédito, atenção ou posição altera uma relação.

**Pesa:** Reconhecimento afeta acesso, identidade ou recompensa.

**Abra:** Mostre as reivindicações e deixe a reação em aberto.

### P02 — Oferta com condições (nucleo)

> A oferta é tentadora; suas condições merecem ser vistas antes da resposta.

**Acontece:** Uma oferta desejável vem com condições, claras ou ocultas.

**Pesa:** Aceitar compromete liberdade, recurso ou outro objetivo.

**Abra:** Defina condição conhecida e assimetria; não imponha acordo.

### P03 — Regra e caso concreto (nucleo)

> Uma regra encontra um caso que não cabe nela sem ferir alguém.

**Acontece:** Uma regra falha diante de um caso concreto.

**Pesa:** Manter ou romper afeta quem depende dela.

**Abra:** Mostre os efeitos plausíveis de cada resposta.

### P04 — Um vínculo escolhe diferente (nucleo)

> Uma pessoa próxima escolhe diferente. A relação precisa lidar com essa escolha.

**Acontece:** Uma pessoa próxima escolhe outro caminho.

**Pesa:** O plano ou vínculo já não continua igual.

**Abra:** Mostre sua decisão; o personagem escolhe como reage.

### P05 — Evidência inesperada (nucleo)

> Uma prova confiável mudou o terreno. O que ainda permanece desconhecido?

**Acontece:** Uma evidência confiável contradiz uma premissa.

**Pesa:** Rever custa algo; insistir assume um risco novo.

**Abra:** Separe o fato confirmado do que continua incerto.

### P06 — Capacidades complementares (nucleo)

> Alguém tem o recurso que lhe falta. Cooperar envolve duas vontades.

**Acontece:** Outra pessoa tem habilidade, recurso ou acesso que falta.

**Pesa:** Cooperar exige ceder algo ou lidar com dependência.

**Abra:** Defina contribuições e limites sem garantir boa vontade.

### P07 — Custo transferido (nucleo)

> A solução transfere a perda para outra pessoa. Mostre quem pagaria.

**Acontece:** Uma solução impõe perda a outra pessoa.

**Pesa:** O efeito é conhecido antes da decisão.

**Abra:** Mostre quem paga e como pode reagir; não apague a perda.

### P08 — Vitória já alcançada (nucleo)

> A vitória já aconteceu. O tempo que sobra também pode ser bom.

**Acontece:** O objetivo foi alcançado e há tempo disponível.

**Pesa:** Descansar, celebrar ou crescer usam esse tempo.

**Abra:** Apresente possibilidades boas sem punir a conquista.

### P09 — Oportunidade com prazo (nucleo)

> A ocasião termina antes de todas as respostas chegarem. Qual risco é conhecido?

**Acontece:** Uma possibilidade termina antes de saber tudo.

**Pesa:** Esperar perde a ocasião; agir aceita risco definido.

**Abra:** Diga o prazo e a incerteza; não escolha pelo personagem.

### P10 — Mais do que esperava (nucleo)

> Veio mais do que o esperado. Pessoas diferentes podem ter direito ao excedente.

**Acontece:** Chega mais recurso ou sucesso do que o previsto.

**Pesa:** Há contribuições, direitos e prioridades sobre o excedente.

**Abra:** Mostre essas posições e deixe a distribuição em aberto.

### P11 — Convite para algo bom (nucleo)

> Há um convite para algo bom. Aceitar ou recusar não precisa virar crise.

**Acontece:** Uma experiência boa pede tempo e presença.

**Pesa:** Ela cruza rotina, compromisso ou receio de participar.

**Abra:** Mostre o convite; aceitar não precisa gerar crise.

### P12 — Duas promessas, um recurso (nucleo)

> Duas promessas precisam do mesmo recurso. Cada pessoa afetada merece ser vista.

**Acontece:** Duas promessas precisam do mesmo recurso.

**Pesa:** Não se pode entregar ambas como combinado.

**Abra:** Mostre pessoas afetadas e deixe prioridade ou ruptura abertas.

### P13 — Perigo presente (expansao)

> O perigo está aqui e impede a rotina. Mostre saídas plausíveis.

**Acontece:** Uma ameaça concreta impede seguir como antes.

**Pesa:** Integridade, vida ou segurança estão em risco agora.

**Abra:** Defina ameaça e saídas plausíveis; sobrevivência não é um prêmio.

### P14 — Tentação acessível (expansao)

> O que se deseja está ao alcance por um caminho que cobra um custo.

**Acontece:** Algo desejado fica ao alcance por um caminho problemático.

**Pesa:** Obter o alvo cobra um limite, compromisso ou risco.

**Abra:** Mostre acesso e custo sem decidir se resistirá.

### P15 — Sinal ambíguo (expansao)

> Um sinal inquieta, mas ainda não é prova. Separe fato e interpretação.

**Acontece:** Um sinal contradiz a explicação atual, mas não está confirmado.

**Pesa:** Agir ou esperar depende de informação incerta.

**Abra:** Separe percepção, relato e fato; não declare prova sem suporte.

### P16 — Perda sem retorno (expansao)

> Algo se perdeu sem retorno igual. O que ainda pode ser escolhido?

**Acontece:** Uma pessoa, oportunidade ou condição não pode ser recuperada igual.

**Pesa:** A escolha atual convive com essa ausência.

**Abra:** Mostre o que acabou e o que ainda é possível, sem exigir superação.

### P17 — Controle exigido (expansao)

> Alguém exige obediência a partir de uma vantagem real. Mostre as margens de resposta.

**Acontece:** Alguém com vantagem tenta impor uma conduta.

**Pesa:** Recusar, obedecer ou resistir tem consequências distintas.

**Abra:** Defina poder e margens reais; não presuma consentimento.

### P18 — O custo em mim (expansao)

> Seguir adiante já cobra corpo, tempo ou paz. Dê forma visível ao custo.

**Acontece:** Prosseguir consome meu corpo, tempo, identidade ou paz.

**Pesa:** A perda pessoal já interfere na próxima ação.

**Abra:** Mostre o custo observável; insistir não garante grandeza.

## Conflito interno — dois valores genuínos

### N01 — Raízes / horizontes (nucleo)

> Você valoriza o lugar de onde veio e a possibilidade de ir além. Ambos pedem algo agora.

**Importam:** Pertencer aqui e conhecer outros caminhos.

**Revele:** Partir coincide com uma ocasião importante em casa.

**Abra:** O que levar, preservar à distância ou adiar?

### N02 — Eficiência / dignidade (nucleo)

> Você quer poupar recursos sem calar os afetados. O atalho tem um preço humano.

**Importam:** Poupar recursos e dar voz aos afetados.

**Revele:** O atalho exclui alguém da decisão.

**Abra:** Como ouvir essa pessoa sem perder todo o prazo?

### N03 — Verdade / pertencimento (nucleo)

> Você quer dizer o que descobriu e continuar pertencendo. Como abrir a conversa?

**Importam:** Dizer uma verdade e continuar no grupo.

**Revele:** Uma descoberta contradiz a narrativa comum.

**Abra:** Como apresentar evidências e preservar diálogo?

### N04 — Afeto / imparcialidade (nucleo)

> Você ama alguém envolvido na decisão e quer ser justo com os demais.

**Importam:** Cuidar de alguém querido e usar critério justo.

**Revele:** Uma decisão pública envolve essa pessoa.

**Abra:** Quem pode decidir sem favorecer ou abandonar?

### N05 — Beleza / utilidade (nucleo)

> Você deseja criar beleza e atender uma necessidade. Talvez o mesmo material não baste.

**Importam:** Criar beleza e atender uma necessidade prática.

**Revele:** O mesmo material serve à obra e ao reparo.

**Abra:** O que adaptar, reutilizar ou fazer em etapas?

### N06 — Continuidade / renovação (nucleo)

> Você quer guardar o que ainda serve e permitir que algo novo exista.

**Importam:** Preservar uma prática e permitir inovação.

**Revele:** Uma novidade muda algo que ainda serve a alguém.

**Abra:** Que parte manter e que parte experimentar?

### N07 — Liberdade / compromisso (nucleo)

> Você deseja escolher de novo sem tratar a promessa anterior como nada.

**Importam:** Escolher livremente e honrar um acordo.

**Revele:** Uma vontade nova esbarra no que prometeu.

**Abra:** Que condição pode renegociar com os envolvidos?

### N08 — Ambição / suficiência (nucleo)

> Você quer crescer e sabe apreciar o bastante. Qual conquista mudaria o equilíbrio?

**Importam:** Crescer e apreciar o que já basta.

**Revele:** A próxima conquista consome um prazer atual.

**Abra:** O que merece expansão e o que merece pausa?

### N09 — Curiosidade / privacidade (nucleo)

> Você quer descobrir, mas reconhece o direito de alguém não abrir a porta.

**Importam:** Aprender e respeitar privacidade.

**Revele:** Uma pista depende do acesso que alguém recusa.

**Abra:** Existe outra prova ou um acesso consentido?

### N10 — Lealdade / justiça (nucleo)

> Você é leal aos seus e vê uma injustiça que os beneficia. O que fará com as duas verdades?

**Importam:** Apoiar os seus e reparar injustiça.

**Revele:** Seu grupo ganhou algo às custas de outros.

**Abra:** Como apoiar a pessoa e responsabilizar o ato?

### N11 — Prudência / oportunidade (nucleo)

> Você quer evitar uma perda e aproveitar a ocasião. Que risco pequeno pode testar?

**Importam:** Evitar perdas e aproveitar uma ocasião.

**Revele:** A informação segura chega depois do prazo.

**Abra:** Que teste pequeno ou risco compartilhado cabe?

### N12 — Franqueza / harmonia (nucleo)

> Você quer dizer o que sente sem destruir a convivência que também estima.

**Importam:** Expressar um desejo e manter convivência.

**Revele:** Uma conversa pessoal vem sendo evitada.

**Abra:** Qual momento e proposta tornam a fala possível?

### N13 — Segurança / confiança (expansao)

> Você precisa de segurança e deseja confiar. Nenhuma das duas vontades desaparece por decreto.

**Disputam:** Evitar uma perda e permitir dependência, abertura ou risco.

**Mostre:** Um passo depende de deixar de controlar tudo.

**Pergunte:** Que sinal permite confiar e qual risco continua real?

### N14 — Controle / entrega (expansao)

> Você valoriza o cuidado com os detalhes e a liberdade de deixar alguém agir.

**Disputam:** Conferir cada detalhe e permitir espontaneidade ou ação alheia.

**Mostre:** Uma tentativa exige soltar parte do comando.

**Pergunte:** O que pode deixar acontecer e o que precisa proteger?

### N15 — Imagem / identidade (expansao)

> Você sustenta uma imagem de si e encontra uma experiência que não cabe nela.

**Disputam:** Preservar o papel em que acredita e admitir o que vive ou descobre.

**Mostre:** Uma experiência contraria a versão que sustenta de si.

**Pergunte:** Que parte é crença, desejo ou fato observado?

### N16 — Apego / desprendimento (expansao)

> Você quer preservar algo precioso e continuar vivendo sem mantê-lo intacto.

**Disputam:** Conservar algo significativo e seguir sem mantê-lo igual.

**Mostre:** Segurar a lembrança, posição ou rotina cobra um custo atual.

**Pergunte:** O que preserva ao soltar, e o que realmente perde?

### N17 — Convicção / vínculo (expansao)

> Você acredita no projeto e se importa com quem ele ameaça afastar.

**Disputam:** Realizar um projeto em que acredita e preservar um vínculo.

**Mostre:** A decisão ameaça quem importa, sem torná-la automaticamente justa.

**Pergunte:** Qual perda admite e qual relação tenta preservar?

### N18 — Impulso / limite (expansao)

> Uma vontade retorna; um limite seu também permanece. O que acontece quando se encontram?

**Disputam:** Atender uma vontade recorrente e manter uma escolha ou limite próprio.

**Mostre:** A vontade retorna apesar de uma decisão anterior.

**Pergunte:** O que dispara a vontade e que limite ainda reconhece?

### N19 — Esperança / desistência (expansao_5)

> Você vê uma razão para tentar de novo e outra para poupar as forças que restam.

**Disputam:** Continuar investindo numa possibilidade e parar de gastar forças numa tentativa que parece fracassar.

**Mostre:** A mesma pessoa encontra motivos reais para tentar mais uma vez e para abandonar essa tentativa.

**Pergunte:** Que sinal sustenta cada lado? A derrota externa sozinha não prova conflito interno; desistir de uma tentativa não é automaticamente desistir da vida.

### N20 — Dever recebido / autoria da vida (expansao_5)

> O dever recebido tem valor para você, mas existe uma vida que também quer escolher.

**Disputam:** Atender uma obrigação ligada a um papel recebido e decidir por si como viver.

**Mostre:** A obrigação importa à pessoa, mas custa um caminho que ela também valoriza.

**Pergunte:** Quanto desse dever foi imposto, herdado ou escolhido? Se só há coerção sem adesão, registre pressão em vez de inventar valor concorrente.

### N21 — Verdade / consolo (expansao_5)

> Você quer conhecer a verdade e preservar um consolo que considera valioso.

**Disputam:** Reconhecer um fato difícil e preservar uma crença ou narrativa que dá amparo a si ou a alguém importante.

**Mostre:** Há razões valorizadas para esclarecer e para proteger o consolo, ainda que escolha ocultar ou selecionar a informação.

**Pergunte:** Quem sabe o quê? Que importância dá à verdade? Mentir sem valorizar a verdade não basta para preencher os dois lados.

### N22 — Dedicação / presença cotidiana (expansao_5)

> A obra importa, e a vida fora dela também. O que perderia se só uma coubesse?

**Disputam:** Entregar-se a uma obra ou vocação e estar disponível para experiências e relações fora dela.

**Mostre:** A pessoa preza a prática e também algo que perde enquanto só pratica.

**Pergunte:** Que ocasião concreta quer viver além do trabalho? Se os outros cobram descanso mas a pessoa não o valoriza, há custo externo, não tensão comprovada.

## Guias de uso

### U01 — NPC rápido (guia)

> Comece pela combinação completa: origem, convicção, desejo, método, expressão, vínculo, pressão e dois valores em conflito; depois responda ao chamado.

**Tire:** Uma carta OR, CV, D, F, V, L, P e N; consulte G07 para Chamado e destino.

**Complete:** Interprete as oito cartas com nome, papel e situação. Separe a origem proposta dos fatos já estabelecidos.

**Entre:** Mostre uma tentativa e a expressão; registre chamado, resposta, fato, crença e escolha. A reação dos outros continua aberta.

### U02 — Personagem completo (guia)

> Todas as oito camadas e Chamado e destino fazem parte da criação 5.2. Conecte-as por escolhas e situações concretas.

**Acrescente:** Preencha OR + CV + D + F + V + L + P + N e os cinco campos de G07; nenhuma dessas camadas é dispensada na criação 5.2.

**Conecte:** Origem não implica culpa. Convicção distingue fato, valor e regra; N precisa de dois valores genuínos que a pessoa deseja preservar.

**Prepare:** Se o sorteio contradiz o recorte, escolha outra carta ou revise a proposta. Uma combinação aleatória não garante coerência nem exige redenção.

### U03 — Conversa viva (guia)

> Numa conversa, cada resposta pode pedir outra tática do personagem.

**Intenção:** Escolha o que quer desta pessoa agora.

**Tática:** Convencer, acolher, testar, negociar ou ganhar tempo.

**Reaja:** Use V; mude a tática quando a resposta mudar.

### U04 — Subtexto (guia)

> O que se quer e o que se mostra podem diferir sem exigir segredo.

**Escolha:** O que busca e o que comunica; nem todo subtexto exige segredo.

**Mostre:** Gesto e fala oferecem pistas; silêncio também comunica.

**Respeite:** Regras resolvem percepção; jogadores decidem interpretação e ação.

### U05 — Dupla em movimento (guia)

> Duas pessoas ganham vida quando cada uma pode querer algo próprio.

**Crie:** D + F + V para cada pessoa; conecte uma carta L.

**Defina:** Cada uma quer algo; reciprocidade e equilíbrio são opcionais.

**Encontre:** Um ponto de contato e um atrito; cooperação não é obrigatória.

### U06 — Escolha aberta (guia)

> Prepare circunstância e consequências; deixe a decisão para a mesa.

**Combine:** P muda a circunstância; N apresenta dois valores genuínos que a pessoa quer preservar e que a escolha coloca em disputa.

**Concretize:** Defina quem é afetado e quais poder, recurso ou risco pesam.

**Abra:** Prepare consequências plausíveis; aceite soluções da mesa.

### U07 — Depois da escolha (guia)

> Depois da cena, registre a mudança observada antes de escolher outra carta.

**Registre:** Escolheu [ação]. Agora [consequência observada].

**Atualize:** Anote uma mudança em objetivo, método ou vínculo, se houver.

**Retome:** Na próxima cena, mostre essa consequência antes de sortear mais.

### U08 — Elenco variado (guia)

> Varie as oito famílias entre personagens e identifique dois valores genuínos em cada N; não uniformize passado, culpa ou destino.

**Distribua:** Núcleo 01–12; expansão 13–18; expansão 5.0 D19–24/F19–20/N19–22/L19–20/V19–22. P termina em P18. Expansão 5.2: OR01–12 e CV01–12.

**Contraste:** Cada criação usa OR/CV/D/F/V/L/P/N e G07. Varie escolhas e respostas; sorteie sem reposição para reduzir repetições no elenco.

**Confira:** N pede dois valores reais em disputa, não só adversidade. A obrigação da camada não autoriza inventar trauma, culpa ou redenção.

### U09 — Ajuste e continuidade (guia)

> Quando a carta contrariar a história jogada, preserve a história.

**Preserve:** Fatos jogados e escolhas pertencem à mesa.

**Adapte:** Se a carta contradiz a pessoa, troque ou deixe a camada aberta.

**Separe:** U é consulta; registre código e versão ao retomar alguém.

## Guias de contexto

### G01 — Memória e registros (guia_contexto)

> Memória, experiência e registro são fontes distintas de continuidade.

**Separe:** O que aconteceu, o que a pessoa retém e o que consta em cada registro.

**Em cena:** Defina alcance da retenção, quem altera notas e o que permite recuperar contexto; não improvise uma perda de memória só para forçar surpresa.

**Use:** F19 descreve o método; V20 o meio. O guia descreve continuidade, não diagnóstico nem conflito entre valores.

### G02 — Percepção e verificação (guia_contexto)

> Percepção, relato e fato devem continuar separados até a verificação.

**Separe:** Fato do cenário, percepção, relato e inferência; marque o que ainda é desconhecido.

**Em cena:** Escolha como um sinal pode ser verificado pelas regras e que explicações permanecem abertas.

**Use:** P15 cria incerteza, mas não explica sua causa. Registre projeção, aparência ou crença apenas quando o recorte ou cenário as sustentar.

### G03 — Influência externa (guia_contexto)

> Uma influência externa tem limites próprios; registre o que ainda é escolha.

**Separe:** Intenção própria, influência de objeto ou entidade e ação que as regras realmente impõem.

**Em cena:** Defina gatilho, alcance, margem de resistência e o que permanece escolha. Não atribua vontade a um objeto sem base no cenário.

**Use:** O Anel, uma maldição ou um hotel podem exigir esse contexto; ele não transforma influência em tensão interna nem autoriza controlar jogadores.

### G04 — Mandato e aprendizagem (guia_contexto)

> Um mandato diz o que se exige, não tudo o que a pessoa pode aprender.

**Separe:** Objetivo atribuído, instrução executada, interpretação e iniciativa própria demonstrada.

**Em cena:** Defina o que pode aprender, quem pode mudar a ordem e como resolve instruções incompatíveis.

**Use:** D21/L19 cabem em dever e programação; não presuma afeto, consentimento ou livre-arbítrio pela aparência de cuidado.

### G05 — Identidade e mudança de registro (guia_contexto)

> Uma mudança de fala não explica, por si, identidade ou diagnóstico.

**Separe:** Papel encenado, identidade sustentada, posição percebida e continuidade estabelecida na ficção.

**Em cena:** Registre o que muda, quem percebe e o que cada posição sabe. V17 só descreve expressão; não explica causas ou retenção de experiência.

**Use:** Não deduza diagnóstico de alternância de fala nem associe condição real a violência. Preserve o mecanismo específico da obra ou do cenário.

### G06 — Orientação sem conflito ativo (guia_contexto)

> Nem toda dificuldade é conflito interno. Na criação 5.2, encontre dois valores genuínos e uma escolha que os coloque em disputa.

**Separe:** Objetivo, obstáculo e custo não são automaticamente valores concorrentes. Nomeie o que a pessoa quer preservar em cada lado de N.

**Em cena:** Apresente uma escolha em que os dois valores importem à pessoa; mostre uma tentativa e deixe a consequência em aberto.

**Use:** G06 ajuda a interpretar ou trocar N, não a omiti-lo na criação 5.2. Se o recorte não sustenta dois valores, reveja a carta ou proponha outra situação; não force culpa ou redenção.

### G07 — Chamado e destino (guia_contexto)

> Algo põe uma possibilidade diante de você. Separe o que aconteceu, o sentido que atribui e a resposta que escolhe.

**Chamado:**

1. Pedido de alguém
2. Papel ou herança
3. Risco concreto
4. Encontro ou convite
5. Presságio ou profecia
6. Natureza, tempo ou finitude

**Resposta:**

1. Aceito
2. Recuso
3. Adio e investigo
4. Negocio as condições
5. Tento impedir o futuro
6. Busco cumprir por outro caminho

**Fato:** O que está confirmado no mundo?

**Crença:** Quem interpreta ou prevê algo, e com qual evidência?

**Escolha:** O que você decide e o que ainda pode escolher? Não sorteie um desfecho.


---

# Exemplos completos — Persona Cards 5.2

Oito famílias obrigatórias e os cinco registros de G07 em cada exemplo. Propostas de interpretação não mudam o cânone; jogadores decidem suas respostas.

## Cinco personagens criados com as cartas

Os códigos são reais; **todas as origens, convicções, tensões e cenas acrescentadas abaixo são propostas autorais**, não acontecimentos ou conclusões canônicas sobre as obras. Luffy, Zuko e Batman servem a leituras específicas. Lina e Seris são originais da mesma campanha. Os exemplos não são teste de mesa.

### 1. Luffy — One Piece

**OR04 · CV05 · D03 · F17 · V09 · L08 · P04 · N07 · guia G07**

Na cena proposta, um companheiro permaneceu ao seu lado numa derrota (**OR04**). Luffy interpreta o apoio como espaço para escolher, não como direito de mandar na vida alheia (**CV05**). Quer decidir a próxima ilha (**D03**), toma a frente da partida (**F17**) e convida com entusiasmo (**V09**). Nami tem uma rota segura e prioridades próprias (**L08**). Um tripulante escolhe ficar no porto (**P04**). Para este exemplo, estabelecemos dois valores genuínos: **liberdade de partir e compromisso aceito de acompanhá-lo até uma entrega** (**N07**). Isso é uma tensão proposta, não deduzida de cansaço ou risco.

**G07:** chamado — o companheiro pede ajuda; resposta — renegociar as condições; fato — a entrega ainda não aconteceu; crença — ser livre também permite assumir compromissos; escolha — combinar uma parada sem decidir por Nami. Se ela recusar, ele precisa ouvir, negociar ou procurar outra rota. Competência: liderar em ação; prazer: procurar uma refeição na próxima ilha.

### 2. Zuko — Avatar: A Lenda de Aang

**OR03 · CV07 · D15 · F15 · V04 · L07 · P05 · N03 · guia G07**

Propomos o papel recebido de herdeiro como antecedente (**OR03**) e o valor de conhecer a verdade como convicção (**CV07**). Zuko tenta reconhecer quem escolhe ser (**D15**), insiste além do desgaste (**F15**) e apresenta a conclusão antes da explicação (**V04**). Iroh oferece conselho, com vontade e critérios próprios (**L07**). Um documento confiável contradiz uma ordem (**P05**). A disputa é entre **dizer a verdade e preservar pertencimento familiar/nacional** (**N03**), ambos ainda importantes neste recorte proposto.

**G07:** chamado — obrigação de um papel recebido; resposta — renegociar; fato — o documento contradiz a justificativa da ordem; crença — discordar não apaga tudo que valoriza em sua origem; escolha — recusar aquela parte e apresentar a prova. A resposta do pai, de Iroh ou do grupo permanece aberta. Competência: treino disciplinado; prazer proposto: preparar uma bebida durante uma pausa.

### 3. Batman — DC Comics

**OR01 · CV06 · D04 · F01 · V04 · L07 · P03 · N14 · guia G07**

Nesta proposta, uma ausência continua presente em sua rotina (**OR01**) e preservar uma vida importa além de sua utilidade (**CV06**). Batman quer retirar moradores de um ataque (**D04**), prepara acessos e recursos (**F01**) e dá a instrução em poucas palavras (**V04**). Alfred orienta sem decidir tudo por ele (**L07**). Um protocolo fechou o abrigo previsto (**P03**). A tensão estabelecida é **conferir cada detalhe e permitir iniciativa real dos aliados** (**N14**); identidade dupla ou juramento, sozinhos, não provariam esse conflito.

**G07:** chamado — ameaça que exige decisão; resposta — redirecionar o caminho; fato — o abrigo está fechado; crença — proteção não depende só de supervisão individual; escolha — confiar a Alfred outra saída enquanto investiga o ataque. Moradores podem contestar a rota. Competência: investigação; prazer proposto: restaurar um pequeno mecanismo fora da operação.

### Uma campanha: as comportas de Porto da Névoa

A vazante revela um canal antigo. Bairros precisam da travessia; o conselho quer fechá-la após acidentes. Um mapa indica uma rota possível, mas **não comprova sua segurança atual**.

### 4. Aliada: Lina Moura, barqueira e cartógrafa

**OR12 · CV03 · D12 · F07 · V11 · L03 · P12 · N02 · guia G07**

Descobrir o prazer de mapear correntezas deu lugar à sua vocação (**OR12**); ela aprendeu que cuidado precisa de presença e gesto (**CV03**). Quer reabrir uma travessia (**D12**), traduz pedidos de moradores e conselho (**F07**) e explica o teste passo a passo (**V11**). A sócia Dara quer reservar o barco para evacuação (**L03**). Inspeção e remédios prometidos precisam da mesma embarcação ao amanhecer (**P12**). Lina valoriza **usar bem o recurso escasso e dar voz a quem assumirá o risco** (**N02**), não apenas terminar rápido.

**G07:** chamado — convite de moradores; resposta — renegociar; fato — há um único barco disponível; crença — a rota merece teste, não certeza antecipada; escolha — ouvir os afetados e pedir ajuda na medição. Dara e jogadores podem recusar. Competência: ler correntezas; prazer: consertar miniaturas de barco.

### 5. Vilã: Seris Vale, conselheira das travessias

**OR09 · CV01 · D10 · F14 · V16 · L15 · P05 · N14 · guia G07**

Uma rotina organizada lhe ofereceu segurança (**OR09**); ela passou a crer que, sem controle, tudo se perde (**CV01**). Quer autoridade exclusiva sobre rotas e taxas (**D10**), oculta um mapa enquanto encena preocupação (**F14**) e cobra com cortesia calculada (**V16**). A guilda coopera enquanto lucra (**L15**). Surge um registro confiável da passagem antiga (**P05**). Para a nova cena, propomos que ela valorize **conferir cada detalhe e permitir iniciativa de administradores cuja capacidade considera necessária** (**N14**). A tensão envolve seu projeto de poder; não exige afeto escondido, remorso ou cura.

**G07:** chamado — sinal interpretado como destino; resposta — redirecionar; fato — o canal existiu; crença — só seu comando evitará outra crise; escolha — tentar controlar a inspeção e testar se tolera a iniciativa da guilda. A prova não determina sua resposta nem comprova a segurança do canal. Competência: organizar estoques; prazer: restaurar encadernações. O grupo pode enfrentar o monopólio por prova, negociação, fiscalização ou combate.
