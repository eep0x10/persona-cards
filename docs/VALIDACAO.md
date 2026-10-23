# Verificação de entrega

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
