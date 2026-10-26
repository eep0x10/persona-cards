# Impressão — Persona Cards 5.2 ilustrado

## Edição 5.2 — revisão 5.2.2

**169 cartas: 153 de criação e 16 guias.** O método usa OR/CV/D/F/V/L/P/N obrigatórias e o guia G07 — Chamado e destino. U/G são consulta, fora do sorteio de personalidade.

[Prévia real de G07 atualizado](preview-g07-5.2.2.png).

G07 agora distingue recusar o chamado de negociar condições e permite registrar mudança posterior da primeira resposta.

![Primeira folha da edição 5.2](preview-frentes-5.2-ilustrado.png)

[Prévia real de F21/F22 e G07 na revisão5.2.1](preview-revisao-5.2.1.png).

| Arquivo | Conteúdo |
| --- | --- |
| [Duplex ilustrado 5.2](Persona-Cards-5.2-Ilustrado-Duplex-A4.pdf) | 86 páginas / 43 folhas, frente e verso alternados |
| [Somente frentes](Persona-Cards-5.2-Ilustrado-Frentes-A4.pdf) | 43 páginas |
| [Somente versos](Persona-Cards-5.2-Ilustrado-Versos-A4.pdf) | 43 páginas espelhadas |
| [Manual rápido](Persona-Cards-5.2-Ilustrado-Manual-Rapido.pdf) | 3 páginas: criação completa, G07 e impressão |

Cartas de **92 × 130 mm**, quatro por A4. Use **retrato, tamanho real / 100%, virar na borda longa**. Teste o primeiro par consecutivo do duplex antes do lote. A última folha tem uma carta e três espaços vazios. Reinserção manual depende da impressora; não ajustar à página.

A fonte textual é [o deck 5.2](../../../deck/persona-cards-5.2.json); a correspondência de códigos e arte está no [manifesto 5.2](../../../deck/illustration_sheets_5_2.json). As fontes e artes são versionadas separadamente. A dimensão da ilustração pode variar conforme o texto, sem alterar a proporção do asset.

O [relatório digital 5.2](verificacao-impressao-5.2-ilustrado.json) registra corpo operacional de pelo menos **8,5 pt** em todas as cartas. Somente G06/G07 usam arte de **56 pt** para acomodar o texto dos guias; as demais mantêm pelo menos **80 pt**. Essas medidas são do arquivo digital, não prova física de leitura.

Para regenerar fontes textuais, execute `python deck/build_5_2.py` e depois `python deck/build_5_2_docs.py`. Estes comandos não geram PDFs. A geração e verificação da impressão são uma etapa própria, com ReportLab, pypdf, Pillow e fontes de sistema indicadas pelo renderizador. Veja [testes e limites](../../../docs/TESTING.md) e [validações por edição](../../../docs/VALIDACAO.md).

Conferência digital de texto, páginas e alinhamento no arquivo não comprova qualidade de corte, registro frente/verso ou leitura em mesa. Faça prova física antes de imprimir um lote. A criação de oito camadas também não é eficácia narrativa comprovada com jogadores.

## Edição histórica 5.1 — revisão 5.1.1

As 141 cartas anteriores permanecem disponíveis, com método e orientação históricos. Elas não são a edição completa de oito famílias 5.2.

- [Duplex 5.1](Persona-Cards-5.1-Ilustrado-Duplex-A4.pdf): 72 páginas / 36 folhas.
- [Frentes 5.1](Persona-Cards-5.1-Ilustrado-Frentes-A4.pdf) e [versos 5.1](Persona-Cards-5.1-Ilustrado-Versos-A4.pdf): 36 páginas cada.
- [Manual 5.1](Persona-Cards-5.1-Ilustrado-Manual-Rapido.pdf): 2 páginas.
- [Verificação histórica](verificacao-impressao-5.1-ilustrado.json).

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
