from pathlib import Path
import json,random,hashlib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
m=json.loads((HERE/'draw.json').read_text(encoding='utf-8'))
source=(HERE.parent/'deck-5.2.1.json').read_bytes()
assert hashlib.sha256(source).hexdigest()==m['deckSha256'], 'Deck revision differs'
cards=json.loads(source)['cartas'];rng=random.Random(m['seed'])
for row in m['characters']:
    for family,card in zip(['OR','CV','D','F','V','L','P','N'],row['cards']):
        assert rng.choice([c for c in cards if c['familia']==family])==card
    assert rng.randrange(1,7)==row['callRoll']
    assert rng.randrange(1,7)==row['responseRoll']
print('REPLAY_OK:80cards+20d6;zero rerolls;deck hash confirmed')
