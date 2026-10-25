# Operação

[Projeto](../README.md) · [Início rápido](QUICKSTART.md) · [Privacidade](PRIVACY.md)

## Processo e configuração

O servidor usa FastAPI/Uvicorn em loopback. `iniciar.ps1` recebe `-Port` (padrão 8766), cria `.venv` se ausente, instala dependências, constrói a interface se `dist/index.html` estiver ausente e reutiliza um servidor saudável. Não há configuração de contas ou chaves de IA.

No Windows, logs e PID ficam em `app/.runtime/`. Antes de encerrar um processo, confira se o PID ainda pertence ao servidor Persona Cards daquele checkout: PIDs podem ser reutilizados. O início manual mantém o processo no terminal e pode ser encerrado com Ctrl+C.

## Atualizar

Preserve alterações locais e exporte fichas. Atualize o checkout normalmente, reinstale dependências quando os arquivos de versão mudarem e reconstrua a interface:

```sh
git pull --ff-only
python -m pip install -r app/requirements.lock.txt
npm --prefix app ci
npm --prefix app run build
```

Use o Python do ambiente virtual. Reinicie o servidor se o backend ou deck mudou; recarregue o navegador após um novo build. Não é necessário recarregar para ações normais de edição, filtros ou salvamento.

## Backup e transferência

Exporte cada ficha em JSON. Markdown/texto serve para leitura, mas a importação espera o formato JSON do aplicativo. Importar cria um novo personagem e preserva o rascunho. Limpar dados do navegador pode apagar fichas; mudar protocolo, host ou porta cria outro armazenamento.

Na atualização para 5.2, conserve cópias das fichas 5.0/5.1 antes de completar as novas etapas. Elas abrem como rascunhos pendentes de oito famílias e G07, sem passado, convicção ou conflito inventado automaticamente. Os registros da jornada, foto e interpretações integram o JSON. A galeria de 100 inspirações permanece histórica e parcial no novo método.

## Diagnóstico

- `/api/health` confirma estado, versão 5.2 e 166 cartas; a revisão 5.2.0 aparece em `/api/deck`.
- Interface em preparação: execute `npm run build` em `app/`.
- Porta ocupada: escolha outra e use o endereço correspondente.
- Importação recusada: confira formato, versão, códigos e limites; não edite a estrutura apenas para contornar a validação.
- Falha de salvamento local: mantenha a sessão e exporte uma cópia.

## Hospedagem

O perfil [Docker/RunicTools](DEPLOY.md) publica a mesa atrás de nginx-proxy e HTTPS. Ele não usa volumes, contas, banco de personagens ou sincronização: combinações continuam no navegador de cada pessoa. O início local acima permanece disponível.
