# Ensaios preservados — revisão 5.2.1

[Projeto](../../README.md) · [Continuidade](../CONTINUITY.md)

Estes exercícios autorais foram preservados antes de mudar de computador. Não são playtests com jogadores nem provas de eficácia narrativa universal.

| Exercício | Leitura | Sorteio reproduzível |
| --- | --- | --- |
| Dez personagens, sorteio livre | [Relatório](random10-521/ENSAIO-10-PERSONAGENS.md) | `python docs/experiments/random10-521/replay.py` |
| Dez personagens, F21/F22/N23 fixadas | [Relatório](targeted10-521/ENSAIO-NOVAS-CARTAS.md) | `python docs/experiments/targeted10-521/replay.py` |

Cada pasta contém protocolo, sorteio, primeiras versões, relatório e crítica. `frozen-hashes.json` mantém os hashes originais. Os resultados narrativos não foram reescritos após a crítica. Apenas os caminhos de `replay.py` foram adaptados para usar a [fonte histórica](deck-5.2.1.json), extraída do commit `727779e34b95ee72c475081e67196ce7faf8047b`, SHA256 `4dae5bb05ba6376bd09ac3d7bcf16a6307e159a236b66f1bef457fce4b897128`.

Essa fonte não é uma quarta cópia ativa: mantém G07 anterior à revisão 5.2.2 e serve exclusivamente à reprodução histórica. Não a use para construir a aplicação atual. A ambiguidade do último personagem do ensaio direcionado motivou a [revisão de G07](../REVISAO-G07-5.2.2.md).

`validate.py` recompõe `characters.json`; `build_report.py` recompõe o relatório. Ambos escrevem arquivos: faça primeiro uma cópia e confira os hashes antes/depois. `replay.py` é somente leitura. Sementes excedem o inteiro seguro de JavaScript; preserve-as como inteiros Python ou strings ao transportar para JS.

Os protótipos visuais anteriores estão em `deck/previews/`, `deck/prototype_art_cards.py` e `skills/persona-cards/print/assets/family-engravings.png`; são históricos, não as artes atuais. Logs, ambientes, snapshots de produção e métricas privadas continuam fora do Git.
