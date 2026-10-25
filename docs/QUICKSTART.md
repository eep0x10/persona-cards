# Início rápido — Persona Cards 5.2

[Projeto](../README.md) · [Manual](../deck/manual-5.2.md) · [Skill](SKILL.md)

## Jogar sem instalar

Use o [PDF](../skills/persona-cards/print/README.md) ou a [mesa online](https://personcard.runictools.com/). Separe e escolha/sorteie **OR + CV + D + F + V + L + P + N**. Todas as oito famílias são obrigatórias. Consulte **G07** para chamado, resposta, fato, crença e escolha.

Conecte antecedente e convicção; dê objetivo, tentativa, expressão e outra vontade à cena. P muda a circunstância. N exige dois valores genuínos; se só descreve um obstáculo, troque ou ressorteie N, sem omiti-la ou impor culpa/redenção. Outros participantes podem recusar.

## Windows

Instale Git, Python 3.12+ e Node.js 22 com npm, disponíveis no terminal:

```powershell
git clone https://github.com/eep0x10/persona-cards.git
cd persona-cards/app
./iniciar.ps1
```

Abra **http://127.0.0.1:8766**. O servidor inicia em segundo plano. Se a política bloquear o script, inicie manualmente, sem alterar a política:

```powershell
python -m venv .venv
./.venv/Scripts/python.exe -m pip install -r requirements.lock.txt
npm.cmd ci
npm.cmd run build
./.venv/Scripts/python.exe -m uvicorn server:app --host 127.0.0.1 --port 8766
```

## Linux e macOS

Com Git, Python 3.12+ e Node.js 22 instalados:

```sh
git clone https://github.com/eep0x10/persona-cards.git
cd persona-cards/app
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
npm ci
npm run build
.venv/bin/python -m uvicorn server:app --host 127.0.0.1 --port 8766
```

No início manual, mantenha o terminal aberto; Ctrl+C encerra o servidor. O launcher reutiliza uma interface já construída. Após atualizar fontes, execute `npm ci` e `npm run build` novamente, reinicie seu processo e recarregue uma vez para carregar o novo build. Ações normais não exigem F5.

## Primeira ficha

Na mesa, explore as oito famílias por setas, gesto ou Mesa/Grade. Vire para consultar; use **Escolher esta carta** para selecionar explicitamente. U/G ficam separados em consulta; G07 acompanha toda criação.

**Salvar personagem** abre a revisão. Preencha nome, oito interpretações e os cinco registros da jornada. Foto, papel, contexto e notas são opcionais. Finalize para guardar a carta; use JSON para backup completo, além de PNG/Markdown para leitura.

Fichas antigas preservam o que já existe e abrem como rascunho pendente quando faltam camadas; não recebem passado ou conflito inventado. As 100 inspirações já incluem oito cartas e G07 na edição 5.2, com justificativas e cenas autorais. Usar uma base copia esses campos para uma revisão editável. Adapte a proposta à sua história antes de salvar; o catálogo permanece intacto.

Porta ocupada: use `./iniciar.ps1 -Port 8767` ou altere `--port` no início manual. Cada porta/navegador/origem tem armazenamento separado; exporte antes de trocar. Veja [operação e backup](OPERATIONS.md).
