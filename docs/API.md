# API Persona Cards 5.2

[Projeto](../README.md) · [Arquitetura](ARCHITECTURE.md)

Swagger: `/api/docs`; OpenAPI: `/api/openapi.json`. Local: http://127.0.0.1:8766/api/docs. API pública sem contas, sem estado e sem acesso ao armazenamento pessoal do navegador.

| Operação | Resultado |
| --- | --- |
| `GET /api/health` | Estado, versão 5.2 e 166 cartas |
| `GET /api/deck` | Deck, módulos e revisão editorial 5.2.0 |
| `GET /api/cards?q=...&family=...&module=...` | Busca por conteúdo e filtros |
| `GET /api/cards/{code}` | Carta por código ou 404 |
| `GET /api/inspirations?q=...&medium=...&archetype=...` | Leituras históricas parciais, filtráveis |
| `GET /api/inspirations/{id}` | Exemplo por ID ou 404 |
| `POST /api/draw` | Sorteio de famílias; oito por padrão |
| `POST /api/characters/compose` | Composição completa ou rascunho explícito, sem salvar |

## Sorteio

```sh
curl -X POST http://127.0.0.1:8766/api/draw \
  -H 'Content-Type: application/json' \
  -d '{}'
```

O padrão sorteia OR/CV/D/F/V/L/P/N. `families` permite consultas/ressorteios parciais; `modules` e `excluded_codes` filtram a seleção. Módulos de criação: `nucleo`, `expansao`, `expansao_5` e `expansao_5_2`. U/G são rejeitados como famílias sorteáveis. Famílias repetidas, códigos desconhecidos ou conjuntos sem carta disponível são erros, não motivo para devolver um personagem incompleto como finalizado.

## Composição e jornada

```json
{
  "version": "5.2",
  "nome": "Lina Moura",
  "papel": "Barqueira e cartógrafa",
  "contexto": "Uma travessia precisa ser testada",
  "codes": ["OR12", "CV03", "D12", "F07", "V11", "L03", "P12", "N02"],
  "fields": {
    "OR": "Mapear correntezas deu a Lina um prazer que ainda orienta seu trabalho.",
    "CV": "Para Lina, cuidado precisa de presença e de gestos que os outros possam aceitar ou recusar.",
    "D": "Quero abrir uma travessia segura para os bairros isolados.",
    "F": "Traduzo os pedidos dos moradores e do conselho para negociar um teste.",
    "V": "Explico primeiro a medição, depois os pontos de retorno e só então o transporte.",
    "L": "Dara divide o barco comigo e quer preservá-lo para uma possível evacuação.",
    "P": "A inspeção e os remédios prometidos precisam do mesmo barco ao amanhecer.",
    "N": "Valorizo usar bem o recurso escasso e dar voz a quem assumirá o risco da travessia."
  },
  "journey": {
    "call": "Moradores convidam Lina para testar a travessia",
    "response": "Renegociar as condições",
    "fact": "Há somente um barco disponível ao amanhecer",
    "belief": "A rota merece teste, não certeza antecipada",
    "choice": "Ouvir os afetados e propor uma medição"
  }
}
```

Uma composição completa 5.2 exige nome explícito não vazio, um código de cada família, oito interpretações não vazias em `fields` e os cinco textos de `journey`. Repetir o primeiro prompt oficial da carta não preenche sua interpretação. G07 é incluído automaticamente como consulta em `guides`; não precisa ser enviado entre os códigos de personalidade. Chamado/resposta aceitam texto próprio, além das opções de 1d6.

A resposta JSON conserva as interpretações em `fields` e `layers`; `markdown` reúne os convites das cartas e os registros da jornada. Use os campos fornecidos para a ficha interpretada. A API não gera uma biografia por IA nem certifica a qualidade narrativa de texto não vazio.

`finalized:false` permite rascunho 5.2 parcial, inclusive `codes:[]`. Uma versão explícita `5.0` ou `5.1` preserva textos/códigos e retorna versão 5.2 com `source_version` original, oito famílias habilitadas e `finalized:false`; registros novos ficam vazios. Não são inventados OR/CV, passado ou valores para N. A finalização posterior precisa preencher as pendências.

Valores, comprimentos e erros 400/422 exatos estão no OpenAPI gerado. O código válido de uma carta não prova que N tem dois valores genuínos; isso exige interpretação e revisão.

## Catálogo e operação

Inspirações mantêm contexto histórico e `rationale` por camada existente. O mapa não completa camadas ausentes nem altera o objeto original. A galeria pode usá-las como base de um novo rascunho.

Hosts aceitos: `personcard.runictools.com`, `localhost`, `127.0.0.1` e `testserver`. Sem wildcard, token ou autenticação. Docker usa porta interna 8000 atrás do proxy HTTPS, sem porta de host ou volume de personagens. Veja [hospedagem](DEPLOY.md).
