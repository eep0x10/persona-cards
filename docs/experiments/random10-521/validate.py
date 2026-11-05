"""Structural integrity only; this does not judge narrative depth."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / 'draw.json').read_text(encoding='utf-8'))
characters = []
for name in ['first5-characters.json', 'last5-characters.json']:
    rows = json.loads((HERE / name).read_text(encoding='utf-8-sig'))
    assert isinstance(rows, list), name
    characters.extend(rows)
assert len(characters) == len({c['id'] for c in characters}) == 10
for current, original in zip(sorted(characters, key=lambda c: c['id']), manifest['characters']):
    assert current['id'] == original['id']
    assert current['role'] == original['role']
    assert len(current['cards']) == 8
    for authored, drawn in zip(current['cards'], original['cards']):
        assert authored['family'] == drawn['familia']
        assert authored['code'] == drawn['codigo']
        assert authored['title'] == drawn['titulo']
        assert authored['interpretation'].strip()
    assert set(current['journey']) == {'call', 'response', 'fact', 'belief', 'choice'}
    assert current['journey']['call'] == original['callResult']
    assert current['journey']['response'] == original['responseResult']
    assert all(v.strip() for v in current['journey'].values())
    assert all(current[k].strip() for k in ['name', 'occupation', 'summary', 'bridgeORCV', 'competence', 'pleasure', 'limit'])
    assert all(current['scene'][k].strip() for k in ['attempt', 'refusal', 'consequence'])
    assert current['friction']['status'] in ['claro', 'fragil', 'forcado']
(HERE / 'characters.json').write_text(json.dumps(sorted(characters, key=lambda c: c['id']), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print('STRUCTURE_OK: 10 original characters, 80 unchanged codes/titles, 50 journey fields; narrative judgment remains separate.')
