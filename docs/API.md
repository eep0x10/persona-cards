# API local

[Projeto](../README.md) · [Arquitetura](ARCHITECTURE.md)

Swagger: http://127.0.0.1:8766/api/docs. OpenAPI: `/api/openapi.json`. API sem estado, sem contas e sem acesso às fichas locais do navegador.

| Operação | Resultado |
| :--- | :--- |
| `GET /api/health` | Estado, versão e quantidade de cartas |
| `GET /api/deck` | Deck completo |
| `GET /api/cards?q=...&family=...&module=...` | Busca sem distinção de acentos e filtros |
| `GET /api/cards/{code}` | Carta por código, ou 404 |
| `POST /api/draw` | Uma carta por família de criação, com módulos/exclusões |
| `POST /api/characters/compose` | Ficha de prompts e Markdown, sem salvar |

Exemplo de sorteio em terminal POSIX:

```sh
curl -X POST http://127.0.0.1:8766/api/draw \
  -H 'Content-Type: application/json' \
  -d '{"families":["D","F","V"],"modules":["nucleo"],"excluded_codes":[]}'
```

Composição:

```json
{"nome":"Brum","papel":"Artesão","contexto":"A apresentação começa hoje","codes":["D23","F15","V02"],"guide_codes":["G06"]}
```

Famílias sorteáveis: D/F/N/L/V/P, sem repetição. Módulos: `nucleo`, `expansao`, `expansao_5`. U/G são rejeitados no sorteio. Cada carta 5.1 traz `leitura`, abertura para leitura ao puxar, e `campos`, instruções operacionais preservadas de 5.0. A busca consulta ambos. Composição exige D/F/V; outras famílias são opcionais, uma carta por família. Guias U/G entram apenas em `guide_codes`. Códigos e combinações inválidos retornam 400/422 conforme a validação. Os limites exatos de campos e listas constam no OpenAPI.

O host é restrito a localhost/127.0.0.1 (e testserver nos testes). Alterar isso e expor na internet exige um projeto operacional adicional; não há tokens ou autenticação nesta API local.
