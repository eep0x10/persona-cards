# Verificação de entrega

As seções datadas abaixo são evidência das edições e ambientes identificados. A criação 5.2 exige oito famílias e G07; resultados e capturas 5.0/5.1 não comprovam automaticamente esse novo fluxo. Os próximos registros 5.2 devem distinguir geração documental, checks de código, PDF digital, navegador desktop/390px e eventual prova física.

## Finalização e carta do personagem — 23/10/2026

- Em origem isolada `localhost:8767`, o antigo modo automático migrou para movimento completo; escolha explícita por reduzido persistiu após recarga. D/F/V permaneceram no rascunho e o + acrescentou P, N e L como etapas 4, 5 e 6 na ordem de escolha. O progresso passou a 6 de 6.
- Salvar abriu revisão separada. Nome vazio e interpretações ainda iguais ao convite foram apontados como pendências; o foco foi ao nome. Preenchimento de seis interpretações, papel/contexto/notas e retorno/recarga mantiveram os dados. Importação de ficha 5.1 sem retrato/finalização conservou identidade, notas, cartas e interpretações e abriu a nova revisão.
- Upload real de PNG válido foi convertido localmente em JPEG 960 × 320 e 116719 caracteres, preservando a proporção. PNG de conteúdo inválido foi recusado sem perder os campos. Remoção do retrato manteve interpretações e permitiu finalizar sem foto.
- Finalização, reabertura na biblioteca após recarregar e edição foram observadas. JSON real exportado incluiu `finalized:true`, retrato e ordem `D/F/V/P/N/L`. PNGs reais com e sem foto foram baixados; o primeiro foi inspecionado como imagem 1200 × 1704, com seis interpretações legíveis e notas. O PNG tem limite de altura para evitar exportações enormes; JSON/Markdown conservam o texto completo.
- Revisão e carta final conferidas em desktop 1366 × 900 e 390 × 844; no móvel, largura de página 375 para viewport 390. Capturas de identidade fictícia em `design/revisao-personagem-desktop.png` e `design/carta-personagem-desktop.png`. Animação final observada com matrix3d intermediária no papel e entrada escalonada das camadas.
- Revisão independente fechou dois defeitos de foto antes da entrega: cancelamento indevido ao trocar movimento e imagem corrigida que permanecia oculta após erro. Seis testes Node do modelo, cinco testes Python de deck/documentação e cinco de API passaram; build integrado com 79 módulos aprovado.

## Publicação RunicTools — 23/10/2026

- `https://personcard.runictools.com/` abre sem conta ou login; DNS A com proxy Cloudflare ativo. HTTPS público e de origem conferidos, sem desativar validação de certificado. `/api/health` retorna 200, versão 5.1 e 141 cartas; OpenAPI e Swagger acessíveis.
- Build Docker real aprovado no servidor: imagem `persona-cards:runictools-20261023`, usuário 10001, filesystem somente leitura, 256 MB, porta 8000 apenas interna e nenhum volume de personagens. nginx-proxy validou a configuração; o serviço Mesa20 continuou saudável. O gate compartilhado já estava desativado por configuração anterior; não foi alterado.
- No navegador integrado público: origem nova começou sem fichas; seleção D02/F01/V01, salvamento e recarga mantiveram a combinação. Exportação gerou JSON 5.1 real; reimportação criou outro salvo e preservou o rascunho.
- Desktop 1366 × 900 e mobile 390 × 844 conferidos. Grade móvel com duas colunas e 24 cartas de Desejo; `scrollWidth` 375 para viewport 390; zero formulários/campos de edição. Animação real de navegação observada com `matrix3d` intermediária no domínio público. Preferência retornada a Seguir sistema após a conferência.
- Cinco testes do deck/documentação e cinco testes de API aprovados. A revisão independente identificou manifesto ausente no primeiro Dockerfile; o caminho foi corrigido antes do build real e o achado foi fechado por leitura.

## Mesa e Grade — conferência final em 23/10/2026

- Interface real conferida no navegador integrado em 1366 × 900 e 390 × 844. Grade de Desejo com cinco e duas colunas respectivamente; tocar D01 abriu a Mesa mantendo D12/F07/V11 na combinação. DOM sem formulários ou campos de edição; somente input de arquivo oculto para importação.
- Animação Anime.js observada em estados intermediários: carta ativa e vizinhas com matrizes de transformação durante navegação, entrada da Grade com opacidade 0,8519 e deslocamento de 2,37 px, e carta escolhida em voo até a combinação com escala 0,69038. Estado da combinação atualizado antes do término do movimento. No modo reduzido, navegação rápida terminou com `transform: none`, opacidade 1 e nenhum clone de voo.
- A faixa da combinação foi colocada no fluxo para deixar o botão Escolher livre: no desktop o botão terminou em y811,4 e a faixa começou em y855; no celular, y496 e y537,8 na posição de rolagem medida. Sem overflow horizontal no celular (`scrollWidth` 375 para viewport 390).
- D20, U02 e G02 tiveram versos longos conferidos em 390 px. Instruções com rolagem interna e botão de virada separado. U/G mostram apenas leitura e não entram na combinação.
- Exercitados: seleção e avanço D/F/V, sorteio com trava e módulos, ativação/retirada de N preservando dados, confirmação de nova combinação, salvar/reabrir/recarregar, duplicação, exportação real JSON/Markdown e reimportação. Uma ficha 5.0 foi importada como novo salvo; arquivo inválido foi recusado sem mudar o rascunho. Exportação de ficha anterior preservou papel, contexto, notas e campos.
- Recuperação do armazenamento testada com armazenamento simulado: itens válidos recuperados, backup bruto exato e exclusivo, preservação de backup anterior, falha de quota bloqueando sobrescrita e getter que lança `SecurityError` mantendo uso em memória. Revisão independente por leitura fechou os dois achados. Bloqueio de armazenamento não foi reproduzido em navegador real.
- Capturas finais em `design/mesa-final-desktop.png`, `mesa-final-mobile.png`, `mesa-final-grid-desktop.png` e `mesa-final-grid-mobile.png`. A conferência de importação usou origem local separada para não misturar fixtures com personagens existentes.
- Refinamento final em 390 × 844: D01 mostra a abertura inteira, com altura e conteúdo de 73 px, sem rolagem interna nessa carta. Botão Escolher termina em y688,8 e faixa começa em y730,6 no topo da página. Build final e cinco testes documentais aprovados; `git diff --check` sem erros.

## Edição 5.1 — 23/10/2026

- As 141 aberturas são únicas; as 141 cartas mantêm código, título, família, módulo e campos da edição 5.0. As três cópias ativas do JSON são idênticas em bytes. O JSON 5.0 congelado mantém seu hash.
- `python -m unittest discover -s tests`: 5 testes passaram. `python -m unittest discover -s app -p test_api.py`: 4 testes passaram. `npm --prefix app run build`: concluído.
- No navegador integrado, a busca encontrou D01 por um trecho exclusivo da nova leitura; o detalhe mostrou leitura e três campos, e o uso da carta levou ambos ao rascunho. Em 390 px, o detalhe e o rascunho permaneceram legíveis, com `scrollWidth` de 375 px para viewport de 390 px. O teste foi feito em uma instância local separada, sem alterar fichas preexistentes.
- Os quatro PDFs **ilustrados** foram convertidos com Microsoft MarkItDown. Como a extração mistura as duas colunas, `deck/verify_illustrated_print_5_1.py` conferiu no PDF os 141 códigos, títulos e leituras nas páginas correspondentes, 141 células com pixels opacos em 24 spritesheets PNG, dimensões A4 e contagens de 36 páginas de frentes, 36 de versos, 72 duplex alternadas e 2 de manual. As 72 páginas duplex foram rasterizadas sem erro. O renderizador rejeita texto que ultrapasse a área útil; o menor corpo é **8,5 pt** e a menor arte, **80 pt**.
- A inspeção visual abrangeu folhas das seis famílias, guias, casos densos, verso botânico e manual. A posição do verso é espelhada no código para impressão pela borda longa. Impressão física, tolerância da impressora, corte real e leitura em mesa ainda não foram medidos.

## Protótipo original 5.0

O protótipo original foi conferido em desktop de 1280 px e viewport de 390 px. Seleção, sorteio mantendo carta, edição, salvamento, recarga, reabertura, exportação JSON e reimportação foram observados. Ficha inválida foi recusada sem perder o rascunho. Escape restaurou foco à carta; no móvel, selecionar focou a edição.

Capturas em images/desktop.jpg e images/mobile.jpg mostram personagens fictícios criados para a conferência, não dados de uma campanha do usuário.

Anime.js está integrado com scope/revert. O ambiente de conferência sinalizava movimento reduzido; esse caminho foi observado. Movimento completo e troca da preferência nativa não foram conferidos visualmente naquele ambiente.

O pacote público acrescenta verificações de identidade das três cópias do deck, hash congelado, consulta por código, busca sem acento e exclusão de guias no sorteio. A API tem quatro testes de contratos. O build é conferido separadamente.

Os quinze ensaios narrativos são exercícios autorais, sem teste independente nem em mesa. Não demonstram uma taxa universal de qualidade.

## Inspiração — 100 personagens (23/10/2026)

Ambiente isolado `http://localhost:8768`, sem editar fichas do domínio público. Exatamente100 cartões no DOM, seis mídias e quatro papéis. Desktop1366×900 e390×844 sem overflow horizontal; galeria e detalhe inspecionados. Capturas: [desktop](../design/inspiracao-desktop.png), [mobile](../design/inspiracao-mobile.png), [detalhe](../design/inspiracao-detalhe.png).

Busca por Nami, resultado vazio/reset e busca sem acento `aneis` (quatro), filtros combinados Cinema/Vilão (dois), detalhes com fontes e Escape/foco foram exercitados. Inspecionar/cancelar manteve D01 no rascunho; confirmar Nami como base abriu revisão, renomear/finalizar criou Cartógrafa do Cais e a ficha permaneceu após reload. Não houve substituição automática de salvos.

Anime.js observado: filtro com opacidade0,7663/translateY8,6814; detalhe com opacidade0,6909 e matrix3d. Modo reduzido: opacidade1 e transformnone em lista e detalhe. Sequência rápida Zoro→Nami→Usopp terminou no personagem correto. A revisão independente por leitura não encontrou perda de rascunho ou clone compartilhado.

Testes do catálogo conferem100 IDs/nomes únicos, fichas completas, códigos e fontes estruturadas; fontes oficiais contextualizam as obras, não comprovam as interpretações. [Revisão do sistema](REVISAO-100-PERSONAGENS.md). Estes resultados não equivalem a teste com jogadores ou fidelidade universal às obras.

## Revisão editorial 5.1.1

Somente U08, D10 e D13 foram alteradas por overlay versionado. Três JSON ativos idênticos; 138 cartas restantes e fonte5.0 intactas, protegidas por testes. Skill local instalada foi sincronizada com os arquivos públicos do projeto, preservando arquivos locais adicionais.

Os quatro PDFs foram regenerados com identificação5.1.1. MarkItDown foi usado nos quatro arquivos anteriores e nos quatro finais; tabelas de duas colunas aparecem parcialmente intercaladas na extração, por isso os campos não foram reconstruídos desse texto. O verificador comparou diretamente todos os códigos, títulos, leituras e campos operacionais das141 cartas com o JSON nas frentes e no duplex; conferiu hashes, arte, A4 e36+36+72+2 páginas. Corpo mínimo8,5pt e arte mínima80pt mantidos. Inspeção visual das folhas3(D10),19(D13),29(U08) e manual não encontrou cortes ou sobreposição. [Folha com U08](assets/revisao-u08-5.1.1.png). Prova física ainda não realizada.

Mesa local `localhost:8769`: D10 nova leitura e campos conferidos no navegador; D13 nova leitura e verso rolável em390px; U08 exibe todos os intervalos de expansão e permanece fora da combinação. Rodapé identifica5.1.1. O formato JSON de fichas continua5.1 e importações5.0/5.1 passaram nos testes.

### Cartas visuais e todas as camadas da Inspiração

A galeria final exibiu100 registros e353 linhas de cartas no DOM (D/F/V/L/P/N). Zoro agora lista L16 junto de D11/F15/V04. Seus detalhes apresentaram4 faces ilustradas e4 justificativas específicas; a leitura oficial permanece na face e a explicação autoral fica abaixo. Desktop1366×900 e390×844 sem overflow horizontal; Escape devolveu foco à prévia. [Detalhe](../design/inspiracao-detalhe.png), [camadas extras](../design/inspiracao-camadas-extras.png), [mobile](../design/inspiracao-detalhe-mobile.png).

Movimento completo: faces observadas com matrix3d/translateY intermediários. Movimento reduzido: todas as4 faces e explicações do caso em transformnone/opacity1, conteúdo completo. Cópia da base abriu4camadas; finalização guardou L16 e um PNG real de4camadas com rótulo5.1.1 foi inspecionado. Os metadados353/353 foram verificados por testes e amostra editorial independente de24IDs; isso não equivale a conferir visualmente cada uma das100 combinações nem testar leitores.

PDFs são marcados como binários no Git, e o JSON de inspirações preserva seus bytes de origem, evitando conversão automática de finais de linha que alteraria os hashes publicados. O pacote de release deve conferir os hashes novamente contra os arquivos no ZIP.

## Edição 5.2 — oito famílias e Chamado e destino

Conferência de 25/10/2026: 166 cartas, 150 de criação e 16 guias. OR01–OR12 e CV01–CV12 preservam o conteúdo revisado; G07 registra chamado, resposta, fato, crença e margem de escolha. As três cópias ativas são idênticas. Os arquivos históricos 5.0/5.1 e os 100 recortes de inspiração 5.1 foram preservados; a galeria os identifica como leituras parciais para completar na 5.2.

Passaram 35 testes: 12 de baralho/documentação, dez de API e 13 de modelo/interface de dados. A finalização requer oito códigos válidos, oito interpretações próprias e os cinco campos de G07 tanto no navegador quanto na API. A revisão independente encontrou e fechou a divergência em que a API aceitava interpretações vazias. Legados continuam rascunhos sem passado ou conflito inventado.

Foram geradas 25 artes originais por ImageGen, no estilo folk já adotado, em quatro spritesheets de seis cenas e uma imagem individual de G07. Os 29 arquivos de atlas, incluindo os anteriores, têm alfa e cobrem as 166 cartas. Os assets de impressão e web têm bytes idênticos. CV02 usa somente um recorte de margem para evitar fragmento da célula vizinha, equivalente na tela, PNG e PDF; as imagens-fonte não foram editadas.

Os quatro PDFs finais foram convertidos primeiro com MarkItDown. A extração em múltiplas colunas não é usada para reconstruir a ordem das cartas; o verificador também compara todos os códigos, títulos, leituras e campos diretamente com o JSON. Passaram a conferência A4, 42 frentes, 42 versos, 84 páginas duplex e manual de três páginas, hashes e corpo mínimo de 8,5 pontos. A codificação das imagens no PDF foi otimizada sem alterar amostras RGB/alfa, verificadas por hash; não houve redução de resolução. As artes das cartas de criação têm no mínimo 80 pontos; G06/G07 reservam 56 pontos para manter texto legível. Inspeção visual de Origem, Convicção, G07 e manual não encontrou sobreposição. [Prévia real](../skills/persona-cards/print/preview-frentes-5.2-ilustrado.png). Prova física e teste com jogadores continuam pendentes.

No navegador integrado, a mesa foi conferida em 1366×900 e 390×844: oito etapas, seleção e troca dinâmica, Mesa/Grade e zero campos de formulário na mesa. A revisão recusou uma ficha com uma carta e também recusou oito interpretações enquanto faltavam três respostas do guia. Após completar, guardou Iara do Cais com oito cartas e G07; PNG real e JSON 5.2 foram baixados e inspecionados. Nenhum dado pessoal foi usado. [Mesa desktop](../design/mesa-5.2-desktop.png), [mobile](../design/mesa-5.2-mobile.png), [guia mobile](../design/chamado-destino-5.2-mobile.png), [PNG completo](../design/personagem-5.2.png).

O pipeline de publicação tem contrato versionado, snapshot da imagem ativa e recuperação serializada. Dois problemas de concorrência na reversão foram encontrados e fechados por revisão e simulação Linux com locks reais: exclusão entre rollback/publicação e recusa de recuperação obsoleta após uma publicação posterior. A verificação de um snapshot exportado foi executada na infraestrutura real. Esses resultados não equivalem a interromper a produção para ensaiar uma reversão completa.

## Inspiração 5.2 completa — aplicação 5.2.1 (25/10/2026)

Os mesmos100 IDs e fontes foram preservados. O catálogo tem800 escolhas,800 interpretações e justificativas,500 respostas de G07 e100 explicações de jornada. A comparação por valor preservou todas as cartas e interpretações já existentes. Acréscimos são propostas autorais explícitas; não afirmam validação canônica ou playtest.

Revisão editorial independente: OR/CV/N/G07 dos100 registros, além dos excerpts/auditorias. Foram corrigidos encaixes de Origem em Tempestade, Gollum, Alan Grant, Ellie Sattler, Edna Moda e Sukuna; os N propostos de Gollum/Grant passaram a N11. As50 novas justificativas CV do primeiro lote foram refinadas para explicar a ponte entre antecedente, convicção e ação, sem repetir o campo. Conferência final encerrou os achados.

Testes executados:12 de repositório/documentação,10 de API e13 Node; build Vite aprovado. Os testes conferem completude5.2 nos100 registros, códigos,500 campos de jornada, importação/cópia sem perda, fontes e filtros. O build avisa que o bundle principal excede500kB minificado (aproximadamente207kB gzip); isso não impede funcionamento, mas permanece uma oportunidade de divisão futura.

CUA local: Luffy e GLaDOS exibiram nove faces reais (oito famílias e G07) e nove explicações. Em390px o diálogo manteve largura320px, sem rolagem horizontal interna; cartas, justificativas e respostas do guia foram inspecionadas. Fechar manteve busca e foco no personagem. Usar como base exigiu confirmação diante de rascunho, aceitou cancelamento e copiou oito interpretações e cinco respostas para revisão; finalizar guardou um personagem completo na origem de QA. Movimento normal exibiu transformações3D intermediárias; reduzido manteve as nove faces em transformnone/opacity1. Essa amostra não equivale a inspecionar manualmente800 faces nem a um teste com leitores.

Catálogo final SHA256: `ed87e3b55a5bf9ff9d97e68701e91216f1557add7c6b79b158c880844ce9e07e`. Capturas de QA ficam no diretório local ignorado `tmp/inspirations-52/`.

## Revisão dos105 — aplicação5.2.2 (26/10/2026)

Foram acrescentados Edward Elric, Alphonse Elric, Frieren, Gon Freecss e Killua Zoldyck, com recortes explícitos, oito escolhas justificadas e G07. As100 leituras anteriores foram percorridas em todas as famílias e na jornada:40 personagens tiveram troca de código, totalizando60 cartas; manutenções e refinamentos também estão registrados. O registro editorial contém945 decisões (oito famílias e G07 para cada pessoa), fontes primárias com limites e vínculo ao hash do catálogo. Não representa comprovação canônica de cenas hipotéticas nem playtest.

Revisão cruzada independente: cinco novos,40 casos com códigos alterados e dez amostras sem troca de código. Foram fechados encaixes incorretos de F19 como memória mental, L03 sem obra conjunta e N14 para improvisação própria. Coringa/Loki/Mestre usam N18 com limite estratégico voluntário; os cinco novos distinguem responsabilidades, agência e recortes sem misturar fases de adaptação.

Execução local:13 testes Python de repositório/documentação/revisão,10 de API e14 Node aprovados,37 no total. Build Vite aprovado com o aviso de bundle grande já conhecido (cerca de230,49kB gzip). O teste editorial confere105 registros e decisões de todas as famílias, hash, códigos anteriores/atuais e fontes; o teste estrutural confere840 justificativas e525 respostas de G07.

CUA no navegador integrado: Edward, Alphonse, Frieren, Gon e Killua abriram cada um com nove faces reais (oito famílias e guia), nove explicações e cinco respostas. Frieren a390px manteve diálogo320px sem rolagem horizontal interna; texto, N22 e G07 foram inspecionados. Usar sua base pediu confirmação diante de rascunho, copiou oito interpretações e a jornada e permitiu finalizar na origem de QA. A versão final de Coringa mostrou N18. Anime.js exibiu transformações3D intermediárias; movimento reduzido manteve nove faces em transformnone/opacity1. A inspeção visual amostral não equivale a ler manualmente todas as840 faces.

Catálogo final SHA256: `755cf04cf8abead0bab024e97f1a170b283b116c3b6f33756c9835286c59ceed`. [Registro dos105](REVISAO-105-PERSONAGENS.md). Capturas locais ignoradas: `tmp/review-105/`.

## Revisão editorial 5.2.1 — aplicação 5.2.3 (26/10/2026)

O deck passa a 169 cartas (153 de criação e16guias): F21, F22 e N23 foram acrescentadas; OR03/N14/P12/L13/D06 e os guiasG06/U08 foram esclarecidos. Históricos5.0/5.1 e fonte da expansão5.2.0 permanecem preservados. As três cópias têm SHA256 `4dae5bb05ba6376bd09ac3d7bcf16a6307e159a236b66f1bef457fce4b897128`.

Os105 personagens foram percorridos nas oito famílias eG07, com945 decisões registradas. Houve15 trocas: trêsF21, trêsF22 e noveN23; Edward mantémN18 por sua linha ética. A auditoria anterior foi preservada e uma leitura independente conferiu as15trocas, Edward e manutenções deN14. Catálogo final SHA256 `b5d21adc69daa45083a64330a59131d9ce0bf7d04d1fe3d5278774b222e07bf6`. As cenas continuam propostas autorais, não novos fatos canônicos ou playtest.

Uma spritesheet original ImageGen acrescenta três artesfolk com alfa, em2×2células, mantendo a última vazia. O arquivoPNG é idêntico na impressão e na web. Os30atlas cobrem169códigos. Os quatro PDFs foram primeiro convertidos viaMarkItDown; a extração mistura colunas e não serve para reconstruir a ordem das cartas. O verificador cruzou todos os textos com oJSON e conferiu43frentes/43versos/86duplex/3manual, A4, hashes e corpo mínimo8,5pt. Inspeção visual das novas cartas, G06/OR03 e instruções de impressão passou. Prova física permanece pendente.

Verificação local:14testesPython de repositório,11deAPI e15Node aprovados; buildVite aprovado, mantendo o aviso conhecido de bundle acima500kB. CUA conferiu F21/F22 no leque, grade com22formas e galeriaIroh com oito cartas, explicações eG07; desktop e390px inspecionados, sem rolagem horizontal do documento. Nenhuma alteração de UI ou motor de animação: Anime.js existente foi preservado. Evidências locais ignoradas em `tmp/revision-521/`.

A integraçãoMesa20 preserva as29folhas anteriores e acrescenta a30ª, com169códigos;41testesPython e9Node aprovados. Publicação e validação pública são registradas no resultado da release, separadas destas provas locais.
