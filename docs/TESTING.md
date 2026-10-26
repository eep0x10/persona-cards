# Testes e limites — edição 5.2

[Projeto](../README.md) · [Registros por edição](VALIDACAO.md)

Com dependências instaladas, na raiz:

```sh
python -m unittest discover -s tests
python -m pip install -r app/requirements.lock.txt
python -m unittest discover -s app -p test_api.py
node --test app/model.test.mjs app/inspirations.test.mjs
npm --prefix app ci
npm --prefix app run build
```

O contrato 5.2 deve proteger 169 códigos únicos, 153 cartas de criação, 16 guias, oito famílias obrigatórias, G07 e as três cópias JSON idênticas. Arquivos 5.0/5.1 permanecem históricos. A geração documental é `python deck/build_5_2_docs.py`, depois de `deck/build_5_2.py`; ela não gera PDFs.

A API distingue sorteio padrão de oito cartas, ressorteio parcial, composição completa com jornada e rascunho legado. O modelo do navegador deve preservar textos de até 20 mil caracteres, foto e notas; importação antiga não pode inventar passado. Complete oito interpretações e os cinco registros antes de declarar uma ficha finalizada.

Os testes de documentação verificam links, anchors, assets, banner e navegação. O conteúdo das 169 cartas no manual/GPT deve corresponder ao JSON, sem reescrever a fonte congelada. Testes e build são necessários, mas não comprovam layout, foco, decodificação raster, exportação PNG ou animação.

A validação no navegador precisa cobrir desktop e 390px: oito escolhas, revisão, G07, recusa de finalização incompleta, recarga, reabertura, exportação/importação, dados legados, filtros e movimento reduzido. Use origem de teste isolada; não substitua dados pessoais para testar migração.

Os 105 personagens têm oito cartas, oito interpretações e justificativas, cinco respostas de G07 e explicação da jornada. Os testes verificam completude estrutural 5.2, códigos reais, importação sem perda, identidade, fontes e filtros. A revisão editorial precisa conferir valores genuínos em N, agência em L e separação de fato/crença/proposta. A [revisão histórica](REVISAO-100-PERSONAGENS.md) preserva critérios anteriores; nenhum desses checks substitui playtest nem mede qualidade narrativa universal.

PDFs 5.2 exigem conversão inicial via MarkItDown, conferência de códigos/textos/arte, A4, 43 frentes, 43 versos, 86 páginas duplex e 3 páginas de manual, além de inspeção visual. Extração pode misturar colunas; não prometa extração perfeita nem impressão física aprovada com base só no arquivo digital.

Resultados executados devem ser registrados em [VALIDACAO.md](VALIDACAO.md) identificando edição, ambiente e limite da prova. Não reutilizar capturas ou resultados 5.1 como validação automática de 5.2.

A suíte `tests/test_inspirations_review.py` vincula os 105 registros editoriais ao SHA256 do catálogo, às escolhas atuais e às nove justificativas de revisão por personagem. Ela verifica rastreabilidade, não transforma interpretação em fato canônico.
