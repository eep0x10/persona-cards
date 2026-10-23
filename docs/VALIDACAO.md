# Verificação de entrega

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
