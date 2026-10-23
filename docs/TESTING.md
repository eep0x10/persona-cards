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

`tests/test_deck.py` protege o hash congelado de 5.0, identidade das três cópias ativas 5.1, contagem/códigos únicos, as 141 leituras e limites de sorteio. `app/test_api.py` protege deck, filtros/exclusões, erros, composição e OpenAPI. `tests/test_docs.py` verifica referências documentais locais, anchors internos, banner e navegação. O workflow Checks executa esses contratos e o build.

Para reconstruir a edição de leitura e os arquivos ilustrados de impressão, execute `python deck/build_5_1.py`, `python deck/build_5_1_docs.py` e `python deck/render_print_illustrated_5_1.py`. Depois, execute `python deck/verify_illustrated_print_5_1.py`. A renderização requer ReportLab, pypdf e as fontes Georgia/Arial indicadas no script; a verificação de transparência das artes também usa Pillow. A validação digital da impressão está registrada em [VALIDACAO.md](VALIDACAO.md); ela não substitui uma prova física.

A conferência original no navegador observou seleção, sorteio com carta mantida, edição, salvamento, recarga, exportação/importação e rejeição de ficha inválida. Desktop e 390 px foram examinados sem transbordamento horizontal. Movimento reduzido foi observado; o modo completo não foi conferido visualmente naquele ambiente.

Os cinco personagens e quinze ensaios são exercícios autorais. Não houve avaliação independente, teste com jogadores, controle sem deck ou cronometragem. Não transformar essa evidência em porcentagem universal de qualidade. Um próximo teste útil é apresentar cenas sem códigos a leitores e observar reconhecimento, decisões improvisadas e lembrança em mesa.
