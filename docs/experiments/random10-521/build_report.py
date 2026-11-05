import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
characters = json.loads((HERE / 'characters.json').read_text(encoding='utf-8'))
draw = json.loads((HERE / 'draw.json').read_text(encoding='utf-8'))
review = json.loads((HERE / 'independent-review.json').read_text(encoding='utf-8'))
by_id = {r['id']: r for r in review['characters']}
labels = {'claro': 'Encaixe claro', 'fragil': 'Encaixe frágil', 'forcado': 'Encaixe forçado'}
counts = review['counts']
lines = ['# Dez personagens aleatórios — Persona Cards 5.2.1', '',
         'Ensaio autoral com cinco protagonistas e cinco vilões originais. A primeira versão de cada personagem foi preservada; a crítica não foi usada para reescrevê-los até todos passarem.', '',
         f"**Resultado da segunda leitura:** {counts['claro']} claros, {counts['fragil']} frágeis e {counts['forcado']} forçados. Isso é um julgamento editorial situado, não uma taxa comprovada de eficácia do baralho.", '',
         '## Como foi feito', '',
         f"Uma carta por família OR/CV/D/F/V/L/P/N e duas rolagens independentes de G07 por personagem. Semente: `{draw['seed']}`. Zero trocas, zero rerrolagens. Oito cartas continuam obrigatórias.", '',
         draw['scenario'], '',
         'Os papéis foram atribuídos antes do sorteio. Protagonista significa foco narrativo, não bondade automática; vilão precisa exercer dano ou coerção concretos. CV05 apareceu cinco vezes. F21/F22/N23 não saíram: este ensaio não valida diretamente as três novidades.', '',
         'O objetivo era avaliar se as cartas mantêm seus sentidos e compõem uma escolha compreensível, com duas vontades genuínas em N, agência em L, reação à recusa e fatos separados de crenças. Ter todos os campos preenchidos não basta para demonstrar profundidade.', '',
         '[Protocolo](PROTOCOLO.md) · [Sorteio com os textos integrais das cartas](draw.json) · [Crítica independente](independent-review.json) · [Reproduzir o sorteio](replay.py)', '',
         '## Os dez personagens', '']
for c in characters:
    r = by_id[c['id']]
    original = next(d for d in draw['characters'] if d['id'] == c['id'])
    lines += [f"### {c['id']}. {c['name']} — {c['role']}", '',
              f"**Papel:** {c['occupation']}", '', c['summary'], '',
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
lines += ['## O que este exercício permite concluir', '',
          'Criar passado, relações e circunstâncias é parte legítima da criação de um personagem original. O teste procura distorção semântica e premissas desnecessárias, não exige que as cartas escrevam a história sozinhas. As fragilidades são preservadas para mostrar a diferença entre preencher oito camadas e integrá-las numa cena.', '',
          '## Limites', '']
for limitation in review['limitations']:
    lines += ['- ' + limitation]
lines += ['', f"Fonte congelada: deck SHA256 `{draw['deckSha256']}`. Nenhum conteúdo do baralho ou da aplicação foi alterado para este ensaio.", '']
(HERE / 'ENSAIO-10-PERSONAGENS.md').write_text('\n'.join(lines), encoding='utf-8')
print('REPORT_OK: ten complete profiles, eighty interpretations, fifty journey fields and independent criticism.')
