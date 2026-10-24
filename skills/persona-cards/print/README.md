# Impressão — Persona Cards 5.1 ilustrado

## Edição ilustrada 5.1 — revisão 5.1.1

**Revisão editorial 5.1.1:** textos de U08, D10 e D13 atualizados. Os quatro PDFs exibem a revisão 5.1.1; nomes dos arquivos conservam 5.1 para estabilidade dos links.

Todas as **141 cartas** têm uma abertura para leitura ao puxar e **uma ilustração própria** relacionada à situação da carta. Os 24 spritesheets PNG transparentes ficam em [`assets/`](assets/), com a correspondência exata de código e célula no [manifesto de ilustrações](../../../deck/illustration_sheets_5_1.json). As cenas seguem uma linguagem folk de recortes e duas tintas, com composição aberta; o verso comum usa um ornamento botânico simétrico. As artes foram geradas para esta edição e revisadas na página impressa.

![Primeira folha da edição ilustrada 5.1](preview-frentes-5.1-ilustrado.png)

As cartas medem **92 × 130 mm**, quatro por folha A4, com marcas de corte e 1 mm de sangria. O tamanho da ilustração se ajusta ao espaço de cada texto; nenhuma carta fica sem arte. O corpo operacional mínimo é 8,5 pt.

- [Duplex ilustrado 5.1](Persona-Cards-5.1-Ilustrado-Duplex-A4.pdf): 72 páginas / 36 folhas.
- [Frentes ilustradas](Persona-Cards-5.1-Ilustrado-Frentes-A4.pdf): 36 páginas.
- [Versos espelhados](Persona-Cards-5.1-Ilustrado-Versos-A4.pdf): 36 páginas.
- [Manual rápido](Persona-Cards-5.1-Ilustrado-Manual-Rapido.pdf): 2 páginas, com régua de 100 mm.

Selecione A4, retrato, **tamanho real / 100%**, impressão duplex **virando na borda longa**. Teste o primeiro par antes do lote. A última folha tem uma carta. A reinserção manual de papel depende da impressora. Conteúdo, encaixe e correspondência foram verificados digitalmente; impressão física e leitura em mesa ainda não foram testadas. Consulte [a verificação ilustrada 5.1](verificacao-impressao-5.1-ilustrado.json).

Para reconstruir e conferir a edição, execute `python deck/build_all_5_1.py` na raiz do repositório. O comando reúne produção do deck, referências, PDFs e verificação; `--help` lista os pré-requisitos. As etapas individuais continuam disponíveis: `build_5_1.py`, `build_5_1_docs.py`, `render_print_illustrated_5_1.py` e `verify_illustrated_print_5_1.py`, todas em `deck/`. Para renderizar é necessário `reportlab` e `pypdf`; a verificação também usa `Pillow`. As fontes Georgia e Arial são carregadas do Windows. A origem textual é [o deck 5.1](../../../deck/persona-cards-5.1.json); as cenas foram planejadas em [direções de arte](../../../deck/art-directions-5.1.json).

## Edição original 5.0

Todas as 141 cartas oficiais: 126 de criação e 15 guias. Cartas de 63 × 88 mm, nove por A4, marcas de corte e sangria de 1 mm.

- [Duplex: frente e verso alternados](Persona-Cards-5.0-Duplex-A4.pdf): 32 páginas / 16 folhas.
- [Frentes](Persona-Cards-5.0-Frentes-A4.pdf): 16 páginas.
- [Versos espelhados](Persona-Cards-5.0-Versos-A4.pdf): 16 páginas.
- [Manual rápido e impressão](Persona-Cards-5.0-Manual-Rapido.pdf): 2 páginas.

Selecione A4, retrato, tamanho real / 100% e **virar na borda longa**. Não ajustar à página. Teste o primeiro par antes do lote. Para impressão manual, combine as folhas de mesmo número; a reinserção depende da impressora.

| Módulo | Folhas separadas | Páginas duplex |
| --- | --- | --- |
| Núcleo | 1–8 | 1–16 |
| Expansão | 9–12 | 17–24 |
| Novidades 5.0 | 13–14 | 25–28 |
| Guias U/G | 15–16 | 29–32 |

Guias são consulta, nunca sorteio. A última folha tem seis cartas. O manual inclui régua de 100 mm. Conteúdo, dimensões, paginação e correspondência de frente/verso verificados digitalmente; teste físico de impressão não realizado.
