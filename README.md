# Persona Cards

**Personagens de RPG com intenção, voz e escolhas em cena.**

Persona Cards é um deck narrativo em português, uma skill para assistentes de IA e uma oficina web para criar e aprofundar personagens. O método começa com três cartas e transforma suas perguntas em ações concretas, relações e consequências.

![Oficina Persona Cards](docs/images/desktop.jpg)

## Comece em três cartas

1. **D — Desejo:** o que o personagem quer agora?
2. **F — Forma de agir:** como tenta conseguir?
3. **V — Expressão:** como comunica sua intenção?

Acrescente **L — Vínculo** e **P — Pressão** quando fizer sentido. **N — Conflito interno** só entra quando dois valores reais disputam uma escolha. Obstáculos e custos não exigem ambivalência. Os guias **U/G** são consulta e ficam fora do sorteio de personalidade.

Complete as cartas com pessoas, lugares e decisões da sua campanha. Dê ao personagem um hábito cotidiano e teste como reage a uma recusa. Preserve a vontade dos jogadores e das outras pessoas: a intenção de alguém não determina a resposta de outro.

### Um exemplo

**Brum, ogro artesão — D23/F15/V02/L06/N22/P11.** Entalhar brinquedos dá sentido aos seus dias. Refaz rodas quase perfeitas até as mãos doerem, mas também quer assistir ao teatro dos netos. Quando chega o horário, verifica que o defeito é acabamento, não segurança, e guarda as ferramentas. Essa escolha não resolve sua insistência para sempre.

[Cinco personagens e quinze ensaios](examples/cinco-personagens.md) · [Oito aplicações adicionais](examples/oito-aplicacoes.md)

## O que está incluído

| Material | Local |
|---|---|
| Deck 5.0 completo, 141 cartas | [JSON](deck/persona-cards-5.0.json) |
| Manual e textos das cartas | [Manual](deck/manual-5.0.md) |
| Skill com método, referências e consulta portátil | [persona-cards](skills/persona-cards/SKILL.md) |
| Material autocontido para GPTs e chats | [Instruções e referência](docs/persona-cards-gpt.md) |
| Aplicativo React + API FastAPI | [app](app/README.md) |

São **126 cartas de criação + 15 guias**: 72 cartas do núcleo, 36 da expansão anterior e 18 novas opções na versão 5.0. Os textos e códigos de 4.0 foram preservados. Esta versão não inclui novos PDFs de impressão.

## Rodar o aplicativo

Requisitos: **Python 3.12+** e **Node.js 22 LTS** com npm. Execute os comandos dentro de `app/`.

### Windows

Com Python e npm disponíveis no terminal:

```powershell
cd app
./iniciar.ps1
```

O script prepara as dependências quando necessário e inicia o servidor em segundo plano. Abra **http://127.0.0.1:8766**. Logs e PID ficam em `app/.runtime/`.

### Linux/macOS ou início manual

```sh
cd app
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock.txt
npm ci
npm run build
python -m uvicorn server:app --host 127.0.0.1 --port 8766
```

No Windows, para início manual use `python` e `.venv/Scripts/python.exe` no lugar da ativação acima.

O aplicativo permite pesquisar e inspecionar cartas, selecionar ou sortear combinações, manter cartas, editar camadas, salvar personagens e importar/exportar fichas. **Rascunhos e personagens ficam no navegador, por endereço e porta.** Exporte JSON para manter uma cópia. Não há contas, sincronização nem IA conectada; a síntese usa as cartas e o texto que você escreve.

API documentada em **http://127.0.0.1:8766/api/docs**; OpenAPI em `/api/openapi.json`. O servidor é local e escuta apenas em loopback.

## Usar a skill

Copie a pasta `skills/persona-cards/` para o diretório de skills do seu assistente. No Codex, o diretório habitual é `~/.codex/skills/`. Inicie uma sessão que descubra a skill e peça:

```text
Use $persona-cards para criar três NPCs de uma cidade portuária,
com intenções diferentes, vida cotidiana e uma cena para cada um.
```

Para ferramentas sem suporte a skills, forneça [persona-cards-gpt.md](docs/persona-cards-gpt.md) como instrução e referência. Isso não instala o método automaticamente em outros chats.

Consulta opcional, somente com a biblioteca padrão do Python:

```sh
python skills/persona-cards/scripts/cards.py get D19 F20 V22
python skills/persona-cards/scripts/cards.py search vocacao
python skills/persona-cards/scripts/cards.py draw --seed 42
```

O sorteio padrão usa D/F/V; N exige inclusão intencional. U/G são rejeitados no sorteio.

## Desenvolvimento e verificações

```sh
python -m unittest discover -s tests
cd app
python -m pip install -r requirements.lock.txt
python -m unittest test_api
npm ci
npm run build
```

Para desenvolvimento da interface, execute também o servidor local e `npm run dev` dentro de `app/`. As animações usam Anime.js com limpeza de instâncias e respeito a movimento reduzido. O GitHub Actions verifica integridade do deck, consulta/sorteio, contratos da API e build.

[Registro da conferência](docs/VALIDACAO.md) · [Como contribuir](CONTRIBUTING.md) · [Histórico](CHANGELOG.md)

## Alcance e limites

Os testes com personagens de cinema e os ensaios de RPG são avaliações autorais, não validação independente nem teste psicológico. Este repositório inclui exemplos originais; o texto integral de filmes não é necessário para usar o método. Não há garantia de qualidade universal, rapidez medida ou equilíbrio mecânico.

Cartas ajudam a escrever; não substituem contexto, revisão ou jogo em mesa. Não impõem trauma, diagnóstico, culpa, redenção ou conflito inexistente. O sistema é narrativo e pode acompanhar diferentes RPGs.

Referência conceitual inicial: [Anatomia do personagem — Jurandir Gouveia](https://jurandirgouveia.com/anatomia-do-storytelling/anatomia-do-personagem/). O deck e os exemplos são a elaboração deste projeto; não implicam endosso do autor da referência.

Licenciamento: ainda não foi definida uma licença de redistribuição para o projeto. As dependências mantêm suas próprias licenças.
