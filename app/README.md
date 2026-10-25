# Persona Cards — mesa web 5.2

Esta é uma das três formas de usar o **baralho narrativo Persona Cards**. A edição 5.2 / revisão 5.2.0 tem 166 cartas: 150 de criação e 16 guias. Veja [como jogar e os cinco exemplos completos](../README.md) ou use o [PDF](../skills/persona-cards/print/README.md) e a [skill](../skills/persona-cards/SKILL.md).

## Abrir

[Mesa online](https://personcard.runictools.com/), sem conta. Para executar localmente, instale Git, Python 3.12+ e Node.js 22 com npm. No Windows, execute `./iniciar.ps1` nesta pasta e abra **http://127.0.0.1:8766**. O serviço local escuta somente neste computador; o launcher reutiliza instalação, interface construída e serviço saudável.

Para instalação manual, script bloqueado ou Linux/macOS, veja o [início rápido](../docs/QUICKSTART.md). Após atualizar fontes, reconstrua a interface e reinicie a API. Ações normais de uso não exigem F5.

## Mesa e revisão

A criação completa usa **OR → CV → D → F → V → L → P → N**, todas obrigatórias, e o guia **G07 — Chamado e destino**. Não há etapas opcionais acrescentadas por +. Mesa/Grade, setas, gesto ou rolagem horizontal permitem explorar; virar e inspecionar não selecionam. Use **Escolher esta carta** para preencher uma etapa. U/G permanecem consulta, fora do sorteio de personalidade.

Em **Sortear · manter**, preserve escolhas com trava e ressorteie as outras. Uma seleção aleatória não garante coerência: interprete as cartas e troque o que contrariar os fatos. N precisa de dois valores genuínos; adversidade isolada exige outra N, não sua omissão ou redenção obrigatória.

**Salvar personagem** abre a revisão com nome, oito interpretações e os cinco textos de G07: chamado, resposta, fato, crença e escolha. Formulários ficam nessa etapa; foto, papel, contexto e notas são livres. Finalizar guarda e apresenta a carta do personagem; reabra, edite ou crie outra versão, preservando o salvo anterior. Exporte JSON para backup completo, além de PNG/Markdown para leitura.

Anime.js anima navegação, virada, Grade, colocação e finalização, com limpeza de scopes ao interromper/sair. O rodapé permite reduzir o movimento ou seguir o sistema; a preferência explícita permanece no navegador.

## Legados e armazenamento

Fichas 5.0/5.1 preservam nomes, textos, códigos, notas e retrato. Abrem como rascunhos pendentes 5.2, sem OR/CV, conflitos ou jornada inventados automaticamente. Complete as oito famílias e G07 antes de finalizar. Uma importação aceita não certifica completude narrativa.

Tudo fica no navegador/origem (protocolo, endereço, porta), sem conta, banco remoto de fichas ou sincronização. Limpar dados do site pode apagar trabalho local; exporte JSON antes de atualizar ou trocar de navegador. Falhas de armazenamento geram aviso e o original é protegido por backup local verificado quando houver recuperação de dados inválidos.

Fotos JPEG/PNG/WebP são processadas localmente: entrada até 10 MiB, saída JPEG até 960 px e dataURL de até 350 mil caracteres. JSON inclui o retrato. Não existe upload ao servidor; várias fotos podem atingir a cota do navegador.

## Inspiração

Os **100 personagens são leituras históricas parciais**, não 100 fichas completas no método de oito famílias. A galeria permite buscar, filtrar e conhecer o recorte, as cartas, justificativas e fontes. Prévia e detalhes mostram todas as camadas existentes no registro; não preenchem as ausentes.

**Usar como base** cria um rascunho independente e pede confirmação quando há uma criação atual. Complete as pendências sem modificar retroativamente o exemplo ou uma ficha salva. Consultar não altera seu rascunho. Veja [a revisão histórica](../docs/REVISAO-100-PERSONAGENS.md).

## API e consulta por terminal

Swagger em **http://127.0.0.1:8766/api/docs**, OpenAPI em `/api/openapi.json`. [Contrato completo](../docs/API.md).

- `GET /api/health`: versão 5.2, 166 cartas.
- `GET /api/deck`: deck e revisão 5.2.0.
- `GET /api/cards` e `GET /api/cards/{code}`: busca e consulta.
- `GET /api/inspirations` e `GET /api/inspirations/{id}`: catálogo histórico sem dados pessoais.
- `POST /api/draw`: oito famílias por padrão; filtros parciais para ressorteio.
- `POST /api/characters/compose`: oito códigos e jornada para composição completa; `finalized:false` permite rascunho. Versão explícita 5.0/5.1 preserva dados como rascunho 5.2 com `source_version`.

O serviço não lê localStorage nem persiste composições ou fotos. Não usa geração por IA. Swagger pode carregar assets externos da sua biblioteca.

A skill oferece consulta Python padrão na raiz do repositório:

```sh
python skills/persona-cards/scripts/cards.py get OR04 CV05 D03 F17 V09 L08 P04 N07 G07
python skills/persona-cards/scripts/cards.py draw --seed 42
```

## Desenvolvimento e validação

React/Vite/Anime.js usam `package-lock.json`. Execute `npm ci` e `npm run dev`; o proxy encaminha `/api` ao backend local. `npm run build` atualiza a interface estática.

Com o ambiente virtual preparado: `.venv/Scripts/python.exe -m uvicorn server:app --host 127.0.0.1 --port 8766`. Testes e limites estão em [TESTING.md](../docs/TESTING.md); evidências por edição, em [VALIDACAO.md](../docs/VALIDACAO.md). Não herdar validação visual da edição anterior nem confundir protótipos autorais com teste de mesa.
