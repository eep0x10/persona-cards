# Verificação de entrega

O protótipo original foi conferido em desktop de 1280 px e viewport de 390 px. Seleção, sorteio mantendo carta, edição, salvamento, recarga, reabertura, exportação JSON e reimportação foram observados. Ficha inválida foi recusada sem perder o rascunho. Escape restaurou foco à carta; no móvel, selecionar focou a edição.

Capturas em images/desktop.jpg e images/mobile.jpg mostram personagens fictícios criados para a conferência, não dados de uma campanha do usuário.

Anime.js está integrado com scope/revert. O ambiente de conferência sinalizava movimento reduzido; esse caminho foi observado. Movimento completo e troca da preferência nativa não foram conferidos visualmente naquele ambiente.

O pacote público acrescenta verificações de identidade das três cópias do deck, hash congelado, consulta por código, busca sem acento e exclusão de guias no sorteio. A API tem quatro testes de contratos. O build é conferido separadamente.

Os quinze ensaios narrativos são exercícios autorais, sem teste independente nem em mesa. Não demonstram uma taxa universal de qualidade.
