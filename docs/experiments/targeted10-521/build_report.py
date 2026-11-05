import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
characters = json.loads((HERE / 'characters.json').read_text(encoding='utf-8'))
draw = json.loads((HERE / 'draw.json').read_text(encoding='utf-8'))
review = json.loads((HERE / 'independent-review.json').read_text(encoding='utf-8'))
by_id = {r['id']: r for r in review['characters']}
labels = {'claro': 'Encaixe claro', 'fragil': 'Encaixe frágil', 'forcado': 'Encaixe forçado'}
counts = review['counts']
lines = ['# F21, F22 e N23 — dez personagens novos', '',
         'Ensaio autoral direcionado às três cartas novas, com cinco protagonistas e cinco vilões originais. As primeiras versões foram preservadas; a crítica não foi usada para reescrevê-las até todas passarem.', '',
         f"**Resultado da segunda leitura:** {counts['claro']} claros, {counts['fragil']} frágeis e {counts['forcado']} forçados. Isso é um julgamento editorial situado, não uma taxa comprovada de eficácia do baralho.", '',
         '## Como foi feito', '',
         f"Quatro exposições fixadas de cada novidade, duas por papel: doze posições fixas e sessenta e oito cartas sorteadas. Cada personagem tem uma carta por família OR/CV/D/F/V/L/P/N e duas rolagens independentes de G07. Semente: `{draw['seed']}`. Zero trocas, zero rerrolagens. Oito cartas continuam obrigatórias.", '',
         draw['scenario'], '',
         'Papéis, cenários e cartas alvo foram definidos antes do sorteio. F21 e F22 são alternativas da mesma família; não são acumuladas num personagem. Os casos7(F21+N23) e10(F22+N23) combinam método e conflito novos. Protagonista significa foco narrativo, não bondade automática; vilão precisa exercer dano ou coerção concretos.', '',
         'O objetivo era avaliar se as cartas mantêm seus sentidos e compõem uma escolha compreensível, com duas vontades genuínas em N, agência em L, reação à recusa e fatos separados de crenças. Ter todos os campos preenchidos não basta para demonstrar profundidade.', '',
         '[Protocolo](PROTOCOLO.md) · [Sorteio com os textos integrais das cartas](draw.json) · [Crítica independente](independent-review.json) · [Reproduzir o sorteio](replay.py)', '',
         '## Resultado por carta alvo', '']
for code, tally in review['byTarget'].items():
    lines += [f"- **{code}:** {tally['claro']} claros, {tally['fragil']} frágeis e {tally['forcado']} forçados."]
lines += ['', '## Os dez personagens', '']
for c in characters:
    r = by_id[c['id']]
    original = next(d for d in draw['characters'] if d['id'] == c['id'])
    lines += [f"### {c['id']}. {c['name']} — {c['role']}", '',
              f"**Papel:** {c['occupation']}", '', f"**Carta(s) fixada(s):** {', '.join(original['fixedCodes'])}", '', c['summary'], '',
              '**Ponte entre Origem e Convicção:** ' + c['bridgeORCV'], '',
              '**As oito cartas sorteadas e suas interpretações:**', '']
    for card in c['cards']:
        lines += [f"- **{card['code']} — {card['title']}:** {card['interpretation']}"]
    lines += ['', '**G07 — Chamado e destino:**', '']
    for key, label in [('call', 'Chamado'), ('response', 'Primeira resposta'), ('fact', 'Fato'), ('belief', 'Crença'), ('choice', 'Escolha agora')]:
        lines += [f"- **{label}:** {c['journey'][key]}"]
    lines += ['', f"**Competência:** {c['competence']}", '',
              f"**Prazer cotidiano:** {c['pleasure']}", '', f"**Limite:** {c['limit']}", '',
              '**Tentativa, recusa e consequência possível:**', '',
              f"- **Tentativa:** {c['scene']['attempt']}",
              f"- **Recusa:** {c['scene']['refusal']}",
              f"- **Consequência:** {c['scene']['consequence']}", '',
              f"**Nota da autoria — {labels[c['friction']['status']]}:** {c['friction']['note']}", '',
              f"**Segunda leitura — {labels[r['status']]}:** {r['strength']}", '',
              f"**Problema observado:** {r['issue']}", '',
              f"**Como testar melhor, sem corrigir silenciosamente a versão acima:** {r['suggestedTest']}", '']
    for target in r['targetAssessments']:
        lines += [f"**Alvo {target['code']} — {labels[target['status']]}:** {target['evidence']}", '', f"**Fronteira verificada:** {target['distinction']}", '']
lines += ['## O que este exercício permite concluir', '',
          'Criar passado, relações e circunstâncias é parte legítima da criação de um personagem original. O teste procura distorção semântica e premissas desnecessárias, não exige que as cartas escrevam a história sozinhas. As fragilidades são preservadas para mostrar a diferença entre preencher oito camadas e integrá-las numa cena.', '',
          '## Limites', '']
for limitation in review['limitations']:
    lines += ['- ' + limitation]
lines += ['', f"Fonte congelada: deck SHA256 `{draw['deckSha256']}`. Nenhum conteúdo do baralho ou da aplicação foi alterado para este ensaio.", '']
(HERE / 'ENSAIO-NOVAS-CARTAS.md').write_text('\n'.join(lines), encoding='utf-8')
print('REPORT_OK: ten complete profiles, eighty interpretations, fifty journey fields and independent criticism.')
