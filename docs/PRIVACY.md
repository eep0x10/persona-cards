# Privacidade e dados

[Projeto](../README.md) · [Operação](OPERATIONS.md)

O aplicativo armazena rascunhos, fichas salvas, seleção de módulos e preferência local de movimento no navegador. O armazenamento é separado por origem (protocolo, host, porta). Não há conta ou banco de personagens no servidor.

A foto opcional é processada localmente, reduzida e guardada com a ficha. Ela não é enviada ao servidor. Exportações JSON incluem o retrato; o PNG contém a carta visual. Compartilhe esses arquivos apenas quando quiser compartilhar também a imagem. Muitas fotos podem atingir a cota do navegador; mantenha cópias exportadas.

A mesa não envia fichas a um serviço de IA. A API pode receber textos se você chamar explicitamente composição, mas não os persiste nem lê localStorage. Exporte JSON para manter backup; fichas exportadas podem conter informações da campanha e devem ser compartilhadas por sua decisão.

Instalação baixa pacotes npm/Python. Swagger utiliza assets públicos de sua biblioteca e pode fazer requisições externas. Badges do README também são imagens externas. O banner e as capturas da aplicação estão versionados no repositório.

`.gitignore` exclui `.venv`, `node_modules`, `dist`, `.runtime`, logs, caches e `.env`. O repositório contém personagens fictícios de exemplo; não contém arquivos de sessões pessoais nem credenciais. Ao contribuir, remova dados privados de imagens, exemplos e anexos.

O início local escuta em loopback. O perfil de hospedagem do RunicTools serve a mesma aplicação por HTTPS, sem contas e sem banco de personagens. O servidor, o proxy e a Cloudflare processam as solicitações necessárias para entregar páginas e arquivos; logs operacionais podem registrar IP, endereço solicitado e horário. Publicar a aplicação não publica as fichas guardadas no navegador. Os dados do endereço local e do domínio online são separados: use exportação/importação para transferi-los.
