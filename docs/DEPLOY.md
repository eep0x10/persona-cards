# Hospedagem no RunicTools

[Projeto](../README.md) · [Operação](OPERATIONS.md) · [Privacidade](PRIVACY.md)

Domínio configurado: **personcard.runictools.com**. A publicação pública exige registro DNS com proxy Cloudflare ativo, certificado de origem válido e o serviço saudável. Um container saudável sozinho não confirma que o endereço público já está disponível.

## Perfil do serviço

- `Dockerfile`: build React/Vite em Node 22; runtime Python 3.12 com FastAPI/Uvicorn.
- `docker-compose.prod.yml`: serviço `personcard` na rede externa `web`, descoberto pelo nginx-proxy por `VIRTUAL_HOST`; certificado existente `runictools.com`.
- Porta 8000 somente na rede Docker, sem portas de host ou volumes. Usuário 10001, filesystem somente leitura, capabilities removidas e `no-new-privileges`.
- Limites: 256 MB, 0,5 CPU e 128 processos; logs rotacionados. Healthcheck em `/api/health`.
- Sem contas ou dados de personagens no servidor. O deck e as artes são estáticos; rascunhos e salvos pertencem a cada navegador/origem.

O contexto Docker permite apenas os arquivos necessários ao app e o manifesto de ilustrações. PDFs, documentação, credenciais e dependências locais ficam fora da imagem. O build preserva o caminho relativo entre `app/src` e `deck/illustration_sheets_5_2.json`.

## Implantar em infraestrutura já preparada

Pré-requisitos do host: Docker/Compose, rede `web`, nginx-proxy atendendo 80/443 e certificado wildcard de origem instalado no proxy com o nome `runictools.com`. Configure no DNS um registro `A` chamado `personcard` apontando ao IP do servidor, com proxy Cloudflare ativo e SSL/TLS Full (strict). Não é preciso modificar os outros serviços.

No host de operação cadastrado, use o pipeline único após validar, commitar e enviar a revisão ao GitHub. Ele chama o preflight registrado de `persona-cards`, executa o contrato de release e cria um snapshot da imagem ativa antes de alterar o serviço. Falhas de contrato, upstream, checks, backup ou saúde bloqueiam a publicação. Não contorne o guard nem remova volumes.

```powershell
python ops/publish.py --expected-revision (git rev-parse HEAD)
```

O SHA deve coincidir com `origin/main`; o pipeline não faz push nem descarta mudanças. Trabalha com arquivos versionados e uma imagem imutável por revisão. O contrato exige árvore de arquivos rastreados limpa; rascunhos não rastreados ficam fora do arquivo de publicação. Uma cópia Git real em `repository` registra a fonte, enquanto `current` aponta para a release ativa. Não há volumes de personagens no servidor.

Publicações e recuperações compartilham um lock. A ativação confere novamente o upstream, o container e a saúde; se falhar, tenta recuperar o snapshot. Uma recuperação atrasada não pode reverter uma publicação posterior.

Para recuperação explícita, no servidor, use um snapshot cujo caminho foi confirmado e cujos hashes sejam válidos:

```sh
bash /home/deploy/persona-cards/ops/rollback.sh /home/deploy/persona-cards/snapshots/IDENTIFICADOR-REAL
```

O script valida o snapshot, carrega a imagem e restaura Compose, fonte Git e ponteiro da release, sem apagar containers, volumes ou fichas. A verificação pré-deploy exige snapshot recente; uma recuperação explícita pode usar um snapshot antigo íntegro. Os snapshots e arquivos de ambiente são privados e não entram no GitHub ou nos downloads.

## Conferir

1. `/api/health`: HTTP 200, versão 5.2 e 169 cartas; revisão 5.2.1 em `/api/deck`.
2. Página, JavaScript, CSS e ilustrações pelo domínio público, sem aviso de certificado nem tela de login.
3. Mesa/Grade, oito escolhas OR/CV/D/F/V/L/P/N, revisão com G07, salvamento e recarga em desktop e 390 px.
4. Exportação/importação de uma combinação de teste, rascunho legado sem passado inventado e movimento reduzido.
5. Serviços anteriores continuam saudáveis; nenhuma porta direta ou volume novo de personagens.

Logs do servidor e do proxy são operacionais; não equivalem a armazenamento de fichas. Consulte a política de [privacidade](PRIVACY.md). As fichas do endereço local não aparecem automaticamente no domínio público: exporte e importe para transferir.
