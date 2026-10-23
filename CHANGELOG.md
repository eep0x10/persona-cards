# Histórico

## Carta do personagem e etapas opcionais

- Botão + após Expressão acrescenta L/P/N como etapas 4–6 na ordem escolhida.
- Salvar abre revisão com informações pendentes e foto opcional; finalizar cria carta do personagem, com edição e exportação PNG.
- Retrato processado e armazenado no navegador, com validação raster e limite de tamanho; JSON preserva foto e compatibilidade com fichas anteriores.
- Movimento completo passa a ser o padrão; preferência explícita por reduzido é preservada.

## Hospedagem pública — RunicTools

- Mesa disponível em `https://personcard.runictools.com/`, sem instalação ou conta; personagens continuam no navegador de cada pessoa.
- Perfil Docker de produção com build Node/Python, isolamento do serviço, HTTPS pelo proxy e domínio permitido explicitamente na API.
- Instruções de hospedagem, transferência entre endereços e privacidade atualizadas.

## Edição de leitura e impressão — 5.1

- Aberturas originais para as 141 cartas, com funções das famílias preservadas e textos integrados ao app, API, manuais e busca.
- Edição ilustrada em 92 × 130 mm: 141 cenas próprias organizadas em 24 spritesheets, arte folk de composição aberta, cores por família e verso botânico comum e simétrico.
- PDFs A4 ilustrados de frentes, versos, duplex e manual rápido, com sangria e marcas de corte; edição 5.0 preservada para consulta.
- Importação de fichas 5.0 mantida. Testes do deck e da API, build e validação digital dos PDFs atualizados.
- README em português e inglês passa a apresentar o baralho físico e as regras de uso antes da oficina opcional; cinco exemplos didáticos mostram três interpretações de cultura pop e uma aliada e uma vilã da mesma campanha de RPG.
- README autocontido organizado em PDF, skill e web; cinco montagens completas no próprio documento, com instruções de uso para leigos.
- Inicializador passa a consultar versão/contagem do deck e reutiliza serviço saudável; versão OpenAPI acompanha o deck. Geração ilustrada consolidada sem substituição de funções em tempo de execução, com comando único `deck/build_all_5_1.py`.
- Aplicação reconstruída como mesa sem formulário: leque, Grade por família, frente/verso, combinação guiada D/F/V e módulos opcionais. Anime.js anima navegação, virada, Grade e colocação de cartas, com controle de movimento reduzido.
- Biblioteca, importação 5.0/5.1 e exportação JSON/Markdown preservam os textos anteriores. Recuperação parcial do armazenamento exige backup verificado antes de gravar; armazenamento bloqueado mantém uso em memória com aviso.

## Impressão — 5.0.2

- Todas as 141 cartas 5.0 na pasta print da skill, com frente/verso A4, corte e manual rápido.
- Verificação de conteúdo, dimensões e espelhamento; impressão física ainda não testada.
- Skill instalada e pacotes públicos incluem os PDFs.

## Correção documental — 5.0.1

- README reorganizado com banner de identidade, badges verificáveis, navegação e resumos português/inglês.
- Guias de início rápido, operação, skill, arquitetura, API, privacidade, testes e identidade.
- Verificação automatizada de assets, links, anchors e estrutura do README.
- Documentação atualizada nos pacotes; deck e comportamento do aplicativo preservados.

## Publicação inicial — Persona Cards 5.0

- Deck com 126 cartas de criação e 15 guias; preservação das 117 cartas da versão 4.0.
- Método rápido D/F/V e aprofundamento opcional L/P/N.
- Guias de contexto para memória, percepção, influência, mandato, identidade e ausência de conflito ativo.
- Skill portátil com método, referências, exemplos e consulta/sorteio em Python.
- Oficina local React/FastAPI com busca, edição, biblioteca e importação/exportação.
- Cinco personagens originais com quinze ensaios narrativos, além de oito aplicações anteriores.
- Documentação e verificações automatizadas do pacote público.

Os PDFs de impressão anteriores permanecem na versão 4.0 e não fazem parte desta publicação.
