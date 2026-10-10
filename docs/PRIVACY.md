# Privacidade e dados

[Projeto](../README.md) · [Operação](OPERATIONS.md)

O aplicativo armazena rascunhos, fichas salvas, seleção de módulos e preferência local de movimento no navegador. O armazenamento é separado por origem (protocolo, host, porta). Não há conta ou banco de personagens no servidor.

A oficina não envia fichas a um serviço de IA. A API pode receber textos se você chamar explicitamente composição, mas não os persiste nem lê localStorage. Exporte JSON para manter backup; fichas exportadas podem conter informações da campanha e devem ser compartilhadas por sua decisão.

Instalação baixa pacotes npm/Python. Swagger utiliza assets públicos de sua biblioteca e pode fazer requisições externas. Badges do README também são imagens externas. O banner e as capturas da aplicação estão versionados no repositório.

`.gitignore` exclui `.venv`, `node_modules`, `dist`, `.runtime`, logs, caches e `.env`. O repositório contém personagens fictícios de exemplo; não contém arquivos de sessões pessoais nem credenciais. Ao contribuir, remova dados privados de imagens, exemplos e anexos.

O servidor escuta em loopback. Nenhuma publicação da aplicação como serviço online foi feita; tornar o repositório público não torna suas fichas públicas.
