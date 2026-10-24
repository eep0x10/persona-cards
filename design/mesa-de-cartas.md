# Mesa de cartas — direção e evidência

Estado: proposta visual A aprovada explicitamente pelo usuário em 23/10/2026; implementação em andamento. As imagens são mockups estáticos, não screenshots de uma mesa implementada.

## Pedido e contratos

Uma mesa extremamente simples para navegar, ler, escolher, trocar e guardar as cartas de um personagem, com profundidade 3D e movimento. Correção explícita do usuário: **nenhum formulário**. A nova superfície não terá input de texto, textarea, busca por texto, select, ficha lateral ou painel de preenchimento. Nome de uma nova combinação será automático. Dados antigos de nome, papel, contexto, interpretação e notas devem sobreviver no armazenamento/importação/exportação.

Dados conferidos no código: 141 cartas; D/F/V necessárias; L/P/N opcionais; U/G somente consulta; uma carta por família; escolha manual e sorteio local; `localStorage` na chave `persona-cards-workbench-v1`; importação 5.0/5.1; JSON/Markdown para cópia. Inspecionar não seleciona. A seleção muda imediatamente, sem depender de animação. A API permanece sem estado e mantém OpenAPI.

## Baseline e alternativas

`app-before-desktop.png` foi capturada no app local em 23/10/2026, antes das alterações do frontend: hero, catálogo com filtros à esquerda e formulário à direita, com dados fictícios de QA já existentes no navegador. Não representa dados de usuário real.

`mesa-alternativas.png` explora:

- **A — Mesa + cartas em foco:** mão navegável, leitura frontal e combinação na borda. Recomendada: a próxima decisão fica evidente e a revisão continua livre.
- **B — Mesa livre:** pilhas por família e três lugares centrais. Mais espacial, exige descobrir mais relações entre objetos.
- **C — Trilha guiada:** etapas em coluna. Boa orientação inicial, mas aproxima a experiência de um processo linear.

A imagem exploratória contém conteúdo esquemático; seus rótulos secundários não são fonte do deck. Nas prévias finais, os códigos e títulos visíveis foram conferidos contra as cartas reais.

## Composição proposta A

- `mesa-desktop-proposta.png`: cabeçalho discreto, passos D/F/V diretos, leque central com carta ativa frontal, uma ação principal e trio escolhido à vista.
- `mesa-mobile-proposta.png`: uma carta legível por vez, vizinhas parciais, setas e gesto horizontal, combinação compacta abaixo. Referência de composição 390 × 844; imagem exportada em resolução ampliada.
- Papel creme, mesa verde pinho, acento vermelhão, serifada para título da carta e texto simples para controles. Face ativa sem inclinação, vizinhas com rotação sutil; movimento interrompido durante leitura ou foco.
- A arte vem das 141 ilustrações folk do PDF. Preservar proporção e recortes seguros N04/U02/G02; carregar por carta/família, não todos os PNG de origem na abertura.
- Sem pesquisa de referências externas: a composição deriva da atividade física de explorar uma mão e colocar cartas numa mesa, usando o baralho real como referência visual.

## Movimento planejado — Anime.js 4.2.2

| Ação | Feedback | Movimento reduzido / interrupção |
| --- | --- | --- |
| Trocar família | Cartas da nova pilha entram na mão | Estado e leitura imediatos; cancelar entrada anterior |
| Navegar cartas | Carta ativa fica frontal; vizinhas se reposicionam | Troca direta; botões/gesto/teclado com mesmo resultado |
| Virar para consultar campos | Rotação curta de papel | Mostrar outra face imediatamente |
| Escolher | Atualizar combinação e elevar/colocar na posição D/F/V | Atualização imediata; sem callback para salvar estado |
| Trocar ou sortear | Animar só as cartas alteradas; manter travadas estáveis | Conteúdo final direto |
| Abrir conjunto salvo/ajuda | Painel curto de cartas ou explicação, sem campos | Foco previsível, fechar restaura controle inicial |
| Salvar/importar/erro | Confirmação localizada e anúncio acessível | Sem movimento necessário, conteúdo preservado |

Sem arrastar obrigatório, captura global de scroll, áudio obrigatório ou ornamentação em loop. Usar escopos por componente e limpar listeners/animações. Responder à mudança de `prefers-reduced-motion`. Preservar controle por teclado e touch.

## Produção das prévias

Ferramenta: `image_gen.imagegen`, modo integrado, imagens raster estáticas antes de código. Referências: screenshot local e `skills/persona-cards/print/preview-frentes-5.1-ilustrado.png`.

Brief dos prompts: “Persona Cards, mesa de feltro verde pinho, cartas reais de papel creme com arte folk em duas cores; três alternativas estruturais; depois composição A em desktop e 390px mobile, carta D01 Ter meu lugar frontal, D02/D03/D04 ao redor, passos D/F/V e combinação na borda; nenhuma entrada de texto ou formulário; leitura e contraste prioritários; sem hero de marketing ou dashboard”. Correção mobile: substituir o rótulo esquemático D14 por D04 Garantir proteção e arte real de mãos protegendo planta/chama, preservando o restante da composição.

## Responsáveis e evidência

Principal: README, direção, integração e navegação de QA. `frontend-sol`: implementação após aprovação explícita. `backend-sol`: inicializador, versão OpenAPI e consolidação de geração do PDF, sem mudança visual.

Prévia estática: disponível. Aprovação: recebida (“Aprovado, implemente essa mesa”).

### Checkpoint do primeiro fluxo implementado

Validação pelo principal no navegador integrado, em 23/10/2026. Evidência visual em `mesa-slice-desktop.png` (1366 × 900) e `mesa-slice-mobile.png` (390 × 844). Revisão independente da implementação visual ainda não realizada.

| Caso | Resultado observado |
| --- | --- |
| Desktop, carta D01 e combinação anterior | **pass**: nova composição de mesa/leque; arte individual e leitura frontal; dados antigos no tray |
| 390px, primeira versão | **fail corrigido**: bandeja cobria Escolher e parte da leitura; agente corrigiu bandeja no fluxo normal até 950px |
| 390px após correção | **pass**: Escolher termina em y645, bandeja começa y683; página sem overflow horizontal; Menu legível |
| 639px após correção | **pass**: Escolher termina em y762.8, bandeja começa y806.4; sem sobreposição |
| Ausência de formulário no slice | **pass**: DOM sem form/input/textarea/select |
| Explorar D02 antes de escolher | **pass**: tray preservou D01; seleção explícita atualizou somente D para D02 |
| Virar, salvar e biblioteca | **pass**: verso mostrou Quero/Mostre/Pedido; salvamento manteve nome anterior; duas fichas anteriores continuaram disponíveis |
| Recarregar | **pass**: D02/F05/V13 permaneceu na combinação; dados textuais antigos preservados por spread no código, exportação ainda não revalidada |
| Teclado e reversão rápida | **pass**: seta direita no controle da carta, próximo/anterior em sequência, título e tray coerentes |
| Anime.js real, modo normal | **pass**: navegação observada durante execução com opacity 0.6967 e matrix3d intermediária em card-content; contador de execução 2 |
| Redução de movimento dinâmica | **pass**: emulação de reduce produziu transform none, opacity 1 e conteúdo correto, sem depender do fim da animação |

A ilustração teve um breve estado de carregamento em uma captura imediatamente após reload; a captura subsequente confirmou a imagem e proporções corretas. A referência de QA é o estado carregado. Na expansão, revalidar dados via export/import, L/P/N, guias, módulos, sorteio/manter, Novo e gestão da biblioteca; esses fluxos ainda não eram expostos no slice. A emulação de mídia usada para testes deve ser removida no fechamento.

### Expansão e conferência final

Implementação concluída com a direção aprovada. A adição solicitada de **Mesa / Grade** conserva a linguagem das cartas e permite comparar uma família; abrir uma carta da Grade somente inspeciona. Grade em cinco colunas desktop e duas em 390 px. Anime.js aplica entrada escalonada, navegação do papel inteiro, virada e voo curto até a posição escolhida. A opção automática acompanha o sistema; escolha explícita de movimento completo/reduzido pode ser revertida por Seguir sistema.

**Pass:** seleção, biblioteca, duplicação, sorteio com travas/módulos, L/P/N, guias U/G, Novo com confirmação, exportações reais e importação 5.0/5.1, recusa de inválidos, manutenção de textos antigos e zero formulários. **Fail corrigido:** bandeja cobria o CTA também no desktop; passou para fluxo normal em todos os tamanhos. Medida final desktop: CTA bottom811,4 < bandeja top855; mobile: 496 < 537,8. Instruções densas ficam em verso rolável, com controle de virada separado.

Movimento real medido: `matrix3d` intermediária no papel ativo e vizinhas; Grade com opacidade 0,8519 e translateY2,37; voo de seleção com escala0,69038 e estado já atualizado. Movimento reduzido e sequência próximo/anterior/próximo terminaram em D02 com transform none, opacidade1 e nenhum voo. Revisão independente de persistência encontrou e fechou recuperação parcial e aquisição do getter localStorage. Testes simulados passaram; não foi reproduzido bloqueio real de armazenamento no browser.

Evidência atual: `mesa-final-desktop.png`, `mesa-final-mobile.png`, `mesa-final-grid-desktop.png`, `mesa-final-grid-mobile.png`. O checkpoint acima permanece como histórico do slice. A conferência visual final foi feita pelo principal; a revisão independente cobriu código e preservação, sem segunda inspeção visual. Não houve publicação ou impressão física nesta etapa.

## Etapas opcionais e carta do personagem — 23/10/2026

O pedido seguinte autoriza uma etapa de preenchimento após Salvar. A mesa conserva o estilo aprovado e continua dedicada às cartas; revisão e cartão final são estados separados. É uma ampliação funcional, sem nova direção visual ou gate de prévia.

- **Mesa:** D/F/V e botão + após Expressão. L/P/N aparecem como etapas 4–6 na ordem de adição; retirar preserva carta e interpretação. U/G continuam guias, fora das etapas do personagem.
- **Revisão:** nome, papel/contexto/notas opcionais, interpretações das famílias ativas e foto opcional. Voltar mantém o rascunho; Finalizar valida e salva. Legados conservam textos e identificadores.
- **Carta:** papel creme, identidade e retrato em destaque, combinação e interpretações legíveis, edição e exportação PNG. Sem foto, usar a arte existente ou composição tipográfica, sem gerar retrato por IA.
- **Dados:** retrato raster processado localmente e guardado/exportado com a ficha; não há upload ao servidor. Tamanho limitado e falha de leitura não substitui foto válida anterior.
- **Movimento:** completo por padrão, migrando o antigo modo automático uma vez; escolha explícita por reduzido é preservada. O usuário ainda pode seguir o sistema. Anime.js anima a adição das etapas, a abertura da revisão e a apresentação do cartão, com cleanup e estado independente da animação.

Responsáveis: `frontend-sol` implementa UI e PNG; `backend-sol` implementa modelo, validação e processamento local do retrato. Principal integra, documenta e confere desktop/390 px e produção.

Checkpoint real: **pass** em desktop 1366 × 900 e 390 × 844. Ordem P/N/L virou 4/5/6 e persistiu; progresso ajustado para 6 de 6. Nome vazio e seis convites sem interpretação foram identificados; foco na primeira pendência. Foto inválida recusada, foto válida convertida proporcionalmente em JPEG 960 × 320/116719 caracteres, campos preservados na recarga. Finalização e edição, biblioteca, legado sem novos atributos, JSON completo e PNG real 1200 × 1704 observados. PNG com seis camadas foi inspecionado visualmente, inclusive textos e arte.

Movimento completo apareceu após migrar automático; reduzido explícito permaneceu após recarga. Anime.js de apresentação final observado com matrix3d intermediária no papel e camadas em translateY12. Revisão independente encontrou e fechou cancelamento incorreto de upload ao mudar movimento e imagem corrigida oculta após erro. A corrida de processamento lento não foi reproduzida por temporização no browser; a correção foi conferida por leitura. Capturas publicáveis: `revisao-personagem-desktop.png` e `carta-personagem-desktop.png`; medições e limites em `docs/VALIDACAO.md`.

## Inspiração — 100 personagens

Ampliação funcional preservando mesa verde, papel creme, tipografia e artes folk existentes. A galeria favorece encontrar um personagem, compreender a interpretação e copiar uma base. Imagens do baralho são símbolos das ideias, sem prometer retratos dos personagens.

- Navegação: Inspiração acessível no desktop e celular; voltar à mesa preserva rascunho.
- Busca/filtros: nome/obra, mídia e papel narrativo, contagem e estado sem resultados com limpeza.
- Inspeção: recorte, cartas interpretadas e fontes; nenhuma alteração na criação.
- Uso: ação explícita, confirmação para substituir rascunho e cópia independente para adaptar.
- Movimento: Anime.js na atualização da coleção e abertura dos detalhes; scopes revertidos; preferência reduzida e interrupções mantêm estado final acessível.
- Proprietários: frontend-sol para UI; backend-sol para coleção/API/contratos; verifier-sol para revisão do sistema. Principal integra, documenta, verifica navegador e publicação.

Checkpoint do slice com **cinco exemplos reais**, antes da expansão: **pass** para identidade visual desktop1366×900 e detalhe390×844, busca vazia/reset, busca Nami, inspeção somente leitura, confirmação/cancelamento com foco restaurado e manutenção da carta D01 anterior. Usar Nami como base abriu revisão com interpretações; renomear para Cartógrafa do Cais e finalizar criou uma ficha independente no ambiente isolado localhost:8768. **Fail corrigido na fonte:** título ocupava cinco linhas mobile; título encurtado e contador reposicionado, metadados ampliados. A versão corrigida e os100 exemplos ainda aguardam build e conferência final. Nenhuma amostra parcial foi publicada.

Movimento do slice observado no navegador: filtragem Zoro com opacidade0,7663 e matriz com translateY8,6814; abertura do detalhe com opacidade0,6909 e matrix3d/translateY19,4262. Em reduzido, filtro e detalhe ficaram em opacidade1/transformnone; sequência rápida Zoro→Nami→Usopp abriu o conteúdo correto. Foco voltou ao cartão original ao cancelar substituição. A inspeção independente por verifier-sol não encontrou perda de rascunho ou referência compartilhada no clone.

Checkpoint final com **100 exemplos**: **pass** desktop1366×900 e390×844, sem overflow horizontal. O título curto e metadados ampliados foram conferidos no build final. Ordem inicial intercala mídias sem modificar o catálogo: Luffy, Luke, Elsa, Batman, Eleven e Link. Busca sem acento `aneis` devolveu quatro casos; filtros Cinema+Vilão devolveram Vader/Palpatine. Escape fechou o detalhe e restaurou foco no cartão. A ficha derivada do slice permaneceu após recarga. API local catálogo, item, health e OpenAPI responderam200. Capturas: `inspiracao-desktop.png`, `inspiracao-mobile.png`, `inspiracao-detalhe.png`. Revisão visual final pelo principal; leitura independente de preservação por verifier-sol.

## Cartas reais e justificativas — revisão 5.1.1

Pedido posterior: a prévia ocultava L/P/N por usar D/F/V fixos, e o detalhe exibia apenas caixas textuais. A correção mantém o visual existente e apresenta todas as famílias ativas. Detalhes usam faces ilustradas do baralho atual (família, código, título, arte, leitura e revisão), seguidas de justificativa autoral e aplicação em cena. Contexto fica depois das cartas; o cabeçalho foi compactado para priorizar a leitura solicitada. Faces são somente leitura, sem alterar escolhas.

Metadados `entry.rationale` cobrem353 camadas dos100 exemplos, fora do objeto character compatível. API os expõe; cópia de uma base preserva os mesmos dados de personagem. A explicação de P se refere à circunstância reveladora, não a um traço fixo. Revisão independente por leitura e amostra24IDs, incluindo8N, não encontrou defeito material.

Checkpoint real: desktop1366×900 e390×844, sem overflow; DOM da galeria contém100 personagens e353 códigos. Zoro lista D11/F15/V04/L16 na prévia e apresenta4 faces/4 justificativas. As cores por família correspondem ao PDF. No desktop a primeira dupla de faces e suas justificativas aparece no primeiro viewport do detalhe; no celular há uma coluna, texto legível e rolagem do diálogo. Escape restaura o foco.

Anime.js real observado em matrix3d intermediária nas faces, com translateY15,8424 na primeira e18 nas demais. Reduzido:4 faces com transformnone e4 explicações com opacity1/transformnone. Usar Zoro como base abriu4 camadas na revisão; finalizar Espadachim do Porto conservou L16 e a revisão5.1.1; PNG real foi inspecionado com4 camadas e rodapé5.1.1. O teste ocorreu somente emlocalhost:8769. Capturas: `inspiracao-detalhe.png`, `inspiracao-camadas-extras.png`, `inspiracao-detalhe-mobile.png`; galeria desktop/mobile atualizadas.
