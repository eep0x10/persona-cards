# Persona Cards — laboratório web

Protótipo local em português para experimentar o deck **5.0**. As 141 cartas são uma cópia fiel do arquivo do projeto, com 126 cartas de criação e 15 guias. Guias U/G nunca entram em sorteios de personalidade.

## Abrir

Endereço local: **http://127.0.0.1:8766**. Para iniciar novamente no Windows, execute `iniciar.ps1` desta pasta. O servidor funciona em segundo plano e só escuta neste computador. O script reutiliza a instalação e a interface já construída; quando necessárias, prepara as dependências antes de iniciar.

## Usar

Explore o catálogo por família, módulo, código ou conteúdo. Inspecionar uma carta não a seleciona; use a ação explícita para levá-la à ficha. A oficina começa com desejo/objetivo, método e expressão. Relação, pressão e conflito podem ser acrescentados; conflito interno só faz sentido quando houver dois valores reais em disputa.

Sorteie uma combinação, troque uma família ou mantenha cartas durante o sorteio. Complete nome, papel, contexto e camadas com detalhes da campanha. A síntese é um apoio baseado nas cartas e no texto que você escreve; não usa um serviço de IA nem promete uma história pronta.

Rascunhos e personagens são mantidos **neste navegador e neste endereço**. Exportar JSON/Markdown permite levar uma ficha para outro lugar; importar JSON validado cria uma nova ficha. Outro navegador ou outro endereço/porta tem armazenamento separado. O protótipo não tem contas, sincronização ou banco remoto.

## API

Documentação interativa em **http://127.0.0.1:8766/api/docs**, especificação em `/api/openapi.json`. Endpoints:

- `GET /api/deck`: deck completo.
- `GET /api/cards?q=...&family=...&module=...`: busca sem distinção de acento e filtros.
- `GET /api/cards/{code}`: carta individual.
- `POST /api/draw`: uma carta por família, módulos e exclusões explícitos. U/G não aceitos.
- `POST /api/characters/compose`: ficha de prompts com D/F/V, outras famílias opcionais e guias separados.
- `GET /api/health`: estado e versão.

A API é sem estado: compor uma ficha não a salva. Ela não lê os personagens privados do navegador. Como não há contas ou escrita persistente no servidor local, não há credenciais a emitir. Swagger pode depender dos assets públicos de sua biblioteca; a aplicação e o deck são servidos localmente.

## Desenvolvimento e conferência

Frontend: React/Vite/Anime.js com dependências travadas em `package-lock.json`. `npm ci` e `npm run dev` abrem a interface de desenvolvimento e encaminham `/api` ao servidor local. `npm run build` atualiza a interface servida pelo endereço principal; recarregar após build.

Servidor: ambiente isolado `.venv`, versões em `requirements.lock.txt`. Início direto: `.venv/Scripts/python.exe -m uvicorn server:app --host 127.0.0.1 --port 8766`. Contratos: `.venv/Scripts/python.exe -m unittest test_api`.

Conferência de entrega em ../docs/VALIDACAO.md.
