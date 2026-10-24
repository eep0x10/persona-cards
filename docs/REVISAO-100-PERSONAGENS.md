# Revisão do baralho com 100 inspirações

## Escopo e natureza da evidência

Esta é uma revisão editorial independente da implementação, feita por leitura do baralho e de um conjunto de interpretações autorais. Não é teste empírico de mesa, avaliação psicológica, pesquisa com participantes ou demonstração de fidelidade universal a personagens conhecidos. Uma cena proposta pelo conjunto é uma hipótese de uso, não um acontecimento canônico. As fontes oficiais dos personagens dão contexto; não endossam a escolha das cartas.

Fontes locais: [baralho 5.1](../deck/persona-cards-5.1.json), [manual](../deck/manual-5.1.md), [revisão editorial anterior](../deck/revisao-editorial-5.1.md), [skill](../skills/persona-cards/SKILL.md) e [limites da revisão histórica](../skills/persona-cards/references/revisao.md). As classificações antigas de 78/84 personagens bons pertencem a outro exercício e não serão reutilizadas como resultado desta amostra.

Nenhum código, leitura, campo oficial, PDF ou conteúdo congelado de 5.0 é alterado por este relatório. As propostas abaixo dependem de decisão editorial e validação futura.

## Critérios de revisão

| Critério | Evidência exigida | O que não conta como prova |
| --- | --- | --- |
| Desejo D | Resultado que a pessoa tenta obter ou manter no recorte | Atribuir bondade, método, diagnóstico ou redenção a partir do título |
| Forma F | Uma tentativa observável e seu custo possível | Uma profissão, poder ou adjetivo sem ação |
| Expressão V | Forma concreta de falar, gesticular, escrever ou sinalizar | Repetir um bordão da obra ou deduzir personalidade de deficiência |
| Vínculo L | Outra vontade e uma possibilidade real de discordância; distinguir pessoa, objeto e memória | Prometer reciprocidade ou inventar vontade atual de pessoa morta |
| Pressão P | Circunstância ou custo observável que muda a próxima escolha | Transformar toda dificuldade em valor interno |
| Conflito N | Dois valores que a pessoa quer preservar e que competem naquele recorte | Adversidade, punição, coerção, receio de perder ou cobrança alheia isolados |
| Agência | Tentativa, resposta aberta e consequências possíveis | Determinar a ação de jogadores ou garantir acordo/perdão |
| Encaixe | Código e título reais; justificativa que respeita os campos da carta | Renomear um conceito ou mudar o passado para declarar cobertura |
| Proposta de expansão | Caso identificado, alternativa mais próxima insuficiente, texto jogável e distinção conceitual | Adicionar carta só porque foi pouco usada ou porque a obra tem um nome específico |

As contagens registram a utilização nesta seleção intencional. Não medem popularidade, eficácia, balanceamento de sorteio ou compreensão de leitores. D/F/V são obrigatórias no método rápido; L/P/N são opcionais, e U/G são consulta. Não usar N pode ser a aplicação correta.

## Inventário do baralho de referência

Leitura estrutural de `deck/persona-cards-5.1.json`: 141 cartas, das quais 126 de criação e 15 guias. Famílias: D 24; F 20; V 22; L 20; P 18; N 22; U 9; G 6. Módulos: núcleo 72; expansão 36; expansão 5.0 18; guias de uso 9; guias de contexto 6.

SHA-256 do arquivo consultado: `6c33a7adb5187c8e909ab5a3bc6c4b283a79c670d03b67ea3c1c32333229f86d`.

## Achado editorial confirmado antes da amostra

### U08 omite a expansão 5.0 no mapa do elenco

**Local:** carta U08, campo `Distribua`, em `deck/persona-cards-5.1.json` e na seção U08 do manual. Texto atual: “Núcleo: 01–12. Expansão: 13–18. Misture por família se quiser.”

**Evidência e impacto:** o arquivo contém 18 cartas com módulo `expansao_5`, mas o guia não apresenta esse terceiro grupo. Quem seguir apenas a distribuição de U08 pode ignorar desejos, métodos e expressões que foram acrescentados justamente para ampliar o repertório. Isto é uma omissão editorial verificável; não prova falha de uso em mesa nem exige uma carta nova.

**Correção candidata, sem alterar o deck nesta tarefa:**

- **Distribua:** “Núcleo: 01–12. Expansão: 13–18. Expansão 5.0: D19–D24, F19–F20, N19–N22, L19–L20 e V19–V22; P termina em P18. Misture por família se quiser.”
- **Contraste:** “Varie desejo, método e expressão; sorteie sem reposição quando quiser reduzir repetições no elenco.”
- **Confira:** “Ausência de conflito não é falha. Não force trauma ou redenção.”

A versão completa esclarece os intervalos diferentes por família. Antes de uma promoção editorial, conferir espaço e leitura no impresso; uma alternativa compacta é apresentar somente os três nomes de módulos e remeter os intervalos ao índice.

## Fronteiras a confrontar com os casos

### D10: influência inclui autoridade coercitiva

O objetivo de D10, “Obter [autoridade] para decidir [assunto]”, comporta autoridade disputada, ilegítima ou absoluta. Já a abertura “Você quer participar das decisões” e o campo “Peça um voto ou aliança; declare um limite” orientam a leitura para participação cooperativa e limite reconhecido. Isso pode exigir adaptação em um tirano; não demonstra ausência de um desejo no baralho.

**Candidato editorial preservando código, título e objetivo:**

- **Leitura:** “Você quer ter poder sobre uma decisão. Que autoridade procura, e quem poderá contestá-la?”
- **Quero:** “Obter [autoridade] para decidir [assunto].”
- **Mostre:** “Busca apoio, acesso ou posição que lhe permita decidir; descreva como usa esse poder.”
- **Interação:** “Declare a autoridade pretendida e a margem real de recusa dos demais. Só atribua um limite se a pessoa o reconhecer.”

O texto não exige consentimento, bondade nem redenção, e também não transforma todo pedido de voz em dominação. F13/F14 descrevem coerção ou encenação; D10 continua descrevendo o resultado desejado.

### D06: resolver uma pergunta não garante abertura à refutação

O objetivo “Descobrir por que [fenômeno] acontece” pertence a D. O campo “Testa uma hipótese e aceita evidência contrária” acrescenta uma atitude metodológica e uma virtude epistêmica. Uma pessoa pode querer realmente uma resposta e, ainda assim, ter dificuldade em admitir refutação. Confirmação deliberada de uma mentira pode ser D24 e não deve ser disfarçada como busca da verdade.

**Candidato editorial, condicionado à leitura dos casos:**

- **Leitura:** “Uma pergunta não o deixa em paz. Que pista procura, e como reage se ela contrariar sua hipótese?”
- **Quero:** “Descobrir por que [fenômeno] acontece.”
- **Mostre:** “Procura uma pista ou testa uma hipótese; registre o que faz diante de evidência contrária.”
- **Interação:** “Peça, negocie ou tente obter acesso à informação; diga o que considera uma resposta suficiente.”

Não é proposta de carta nova: F01/F10/F16/F19 podem diferenciar planejamento, pragmatismo, verificação de risco e registros. O caso precisa sustentar a busca de resposta; ser dogmático por si só não demonstra D06.

## Resultado da análise dos 100 casos

Conjunto consultado: [100 inspirações](../app/public/inspirations.json), versão 5.1, 100 IDs únicos, 27 franquias. SHA-256: `e86d8100963b81da76b28259e18d1408107dfccf8f1d224ba1d916482b013ae7`. As propostas, campos e justificativas dos 100 registros foram lidos; as oito justificativas N e o caso Muzan foram relidos depois das correções abaixo. O baralho de referência conservou o hash registrado acima.

**Conclusão editorial:** o conjunto produz propostas jogáveis usando o repertório existente. Há uma omissão confirmada em U08 e nove usos cuja fronteira literal precisa ficar visível: oito adaptações do convite de D10 e uma do horizonte temporal de D13. Não há base para afirmar que o baralho cobre toda personalidade, que o público reconhecerá os 100 personagens ou que novos códigos são necessários. A revisão foi feita por um agente distinto do gerador, na mesma tarefa autoral, sem leitores cegos, jogadores ou observação de sessões.

### Cobertura efetivamente observada

| Família | Cartas no deck | Ocorrências nos 100 casos | Códigos distintos usados | Códigos não usados |
| --- | ---: | ---: | ---: | --- |
| D | 24 | 100 | 24 | Nenhum |
| F | 20 | 100 | 20 | Nenhum |
| V | 22 | 100 | 20 | V14, V19 |
| L | 20 | 23 | 15 | L01, L04, L11, L12, L14 |
| P | 18 | 22 | 13 | P08, P10, P11, P15, P16 |
| N | 22 | 8 | 8 | N02, N04, N05, N06, N08, N09, N10, N11, N12, N16, N17, N18, N19, N21 |
| U | 9 | 0 | 0 | U01–U09: consulta, não camadas dos personagens |
| G | 6 | 0 | 0 | G01–G06: consulta, não camadas dos personagens |

São 353 atribuições e 100 códigos distintos das 126 cartas de criação; 26 não foram usados. Não se soma U/G a uma suposta taxa de falha: a amostra não os registra como camadas nem mede sua consulta. Os 92 casos sem N não foram classificados como incompletos por essa ausência. Os oito com N são `han-solo`, `katniss-everdeen`, `elsa`, `moana`, `zuko`, `batman`, `homem-aranha` e `cloud-strife`.

| Recorte da seleção | Contagem |
| --- | ---: |
| Anime | 20 |
| Cinema | 18 |
| Animação | 18 |
| Quadrinhos | 16 |
| Séries | 12 |
| Jogos | 16 |
| Herói | 48 |
| Ambíguo | 23 |
| Vilão | 17 |
| Coadjuvante | 12 |

Mídia e papel são rótulos editoriais da amostra, não categorias mutuamente exclusivas do mundo real nem classificação moral definitiva dos personagens. A predominância de protagonistas protetores influencia quais cartas aparecem mais.

### Concentração, repetições e cartas pouco usadas

- **D:** D04 aparece 19 vezes e D10 oito: juntas, 27 das 100 atribuições de desejo. D03 e D22 aparecem sete vezes cada. D01, D02, D05, D08, D09 e D16 aparecem uma vez cada.
- **F:** F14 aparece 14 vezes e F13 doze: 26 das 100 atribuições de método. F01 e F10 aparecem oito vezes cada. F05, F18 e F19 aparecem uma vez cada.
- **V:** V04 aparece 18 vezes e V10 treze: 31 das 100 atribuições de expressão. V05 e V18 aparecem oito vezes cada. V02, V17, V20 e V22 aparecem uma vez cada; V14/V19 não aparecem.
- **L/P/N:** L06/L08 aparecem três vezes cada; P04/P05/P17 três vezes cada; cada um dos oito códigos N usados aparece uma vez. Os denominadores são 23, 22 e oito atribuições, respectivamente, e não 100 aplicações obrigatórias dessas famílias.

Há 94 trios D/F/V distintos. Seis trios aparecem duas vezes: Elsa/Eleven (`D03/F20/V18`); Piccolo/Batman (`D04/F01/V04`); Aang/Superman (`D04/F03/V12`); Yuji/Tifa (`D04/F08/V08`); Vader/Bowser (`D10/F13/V04`); Maui/Loki (`D24/F14/V16`). Os campos situam cada uso em alvos, relações e circunstâncias diferentes. Compartilhar cartas não é defeito, mas o leitor ainda precisa conferir se as falas e reações continuam distinguíveis sem nome, arte ou franquia. Isso não foi testado com leitores.

**Cartas não amostradas não são automaticamente ruins.** A ausência de V19 não justifica atribuir língua de sinais a alguém sem base; a de N09 não justifica inventar privacidade como valor só para completar cobertura. P08/P10/P11 sugerem uma próxima bancada de vitória, excedente e convite agradável: a atual seleção privilegia perigo, oposição e proteção. Isso identifica um limite da seleção, não uma falha provada dessas cartas.

### O que as classificações de aderência realmente dizem

O arquivo final tem **84 registros rotulados `direto` e 16 `adaptado` pelo gerador**. Não são 84 acertos contra 16 erros: a classificação mistura fronteiras da carta e cautela de recorte. Esta revisão mantém essa distinção explícita:

| Motivo registrado | Quantidade | IDs |
| --- | ---: | --- |
| Convite cooperativo de D10 não descreve o uso coercitivo da autoridade | 8 | `freeza`, `darth-vader`, `palpatine`, `scar`, `doutor-destino`, `o-mestre`, `ganondorf`, `bowser` |
| D13 descreve saída imediata, mas o objetivo é eliminar vulnerabilidade duradoura | 1 | `muzan-kibutsuji` |
| Agência parcialmente atribuída pelo jogador | 3 | `link`, `red`, `chell` |
| Agência/programação de inteligência artificial | 1 | `glados` |
| Continuidade editorial específica | 1 | `thanos` |
| Motivação ligada a uma fase clandestina | 1 | `severo-snape` |
| Proteção não humana e meios coercitivos | 1 | `hera-venenosa` |

Os sete últimos registros não demonstram, por si, falta de carta. Em particular, proteger uma área vegetal cabe literalmente no “alguém ou lugar” de D04; a ressalva de Hera serve para não equiparar proteção a bondade dos meios. O caráter adaptado de Link/Red/Chell tampouco deve ser interpretado como incapacidade de representar comunicação sem fala: V13 fornece gesto, distância, objeto e ação.

## Achados sustentados pelos casos e correções da bancada

### Prioridade 1 — manter objetivo e marcar a adaptação temporal em Muzan

**Caso:** `muzan-kibutsuji`, D13/F13/V04. Seu campo D busca eliminar a vulnerabilidade ao sol para continuar existindo sem depender da noite. D13, porém, abre com “O perigo é presente” e pede sair de uma ameaça com condição mínima. Sobreviver a um episódio e modificar duradouramente a própria condição são objetivos próximos, mas não idênticos.

O primeiro arquivo rotulava o caso como direto. Depois do apontamento, o gerador manteve o objetivo e passou a registrar `adaptado`, com a tag `d13-objetivo-duradouro`. Essa é uma correção de classificação demonstrável, não um teste de eficácia do baralho. Alterar o exemplo para uma fuga noturna teria escondido a diferença que a bancada deveria revelar.

**Proposta pequena para uma edição futura, em alternativa a criar novo D:**

- **Leitura:** “Uma ameaça pesa sobre sua continuidade. Você tenta atravessar este perigo ou impedir que ele volte a alcançá-lo?”
- **Quero:** “Preservar minha vida diante de [ameaça], buscando [condição de sobrevivência].”
- **Mostre:** “Procura uma saída imediata ou uma proteção duradoura; diga qual delas orienta a próxima ação.”
- **Interação:** “Peça, exija ou procure o recurso necessário. Não presuma que desejar sobreviver determina os meios ou um limite moral.”

**Distinção e risco:** D13 continua sendo a continuidade da própria vida; D04 protege alguém ou lugar; D06 busca uma resposta; D22 busca valor para si. O caso não basta para decidir entre ampliar D13 e criar uma carta de transformação duradoura. A alteração acima precisa de contraexemplos de sobrevivência imediata, como `alan-grant` e `chell`, antes de promoção. Nesta tarefa, conserva-se a carta oficial e explicita-se a adaptação.

### Prioridade 2 — D10 já alcança tiranos; seus convites precisam de neutralidade

Os oito IDs D10 da tabela concretizam domínio: controlar recursos, a instituição, um reino, uma decisão familiar ou a possibilidade de resistência. O resultado desejado está no objetivo da carta. O problema é importar para todos o “declare um limite” como se cada antagonista reconhecesse uma fronteira moral. As notas finais evitam isso e F13/F14 distinguem coerção e encenação.

**Aceite editorial:** manter código D10 e objetivo, preservar o convite de agência dos demais e aplicar a revisão textual proposta na seção D10 somente após decisão editorial. Não criar uma carta “tirano” ou “vilão”: seria um rótulo moral no lugar de desejo e duplicaria autoridade já representada.

### Prioridade 2 — N exige dois valores no caso, não apenas um personagem conhecido

A primeira composição de `nico-robin` acrescentava N09 com curiosidade e privacidade, mas a fonte genérica e o recorte não demonstravam a atribuição desse segundo valor ao personagem. O par era logicamente válido numa cena inventada; não era evidência independente de uma característica canônica. O gerador optou por retirar N09 e manter D06/F16/V05. Assim a cobertura N diminuiu de nove para oito códigos, sem tornar o personagem incompleto.

As oito notas restantes foram reescritas para explicar os dois lados já presentes nos campos. Antes repetiam uma frase sobre não exigir “tensão interna adicional”, ambígua quando N já estava selecionado. Os pares finais são:

| ID | Carta | Dois lados explicitados no recorte autoral |
| --- | --- | --- |
| `han-solo` | N07 | Liberdade de partir e compromisso aceito de transporte |
| `katniss-everdeen` | N13 | Segurança/autoproteção e confiança valorizada na cooperação |
| `elsa` | N20 | Dever pelo reino e autoria da própria vida |
| `moana` | N01 | Pertencer à comunidade e conhecer o horizonte |
| `zuko` | N03 | Verdade aprendida e pertencimento familiar/nacional |
| `batman` | N14 | Conferir o resgate e permitir iniciativa real dos aliados |
| `homem-aranha` | N22 | Responsabilidade heroica e presença desejada nas relações cotidianas |
| `cloud-strife` | N15 | Autoimagem sustentada e reconhecimento de experiência que a contradiz |

Esses campos passam o critério lógico da cena. Não estabelecem que cada continuidade da obra atribui exatamente os mesmos valores. Batman explicita variação entre continuidades; Cloud não recebe diagnóstico a partir da dúvida sobre memória. O custo em Vegeta, a ameaça em Jesse e a punição buscada por Sasuke não foram convertidos automaticamente em N. Nenhum dos 17 registros rotulados vilão exige N ou redenção para ser finalizado.

### D06: limite editorial real, sem falha demonstrada nos cinco casos escolhidos

`nico-robin`, `hermione-granger`, `dustin-henderson`, `sherlock-holmes` e `cynthia` explicam investigação ou verificação e incorporam abertura a correção nos campos propostos. Nenhum é um antagonista dogmático escolhido para confirmar uma crença. Portanto a amostra não demonstra falha desses cinco encaixes nem sustenta outra carta de desejo. A revisão textual de D06 acima é uma proposta preventiva de separação entre desejo e método, não um achado empírico contra os casos.

### Distinção de voz: ajustar o exemplo antes de expandir V

Na versão parcial, `usopp` usava V21 com uma imagem lírica do horizonte. O trecho satisfazia a carta, mas não explicava por que essa voz seria distintiva do personagem escolhido. O gerador trocou para V10 e descreveu o exagero humorístico que disfarça medo; não foi necessário criar carta de expressão. `monkey-d-luffy` também deixou de receber o hábito genérico de compartilhar comida, passando a procurar uma refeição. São melhorias autorais de reconhecimento, sem alegar que uma proposta anterior constituía um acontecimento canônico falso.

V04 frequente não impede variação, mas recomenda um próximo exercício de fala sem nome. Se Piccolo/Batman ou Vader/Bowser se tornarem indistinguíveis nesse exercício, comparar primeiro finalidade da frase, ritmo, gesto e reação à recusa. Não acrescentar V para reproduzir bordões de franquias.

## Expansão: decisão provisória e contraexemplos necessários

**Nenhuma carta NEW é recomendada para incorporação nesta revisão.** As oportunidades sustentadas são correções de texto ou classificação: U08, D10 e o horizonte de D13. Não há evidência suficiente para converter estas duas hipóteses em cartas novas:

- **Acumular sem suficiência:** D08 exige quantidade/projeto, mas `han-solo` tem dívida finita e se encaixa. Não há um acumulador sem projeto nesta seleção. Usar a ausência desse perfil para declarar o desejo coberto seria tão indevido quanto declarar D08 defeituoso. Antes de propor outra D, montar casos específicos e explicar por que D08/D10/D24 não representam seu resultado pretendido.
- **Delegar autonomia:** `gandalf` traduz posições (F07); `alfred-pennyworth` oferece cuidado antes de pedir mudança (F08). As cenas não estabelecem alguém transferindo autoridade de decisão e aceitando ser contrariado pelo delegado. F17 já distribui tarefas e inicia ação, sem exigir microgestão. Uma nova F só se justifica depois de um caso que distinga delegação de ajuda, mediação, apoio e liderança, sem atribuir retrospectivamente outra ação a estes registros.

Uma bancada seguinte pode testar um único contraste por vez: sobrevivência imediata versus continuidade duradoura; consulta informacional versus imposição de narrativa; liderança inicial versus delegação de decisão. Para uma proposta NEW futura, registrar obrigatoriamente ID/recorte, campo insuficiente da alternativa mais próxima, leitura, ação jogável, custo e diferença em relação ao existente. A proposta permanece fora do baralho até haver revisão editorial, contraexemplo e verificação dos artefatos derivados.

## Limites de cânone e de validação

As URLs em `sources` são referências oficiais de franquias, catálogos, plataformas ou divulgação. Um catálogo não comprova cada valor interno, frase original ou fase escolhida. Esta revisão não atribui às fontes as interpretações de D/F/V/L/P/N e não certifica linha por linha a biografia dos 100 personagens. Link/Red/Chell têm agência parcialmente construída pelo jogador; Thanos está explicitamente no recorte dos quadrinhos ligado à Morte; Snape depende de uma fase; GLaDOS separa atribuição de vocação de programação/autonomia.

O conjunto diferencia coerção de consentimento e, em casos como `darth-vader`, `coringa`, `walter-white` e `loki`, mantém controle, manipulação ou imagem sem cura obrigatória. Isso é observação dos textos produzidos, não uma afirmação sobre como participantes reagirão a eles. N/L/P opcionais não precisam aparecer em todos; não é possível estimar os efeitos do sorteio com uma seleção intencional de cartas.

**Verificações efetivamente feitas nesta revisão:** leitura de `AGENTS.md`, README, skill, manual, campos das 141 cartas, revisão editorial e registros dos 100 casos; agregações por PowerShell com `ConvertFrom-Json`, `Group-Object` e `Sort-Object`; hashes com `Get-FileHash`; comparação das correções solicitadas ao gerador. Não foram executados testes Node, API, build, navegador, renderização ou sessão de mesa por este revisor. As suítes e o QA relatados pelos outros agentes não são contabilizados como execução própria nem como prova de eficácia narrativa.

**Critérios de aceite deste relatório:** todos os 100 IDs constam no apêndice; métricas têm denominador e fonte; nenhuma ausência é automaticamente defeito; propostas não mudam o baralho; adaptações conservam os objetivos incômodos em vez de fabricar encaixe; alegações canônicas não verificadas ficam como limites. O próximo passo de prova narrativa é uma avaliação com leitores que não vejam nome/códigos, seguida de observação de respostas e mudanças de tática em cenas reais. Ainda não ocorreu.

## Apêndice — rastreio dos 100 IDs

`direto`/`adaptado` reproduzem a autoavaliação do conjunto, com as diferenças de significado detalhadas acima. A tabela permite localizar cada interpretação; não é uma nota independente de qualidade.

| ID | D / F / V | Outras camadas | Classificação autoral |
| --- | --- | --- | --- |
| `monkey-d-luffy` | D03 / F17 / V09 | L08 / P04 | direto |
| `roronoa-zoro` | D11 / F15 / V04 | L16 | direto |
| `nami` | D23 / F01 / V01 | P09 | direto |
| `usopp` | D22 / F14 / V10 | — | direto |
| `sanji` | D23 / F08 / V16 | — | direto |
| `nico-robin` | D06 / F16 / V05 | — | direto |
| `naruto-uzumaki` | D01 / F15 / V09 | L02 | direto |
| `sasuke-uchiha` | D19 / F09 / V04 | L13 | direto |
| `sakura-haruno` | D22 / F10 / V11 | — | direto |
| `kakashi-hatake` | D21 / F12 / V10 | L06 | direto |
| `son-goku` | D23 / F04 / V09 | L02 | direto |
| `vegeta` | D22 / F15 / V04 | P18 | direto |
| `piccolo` | D04 / F01 / V04 | L06 | direto |
| `freeza` | D10 / F13 / V16 | — | adaptado |
| `tanjiro-kamado` | D04 / F03 / V08 | L09 | direto |
| `shinobu-kocho` | D19 / F14 / V16 | — | direto |
| `muzan-kibutsuji` | D13 / F13 / V04 | — | adaptado |
| `yuji-itadori` | D04 / F08 / V08 | P07 | direto |
| `satoru-gojo` | D12 / F06 / V10 | — | direto |
| `ryomen-sukuna` | D03 / F13 / V10 | — | direto |
| `luke-skywalker` | D03 / F06 / V01 | L07 | direto |
| `leia-organa` | D18 / F17 / V04 | P06 | direto |
| `darth-vader` | D10 / F13 / V04 | L20 | adaptado |
| `han-solo` | D08 / F02 / V10 | N07 | direto |
| `palpatine` | D10 / F14 / V05 | — | adaptado |
| `rey` | D15 / F11 / V01 | P05 | direto |
| `frodo-bolseiro` | D21 / F16 / V18 | L08 / P18 | direto |
| `samwise-gamgi` | D11 / F12 / V02 | P12 | direto |
| `gandalf` | D12 / F07 / V06 | — | direto |
| `gollum` | D17 / F14 / V17 | L18 / P14 | direto |
| `harry-potter` | D04 / F06 / V04 | L08 | direto |
| `hermione-granger` | D06 / F01 / V11 | P03 | direto |
| `severo-snape` | D11 / F14 / V05 | — | adaptado |
| `draco-malfoy` | D24 / F14 / V18 | P17 | direto |
| `katniss-everdeen` | D04 / F16 / V13 | P02 / N13 | direto |
| `peeta-mellark` | D22 / F08 / V08 | L17 | direto |
| `alan-grant` | D13 / F16 / V04 | — | direto |
| `ellie-sattler` | D04 / F10 / V07 | — | direto |
| `elsa` | D03 / F20 / V18 | N20 | direto |
| `anna` | D14 / F06 / V09 | L10 | direto |
| `olaf` | D09 / F05 / V03 | — | direto |
| `moana` | D12 / F15 / V11 | N01 | direto |
| `maui` | D24 / F14 / V16 | — | direto |
| `simba` | D20 / F20 / V10 | — | direto |
| `scar` | D10 / F14 / V16 | — | adaptado |
| `rafiki` | D12 / F07 / V21 | — | direto |
| `woody` | D17 / F13 / V04 | P01 | direto |
| `buzz-lightyear` | D15 / F18 / V15 | P05 | direto |
| `helen-parr` | D04 / F11 / V11 | — | direto |
| `edna-moda` | D23 / F10 / V04 | — | direto |
| `aang` | D04 / F03 / V12 | — | direto |
| `katara` | D05 / F08 / V08 | — | direto |
| `sokka` | D22 / F01 / V10 | — | direto |
| `toph-beifong` | D03 / F10 / V04 | — | direto |
| `zuko` | D15 / F15 / V18 | L07 / N03 | direto |
| `iroh` | D07 / F07 / V03 | L06 | direto |
| `batman` | D04 / F01 / V04 | N14 | direto |
| `superman` | D04 / F03 / V12 | P07 | direto |
| `mulher-maravilha` | D12 / F07 / V15 | — | direto |
| `alfred-pennyworth` | D04 / F08 / V06 | — | direto |
| `coringa` | D18 / F14 / V10 | — | direto |
| `lex-luthor` | D24 / F02 / V05 | — | direto |
| `arlequina` | D03 / F11 / V22 | P04 | direto |
| `hera-venenosa` | D04 / F13 / V21 | — | adaptado |
| `homem-aranha` | D21 / F11 / V10 | P12 / N22 | direto |
| `capitao-america` | D21 / F03 / V04 | — | direto |
| `homem-de-ferro` | D16 / F10 / V10 | — | direto |
| `tempestade` | D04 / F17 / V15 | — | direto |
| `magneto` | D04 / F13 / V15 | L10 | direto |
| `loki` | D24 / F14 / V16 | — | direto |
| `thanos` | D14 / F13 / V15 | L17 | adaptado |
| `doutor-destino` | D10 / F01 / V15 | — | adaptado |
| `eleven` | D03 / F20 / V18 | P17 | direto |
| `jim-hopper` | D04 / F13 / V04 | L19 | direto |
| `dustin-henderson` | D06 / F06 / V07 | — | direto |
| `steve-harrington` | D04 / F08 / V10 | — | direto |
| `o-doutor` | D12 / F11 / V07 | — | direto |
| `donna-noble` | D22 / F03 / V04 | — | direto |
| `o-mestre` | D10 / F14 / V10 | — | adaptado |
| `sherlock-holmes` | D06 / F10 / V07 | — | direto |
| `john-watson` | D07 / F19 / V20 | L03 | direto |
| `walter-white` | D24 / F14 / V05 | P05 | direto |
| `jesse-pinkman` | D20 / F20 / V18 | P17 | direto |
| `gus-fring` | D19 / F01 / V16 | — | direto |
| `link` | D21 / F10 / V13 | — | adaptado |
| `princesa-zelda` | D21 / F01 / V05 | — | direto |
| `ganondorf` | D10 / F13 / V15 | — | adaptado |
| `midna` | D17 / F14 / V10 | L15 | direto |
| `mario` | D04 / F15 / V09 | — | direto |
| `luigi` | D04 / F16 / V18 | — | direto |
| `bowser` | D10 / F13 / V04 | — | adaptado |
| `red` | D23 / F15 / V13 | — | adaptado |
| `blue` | D02 / F04 / V04 | — | direto |
| `cynthia` | D06 / F11 / V05 | — | direto |
| `cloud-strife` | D15 / F09 / V18 | N15 | direto |
| `tifa-lockhart` | D04 / F08 / V08 | L05 | direto |
| `sephiroth` | D18 / F14 / V21 | — | direto |
| `chell` | D13 / F10 / V13 | P13 | adaptado |
| `glados` | D23 / F13 / V05 | P04 | adaptado |
| `wheatley` | D22 / F06 / V07 | — | direto |

## Aplicação da revisão editorial 5.1.1

Esta seção registra uma aplicação posterior, autorizada, das correções **U08, D10 e D13**. As seções e a tabela anteriores são o snapshot da revisão original dos 100 casos: descrevem o baralho e o conjunto anteriores à aplicação. Seus hashes, conclusões, propostas e classificações foram preservados, sem atribuir retrospectivamente os resultados atuais à primeira avaliação. **D06 não foi alterada.**

O formato dos personagens e do catálogo continua **5.1**. A revisão do baralho é identificada por `revisao_editorial: "5.1.1"` nas três fontes JSON ativas. O catálogo de inspirações não recebeu um novo campo de versão; seu vínculo com a revisão atual é documentado nesta seção e nas nove notas reavaliadas.

### Decisão sobre os nove casos afetados

Os novos campos de D10 admitem poder sobre uma decisão sem pressupor cooperação ou um limite moral reconhecido. D13 agora distingue saída imediata de proteção duradoura da própria vida. As interpretações dos personagens não precisaram ser reescritas para caber: mudaram somente `audit.fit`, `audit.note` e `audit.gapTags` nos nove IDs abaixo.

| ID | Carta | Classificação anterior → atual | Justificativa da reavaliação |
| --- | --- | --- | --- |
| `freeza` | D10 | adaptado → direto | Autoridade sobre os recursos de Namek; o convite já não exige limite moral. F13/V16 preservam coerção e cortesia intimidatória. |
| `darth-vader` | D10 | adaptado → direto | Poder pretendido sobre o destino de Luke; parentesco não cria consentimento. L20 conserva proximidade e domínio como aspectos distintos. |
| `palpatine` | D10 | adaptado → direto | Concentração das decisões e supressão de contestação; F14/V05 continuam descrevendo encenação e formulação legal estreita. |
| `scar` | D10 | adaptado → direto | Tomar o trono e governar; manipular aliados não precisa ser interpretado como cooperação ou limite voluntário. |
| `doutor-destino` | D10 | adaptado → direto | Expandir soberania; preparação técnica e legitimação cerimonial continuam em F01/V15. |
| `o-mestre` | D10 | adaptado → direto | Domínio institucional no recorte John Simm; a formulação não impõe limite moral nem generaliza a todas as encarnações. |
| `ganondorf` | D10 | adaptado → direto | Concentrar autoridade e retirar meios de resistência; F13/V15 preservam coerção e reivindicação de soberania. |
| `bowser` | D10 | adaptado → direto | Autoridade imposta sobre uma região; o encaixe não acrescenta reciprocidade afetiva ou consentimento. |
| `muzan-kibutsuji` | D13 | adaptado → direto | Eliminar duradouramente a vulnerabilidade ao sol é proteção da própria continuidade, horizonte agora explícito na carta. O desejo não foi trocado por uma fuga imediata. |

As oito tags `d10-convite-cooperativo` e a tag `d13-objetivo-duradouro` foram retiradas desses casos. Suas novas notas explicam o encaixe na revisão, sem afirmar reforma moral dos personagens. Os sete casos adaptados por cautela de contexto permanecem: `severo-snape`, `hera-venenosa`, `thanos`, `link`, `red`, `chell` e `glados`.

U08 é um guia, não uma camada dos 100 personagens. Seu novo campo `Distribua` agora inclui a expansão 5.0 e os intervalos específicos por família; a leitura foi mantida. Isso fecha a omissão editorial sem acrescentar códigos ou inflar a cobertura da amostra.

### Métricas atuais e alcance da comparação

| Medida | Snapshot anterior | Após aplicação 5.1.1 |
| --- | ---: | ---: |
| IDs únicos / franquias | 100 / 27 | 100 / 27 |
| Atribuições / códigos distintos | 353 / 100 | 353 / 100 |
| Trios D/F/V distintos | 94 | 94 |
| Casos com D / F / V | 100 / 100 / 100 | 100 / 100 / 100 |
| Casos com L / P / N | 23 / 22 / 8 | 23 / 22 / 8 |
| Casos sem N | 92 | 92 |
| Rotulados direto / adaptado | 84 / 16 | 93 / 7 |

As distribuições por mídia, papel e frequência de cada código não mudaram. Todos os 100 objetos de personagem e todos os campos interpretativos, nomes, recortes, fontes, IDs e ordem dos registros permaneceram semanticamente idênticos. A diferença de nove classificações resulta da revisão dos textos das cartas e da reapreciação dos mesmos casos; **não é uma melhora medida em jogadores, um novo teste cego ou nove personagens adicionais**. As sete adaptações contextuais continuam sem ser tratadas como erros do baralho.

### Prova de preservação e sincronização

| Artefato | SHA-256 / resultado |
| --- | --- |
| Snapshot anterior do catálogo | `e86d8100963b81da76b28259e18d1408107dfccf8f1d224ba1d916482b013ae7` |
| Catálogo após as nove reavaliações | `7eae66fa26f9c50947b01ba665fa972cf771c1261a95d9be35a2b097268cd68c` |
| Baralho anterior à revisão | `6c33a7adb5187c8e909ab5a3bc6c4b283a79c670d03b67ea3c1c32333229f86d` |
| Baralho ativo com revisão 5.1.1 | `181d079735ed27358a911bc3e1affc249ac3815ca740fa0330115563210ea06f` |
| Baralho congelado 5.0 | `eb97dcae9235f08008fcea79ee765d8735b1b5eff5453a6e9b8dd79e09dab7e5`, preservado |
| Relatório histórico antes desta seção | SHA-256 `832a1624a01454ccdc2d7ac5257700d987b45ca4e4cce4cb34d3142c97e01222` dos 28303 bytes originais, preservados como prefixo |

Comparação estrutural independente dos hashes de cada carta antes/depois: **somente D10, D13 e U08 mudaram; as outras 138 cartas, incluindo D06, ficaram idênticas**. Códigos, títulos, famílias e módulos continuam iguais aos do arquivo congelado 5.0. A revisão veio do overlay editorial [editorial-5.1.1.json](../deck/editorial-5.1.1.json), aplicado pelo gerador; não foi uma alteração avulsa nas cópias distribuídas.

Os arquivos `deck/persona-cards-5.1.json`, `app/public/deck.json` e `skills/persona-cards/references/deck.json` foram comparados byte a byte e estão idênticos. O manual e `skills/persona-cards/references/deck.md` também estão idênticos. As novas leituras e os campos das três cartas aparecem no manual e na referência autocontida para GPT; skill e índice identificam a revisão 5.1.1.

**Verificações executadas nesta aplicação:**

- `node --test app/inspirations.test.mjs`: quatro testes passaram. Cobrem os 100 IDs, validação e finalização das 100 fichas, roundtrip no formato 5.1, conteúdo interpretativo específico, fontes permitidas e contagens de cobertura. Não demonstram reconhecimento narrativo nem desempenho em mesa.
- Comparações por Python padrão: hashes semânticos por registro e por carta, igualdade das três cópias JSON, preservação do hash 5.0, igualdade manual/referência e presença dos textos aprovados nas fontes geradas. Resultado: nove auditorias alteradas, zero interpretações alteradas e três cartas alteradas.
- Conferência do prefixo histórico deste relatório e das métricas atuais após a escrita. Nenhuma geração de PDF, edição de UI ou alteração de README foi executada por este revisor.

**Aceite da aplicação:** aprovado no catálogo e nas fontes textuais conferidas. Os achados U08, D10 e D13 estão atendidos pelos textos autorizados. D06 permanece apenas como hipótese editorial do snapshot, sem promoção nesta revisão. PDFs, build, navegação e publicação pertencem à validação de integração do responsável principal; os resultados desta seção não os substituem.

## Explicações visuais e todas as camadas na galeria

Este complemento registra um pedido posterior à aplicação editorial 5.1.1: mostrar as cartas selecionadas e explicar por que cada uma compõe a interpretação. O relatório histórico e a seção 5.1.1 anteriores foram preservados como estavam. Não houve outra revisão das cartas nem nova reclassificação dos nove casos já reavaliados.

### Correção da prévia e leitura das cartas

A prévia do catálogo em [InspirationGallery.jsx](../app/src/InspirationGallery.jsx) usava uma lista fixa de D/F/V. `CardCombination` passou a percorrer `character.enabled`, assim como a apresentação dos detalhes. Isso inclui L, P e N quando presentes e respeita sua ordem armazenada. O total de camadas da amostra continua sendo 353; exibir somente D/F/V ocultava 53 camadas opcionais, sem que elas estivessem ausentes dos personagens.

Nos detalhes, `IllustratedExplanation` consulta o baralho atual pelo código e apresenta família, código, título, ilustração e leitura oficial numa face de carta. A justificativa autoral em **Por que esta carta?** e a aplicação em **Na cena** ficam fora dessa face, para não atribuir ao texto oficial aquilo que pertence à interpretação do personagem. Não foram adicionados controles de seleção às faces: explorar e ler continuam separados de **Usar como base**.

**Prova por leitura:** prévia e detalhes percorrem `enabled`; a face usa `lookup`, `card.leitura` e `Art`, identificando a revisão atual; as duas explicações usam, respectivamente, `entry.rationale[family]` e `entry.character.fields[family]`. As novas faces são `article` dentro de `figure`, sem botões aninhados no controle de inspeção. As regras de texto consultadas no CSS permitem quebra de linhas; não foi encontrada supressão por limite de linhas nesses novos parágrafos. Isso não substitui a observação do layout, foco e animação no navegador em desktop e 390px, que cabe ao responsável pela integração.

### Metadados: 100 registros, 353 explicações

Cada registro recebeu `rationale`, fora do objeto `character`, com uma chave para cada família ativa. A conferência de todas as chaves e valores encontrou:

| Verificação | Resultado local |
| --- | ---: |
| Registros com `rationale` | 100 |
| Explicações não vazias | 353 |
| D / F / V | 100 / 100 / 100 |
| L / P / N | 23 / 22 / 8 |
| Divergências entre chaves de `rationale` e ordem de `enabled` | 0 |
| Objetos `character` alterados | 0 |
| Registros alterados quando se ignora apenas `rationale` | 0 |
| Classificações direto / adaptado | 93 / 7, preservadas |

O esquema da API agora inclui `rationale: dict[Family, str]` em `Inspiration`, permitindo devolver as explicações sem filtrá-las da resposta. São metadados do catálogo público de inspirações; não são novos campos das fichas pessoais e não alteram seus dados ou contratos de importação/finalização.

### Amostragem semântica independente

Foi feita leitura de explicações em 24 IDs, cobrindo D/F/V/L/P/N e os oito casos ativos de N. É uma amostragem das explicações, não leitura semântica integral das 353 justificativas. A cobertura estrutural de 353 foi conferida separadamente em todos os registros.

| Família | Exemplos conferidos | Critério observado nos textos |
| --- | --- | --- |
| D | `monkey-d-luffy`, `nico-robin`, `muzan-kibutsuji`, `darth-vader`, `palpatine` | Autonomia, resposta histórica, sobrevivência duradoura e autoridade são resultados desejados. O método coercitivo não vira prova de bondade nem obriga novo conflito interno. |
| F | `roronoa-zoro`, `nico-robin`, `palpatine`, `john-watson`, `glados` | Insistência, avaliação de risco, encenação, registros e controle são maneiras observáveis de tentar; o texto relaciona sua utilidade e seu custo ao recorte. |
| V | `roronoa-zoro`, `gollum`, `john-watson`, `hera-venenosa`, `severo-snape` | Concisão, alternância de registro, escrita, imagem sensorial e precisão verbal explicam expressão. A alternância não recebe diagnóstico, nem a metáfora vira prova técnica. |
| L | `roronoa-zoro`, `darth-vader`, `gollum`, `jim-hopper`, `thanos` | Memória de Kuina não ganha vontade atual; parentesco não produz consentimento; o Anel é distinguido de duas vontades humanas; obrigação de cuidado não legitima imposição; a Morte tem vontade própria apenas no recorte de entidade explicitado. |
| P | `monkey-d-luffy`, `katniss-everdeen`, `homem-aranha`, `rey`, `eleven`, `chell`, `glados` | Mudança de rota alheia, ajuda condicionada, tempo incompatível, pista confirmada, coerção material e perigo letal mudam a situação. A explicação não converte a pressão numa característica fixa do personagem nem numa resposta obrigatória. |
| N | `han-solo`, `katniss-everdeen`, `elsa`, `moana`, `zuko`, `batman`, `homem-aranha`, `cloud-strife` | Os textos identificam dois lados valorizados; liberdade/compromisso, segurança/confiança, dever/autoria, raízes/horizonte, verdade/pertencimento, controle/iniciativa, dedicação/presença e autoimagem/experiência. Custo externo isolado não foi usado como justificativa de N. |

O conjunto de IDs amostrados também inclui `hera-venenosa`, `severo-snape` e `john-watson` para confrontar a relação entre explicação e a carta específica, não apenas definições genéricas das famílias. Não foi encontrado defeito material nessa amostra. A ausência de N em Robin e nos demais casos sem dois lados estabelecidos permaneceu intacta. As explicações continuam sendo interpretações autorais de cenas propostas; não são validação canônica linha por linha, diagnóstico ou observação de jogo.

### Hashes e distinção das mudanças

| Estado do catálogo | SHA-256 |
| --- | --- |
| Snapshot histórico, antes das nove reclassificações | `e86d8100963b81da76b28259e18d1408107dfccf8f1d224ba1d916482b013ae7` |
| Aplicação 5.1.1: nove auditorias atualizadas, sem `rationale` | `7eae66fa26f9c50947b01ba665fa972cf771c1261a95d9be35a2b097268cd68c` |
| Complemento atual: adição das 353 explicações | `72e60b6439971d96229bd03b017e2f81ff76fe7d438da6bbf0d007b6388db7f4` |

Comparações semânticas por registro confirmaram que retirar `rationale` do conjunto atual reproduz integralmente o estado anterior: mesmos 100 IDs na mesma ordem, personagens, fontes, auditorias, classificações, camadas e interpretações. Portanto a diferença do hash atual não representa mais nove mudanças de aderência nem revisão do baralho. A adição de explicações é distinta da aplicação editorial 5.1.1 já registrada.

O prefixo deste relatório antes do complemento tinha 35645 bytes e SHA-256 `c1c3f5b26d2e73b82ea66ca8fd7ffff28c15818f9820de5af09641fee50b41db`; foi preservado. Os hashes anteriores documentam seus respectivos snapshots e não devem ser apresentados como o hash do catálogo atual.

**Verificações próprias deste complemento:** leitura focal de `InspirationGallery.jsx`, das regras de texto no CSS e do campo de resposta em `app/server.py`; leitura semântica da amostra indicada; agregação por Python/PowerShell das 353 chaves, valores não vazios, famílias, IDs e classificações; comparação de hashes semânticos por personagem e registro; conferência do prefixo histórico. Nenhuma edição de UI, API, catálogo ou PDF foi feita por este revisor neste complemento. O responsável pelo backend informou cinco testes Node e sete de API aprovados; essas suítes não foram repetidas nem são contabilizadas como execução própria.

**Aceite:** aprovado por leitura dos contratos, conferência estrutural integral dos metadados e amostragem semântica. A comprovação visual e de interação em desktop/390px e a publicação devem ser associadas às evidências reais do responsável pela integração. A existência de 353 textos e um build aprovado, isoladamente, não comprova sua apresentação no serviço publicado.
