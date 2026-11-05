# Auditoria de continuidade — 5 de novembro de 2026

[Guia de transferência](CONTINUITY.md) · [Projeto](../README.md)

Base auditada: commit `3bf394beb77649ea31a38cabf76a5b378165f622`, release 5.2.5, baralho 5.2 / revisão editorial 5.2.2. Esta entrega documental é 5.2.6; não altera textos das cartas, catálogo de 105 inspirações, artes ativas ou os quatro PDFs distribuídos.

## Resultado e correções

- O remoto oficial e o HEAD inicial coincidiam. O pacote 5.2.5 continha todos os arquivos então versionados, com hash igual ao digest publicado, mas não incluía os dois ensaios locais nem os protótipos.
- Os ensaios agora estão em [experiments](experiments/README.md), com primeiras versões e hashes preservados. A fonte histórica exata acompanha os replays; ambos foram reproduzidos sem rerrolagem. Métricas privadas e logs ficaram fora da publicação.
- Protótipos visuais foram incluídos e identificados como históricos. Código, arte fonte, manifestos, skill, documentação e PDFs atuais são versionados. Dependências instaladas, builds, runtime e snapshots são recriados ou transferidos por procedimento próprio.
- Foram acrescentados AGENTS.md ampliado, guia autocontido, dependências fixadas de impressão e comando de checks usando o Python atual e Node/npm do PATH. O diretório de fontes pode ser configurado; ausência falha explicitamente, sem mudar tipografia.
- Uma cópia limpa revelou hash incompatível no manifesto de arte por CRLF/LF. O manifesto agora preserva seus bytes publicados pelo Git; o recibo foi corrigido e um teste independente de ferramentas PDF confere manifesto, deck e quatro arquivos PDF em cada CI.

## Provas executadas

Em Windows, foi criado clone independente sem hardlinks e ambiente virtual novo, com Python 3.14 e Node/npm do host. Instalação dos dois locks Python e `npm ci` concluída; `pip check` não encontrou incompatibilidades. Testes da API (11), modelo/galeria (15), testes do repositório e build Vite foram executados. Após a correção, a suíte do repositório tem 17 testes.

O servidor foi iniciado nesse clone em porta isolada: serviu o build de produção e `/api/health`/`/api/deck` retornaram 169 cartas, estado saudável e revisão 5.2.2. O processo de teste foi encerrado. Fichas pessoais não foram importadas ou alteradas.

Os quatro PDFs ativos foram inicialmente convertidos com MarkItDown; a extração pode misturar colunas. O verificador completo passou: 169 textos/artes, 30 folhas de arte, páginas A4 43/43/86/3, hashes e limites tipográficos. A configuração padrão das fontes e a falha por diretório sem fontes foram conferidas. Não houve regeneração visual nem teste físico de impressão nesta auditoria.

## Limites da garantia

Não foi executada instalação em outro computador físico, Linux ou macOS nesta estação. A CI Linux fornece evidência separada identificada no GitHub Actions. O aviso Vite de bundle acima de 500 kB permanece; não impede o build. Sem alteração de UI, esta auditoria não repete a validação visual de todos os fluxos.

Fichas/fotos no navegador, segredos, credenciais de produção e arquivos temporários privados não viajam pelo Git. Exporte cada personagem em JSON. Acesso operacional precisa de configuração equivalente no novo host; não se deve publicar contornando o preflight. Direitos de redistribuição continuam sem licença definida. Nenhum arquivo de instruções garante que toda IA obedecerá: o responsável deve conferir diffs e evidências antes de integrar mudanças.
