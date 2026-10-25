# Histórico

## Edição 5.2 — revisão 5.2.0

- 166 cartas: 150 de criação e 16 guias. OR/CV/D/F/V/L/P/N passam a ser obrigatórias em toda criação completa; G07 organiza chamado, resposta, fato, crença e escolha.
- Doze cartas de Origem e doze de Convicção conectam antecedente, interpretação e ação. Não impõem trauma, culpa ou redenção. N requer dois valores genuínos; se não cabe, trocar ou ressorteiar a carta, sem omitir a família.
- Mesa com oito etapas; salvar abre a revisão de oito interpretações e jornada. Foto e notas continuam livres. CLI sorteia oito famílias por padrão; API distingue composição completa de rascunho parcial.
- Fichas 5.0/5.1 mantêm seus dados e abrem como rascunhos pendentes, sem novos passados inventados. A galeria de 100 inspirações continua histórica e parcial no método 5.2.
- Fonte 5.2, três cópias JSON, gerador documental próprio, manual, referências e cinco exemplos nos READMEs acompanham a edição. Arquivos e manuais 5.0/5.1 permanecem históricos.
- PDFs 5.2 têm nomes próprios, cartas de 92 × 130 mm, quatro por A4, 42 folhas e 84 páginas duplex. O manual rápido tem três páginas. Conferências digitais, publicação e eventuais provas físicas devem ser registradas separadamente em `docs/VALIDACAO.md`; esta nota não declara release público ou teste com jogadores.

## Revisão editorial — 5.1.1

- U08 passa a distribuir também a expansão 5.0, com intervalos por família.
- D10 mantém autoridade como desejo e remove exigência de cooperação/limite moral dos convites.
- D13 inclui continuidade diante de ameaça imediata ou duradoura.
- Overlay editorial reproduzível modifica somente essas três cartas; fonte 5.0 preservada, três JSON ativos idênticos.
- Skill, referências, catálogo de inspiração, PDFs, aplicação, API e pacote de release sincronizados; formatos de fichas 5.0/5.1 compatíveis.
- Inspiração lista todas as camadas escolhidas e mostra as cartas ilustradas com353 justificativas específicas abaixo delas, nos100 exemplos.


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
