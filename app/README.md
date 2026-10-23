# Persona Cards — mesa web

Mesa local em português para explorar o deck **5.1** por cartas, sem formulário. As 141 cartas têm uma abertura para ler ao puxar e uma ilustração própria: 126 cartas de criação e 15 guias. O [README principal](../README.md) explica as três entregas do projeto e o método completo, com cinco personagens de exemplo.

## Abrir

**Online:** [personcard.runictools.com](https://personcard.runictools.com/), sem instalar ou criar conta. Cada pessoa guarda suas combinações no próprio navegador.

Endereço local: **http://127.0.0.1:8766**. Para iniciar novamente no Windows, execute `iniciar.ps1` desta pasta. O servidor funciona em segundo plano e só escuta neste computador. O script reutiliza a instalação e a interface já construída; quando necessárias, prepara as dependências antes de iniciar.

## Usar

Comece pelas famílias Desejo, Forma de agir e Expressão. Alterne **Mesa / Grade** para ver a mão em leque ou comparar as cartas de uma família. Navegue pela mão com setas, gesto ou rolagem horizontal, vire a carta para consultar seus convites e use **Escolher esta carta** para levá-la à combinação. Explorar e virar não selecionam. Na Grade, tocar abre a carta na Mesa. As posições da combinação permitem voltar a uma escolha sem preencher ficha ou questionário.

O **+ após Expressão** acrescenta Vínculo, Pressão e Conflito interno como etapas 4–6, na ordem de escolha. Retirar uma camada guarda seu texto e carta para depois. Os guias U/G ficam separados em **Guias**.

**Salvar personagem** abre uma revisão com nome, informações pendentes, interpretações e foto opcional. **Finalizar** salva e apresenta a carta do personagem; ela pode ser editada, exportada em PNG ou usada como base de uma nova versão. Voltar da revisão conserva o rascunho. Textos de fichas antigas continuam preservados. O app não usa geração por IA.

Anime.js anima navegação, virada, Grade, colocação e finalização; scopes são limpos ao interromper ou sair. Movimento completo é o padrão, preservando uma escolha explícita por reduzido. O rodapé permite reduzir ou seguir o sistema.

Rascunhos e personagens são mantidos **neste navegador e neste endereço**. Exportar JSON/Markdown permite levar uma ficha para outro lugar; importar JSON validado cria uma nova ficha. Outro navegador ou outro endereço/porta tem armazenamento separado. O protótipo não tem contas, sincronização ou banco remoto.

Fotos JPEG/PNG/WebP são lidas e reduzidas no navegador: entrada até 10 MiB, saída JPEG até 960 px e dataURL de até 350 mil caracteres. O JSON inclui a foto. Não existe upload ao servidor; o limite do armazenamento do navegador continua valendo, e uma falha gera aviso para exportar antes de fechar.

## Inspiração

A aba **Inspiração** reúne 100 personagens da cultura pop com cartas interpretadas para um recorte específico. Busque nome ou obra, filtre por mídia/papel e abra os detalhes. **Usar como base** copia o exemplo para adaptar na sua criação; consultar não altera o rascunho. As fontes e a distinção entre obra e cena sugerida acompanham cada exemplo. Veja a [revisão editorial do sistema](../docs/REVISAO-100-PERSONAGENS.md).

## API

Documentação interativa em **http://127.0.0.1:8766/api/docs**, especificação em `/api/openapi.json`. Endpoints:

- `GET /api/deck`: deck completo.
- `GET /api/inspirations?q=...&medium=...&archetype=...`: coleção e filtros.
- `GET /api/inspirations/{id}`: exemplo individual.
- `GET /api/cards?q=...&family=...&module=...`: busca sem distinção de acento e filtros.
- `GET /api/cards/{code}`: carta individual.
- `POST /api/draw`: uma carta por família, módulos e exclusões explícitos. U/G não aceitos.
- `POST /api/characters/compose`: ficha de prompts com D/F/V, outras famílias opcionais e guias separados.
- `GET /api/health`: estado e versão.

A API é sem estado: compor uma ficha não a salva. Ela não lê os personagens privados do navegador. Como não há contas ou escrita persistente de fichas no servidor, não há credenciais a emitir. Swagger pode depender dos assets públicos de sua biblioteca. O modo online serve os mesmos arquivos por HTTPS; o modo local continua disponível.

## Desenvolvimento e conferência

Frontend: React/Vite/Anime.js com dependências travadas em `package-lock.json`. `npm ci` e `npm run dev` abrem a interface de desenvolvimento e encaminham `/api` ao servidor local. `npm run build` atualiza a interface servida pelo endereço principal; recarregar após build.

Servidor: ambiente isolado `.venv`, versões em `requirements.lock.txt`. Início direto: `.venv/Scripts/python.exe -m uvicorn server:app --host 127.0.0.1 --port 8766`. Contratos: `.venv/Scripts/python.exe -m unittest test_api`.

Conferência de entrega em ../docs/VALIDACAO.md.
