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

## Diagnóstico

- `/api/health` confirma estado, versão 5.0 e 141 cartas.
- Interface em preparação: execute `npm run build` em `app/`.
- Porta ocupada: escolha outra e use o endereço correspondente.
- Importação recusada: confira formato, versão, códigos e limites; não edite a estrutura apenas para contornar a validação.
- Falha de salvamento local: mantenha a sessão e exporte uma cópia.

Não há serviço de produção, Docker, HTTPS, autenticação ou sincronização configurados nesta entrega.
