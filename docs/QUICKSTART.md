# Início rápido

Persona Cards oferece três entradas: ler o deck, usar a skill ou abrir a oficina. [Voltar ao projeto](../README.md).

## Sem instalar o aplicativo

Leia o [manual 5.1](../deck/manual-5.1.md), escolha D/F/V e leia a abertura de cada carta. Complete objetivo, método e expressão com detalhes do cenário. Vínculo e pressão são opcionais; N exige dois valores em disputa. Consulte [a skill](SKILL.md) para uso com assistentes.

## Oficina no Windows

Instale Git, Python 3.12+ e Node 22 LTS com npm. Python e npm devem estar disponíveis no terminal.

```powershell
git clone https://github.com/eep0x10/persona-cards.git
cd persona-cards/app
./iniciar.ps1
```

Abra http://127.0.0.1:8766. Primeira instalação baixa dependências; o servidor é iniciado em segundo plano. Se a política local impedir o script, use início manual sem alterar a política:

```powershell
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.lock.txt
npm.cmd ci
npm.cmd run build
./.venv/Scripts/python.exe -m uvicorn server:app --host 127.0.0.1 --port 8766
```

## Linux/macOS

```sh
git clone https://github.com/eep0x10/persona-cards.git
cd persona-cards/app
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
npm ci
npm run build
.venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8766
```

O processo manual precisa continuar ligado. Ctrl+C encerra o servidor.

## Primeira ficha

Pesquise uma carta em **O baralho**, abra detalhes e use **Usar carta no personagem**. Preencha nome, papel e contexto. Sorteie as outras camadas e marque **Manter** nas que deseja preservar. Substitua espaços entre colchetes por situações concretas. Salve e exporte JSON; a ficha fica no navegador atual.

Porta ocupada: no Windows, `./iniciar.ps1 -Port 8767`; no início manual, substitua `--port 8766` por `--port 8767`. Use o novo endereço no navegador. Armazenamento de fichas muda com a porta: exporte antes de trocar. [Operação](OPERATIONS.md).
