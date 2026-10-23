# Hospedagem no RunicTools

[Projeto](../README.md) · [Operação](OPERATIONS.md) · [Privacidade](PRIVACY.md)

Domínio configurado: **personcard.runictools.com**. A publicação pública exige registro DNS com proxy Cloudflare ativo, certificado de origem válido e o serviço saudável. Um container saudável sozinho não confirma que o endereço público já está disponível.

## Perfil do serviço

- `Dockerfile`: build React/Vite em Node 22; runtime Python 3.12 com FastAPI/Uvicorn.
- `docker-compose.prod.yml`: serviço `personcard` na rede externa `web`, descoberto pelo nginx-proxy por `VIRTUAL_HOST`; certificado existente `runictools.com`.
- Porta 8000 somente na rede Docker, sem portas de host ou volumes. Usuário 10001, filesystem somente leitura, capabilities removidas e `no-new-privileges`.
- Limites: 256 MB, 0,5 CPU e 128 processos; logs rotacionados. Healthcheck em `/api/health`.
- Sem contas ou dados de personagens no servidor. O deck e as artes são estáticos; rascunhos e salvos pertencem a cada navegador/origem.

O contexto Docker permite apenas os arquivos necessários ao app e o manifesto de ilustrações. PDFs, documentação, credenciais e dependências locais ficam fora da imagem. O build preserva o caminho relativo entre `app/src` e `deck/illustration_sheets_5_1.json`.

## Implantar em infraestrutura já preparada

Pré-requisitos do host: Docker/Compose, rede `web`, nginx-proxy atendendo 80/443 e certificado wildcard de origem instalado no proxy com o nome `runictools.com`. Configure no DNS um registro `A` chamado `personcard` apontando ao IP do servidor, com proxy Cloudflare ativo e SSL/TLS Full (strict). Não é preciso modificar os outros serviços.

No checkout da revisão aprovada:

```sh
docker compose -p personcard -f docker-compose.prod.yml config -q
docker build -t persona-cards:release-REVISAO .
PERSONA_IMAGE=persona-cards:release-REVISAO docker compose -p personcard -f docker-compose.prod.yml up -d --no-build --wait
```

Use um identificador de revisão real em lugar de `REVISAO`. Antes de atualizar, registre a imagem anterior e preserve a configuração vigente. Para reverter, execute o mesmo comando `up` com a imagem anterior; nenhuma ficha de usuário precisa de migração no servidor.

## Conferir

1. `/api/health`: HTTP 200, versão 5.1 e 141 cartas.
2. Página, JavaScript, CSS e ilustrações pelo domínio público, sem aviso de certificado nem tela de login.
3. Mesa/Grade, escolha D/F/V, salvamento e recarga em desktop e 390 px.
4. Exportação/importação de uma combinação de teste e movimento reduzido.
5. Serviços anteriores continuam saudáveis; nenhuma porta direta ou volume novo de personagens.

Logs do servidor e do proxy são operacionais; não equivalem a armazenamento de fichas. Consulte a política de [privacidade](PRIVACY.md). As fichas do endereço local não aparecem automaticamente no domínio público: exporte e importe para transferir.
