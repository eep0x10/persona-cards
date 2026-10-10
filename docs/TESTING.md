# Testes e limites

[Projeto](../README.md) · [Evidência visual](VALIDACAO.md)

Na raiz do repositório, com Python e dependências instaladas:

```sh
python -m unittest discover -s tests
python -m pip install -r app/requirements.lock.txt
python -m unittest discover -s app -p test_api.py
npm --prefix app ci
npm --prefix app run build
```

`tests/test_deck.py` protege identidade e hash das três cópias do deck, contagem/códigos únicos, consulta, busca e limites de sorteio. `app/test_api.py` protege deck, filtros/exclusões, erros, composição e OpenAPI. `tests/test_docs.py` verifica referências documentais locais, anchors internos, banner e navegação. O workflow Checks executa esses contratos e o build.

A conferência original no navegador observou seleção, sorteio com carta mantida, edição, salvamento, recarga, exportação/importação e rejeição de ficha inválida. Desktop e 390 px foram examinados sem transbordamento horizontal. Movimento reduzido foi observado; o modo completo não foi conferido visualmente naquele ambiente.

Os cinco personagens e quinze ensaios são exercícios autorais. Não houve avaliação independente, teste com jogadores, controle sem deck ou cronometragem. Não transformar essa evidência em porcentagem universal de qualidade. Um próximo teste útil é apresentar cenas sem códigos a leitores e observar reconhecimento, decisões improvisadas e lembrança em mesa.
