from pathlib import Path
import json,random,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
m=json.loads((HERE/'draw.json').read_text(encoding='utf-8'));source=(HERE.parent/'deck-5.2.1.json').read_bytes()
assert hashlib.sha256(source).hexdigest()==m['deckSha256']
cards=json.loads(source)['cartas'];bycode={c['codigo']:c for c in cards};rng=random.Random(m['seed'])
fixed=drawn=0
for row in m['characters']:
    assigned={bycode[code]['familia']:bycode[code] for code in row['fixedCodes']}
    for family,card in zip(['OR','CV','D','F','V','L','P','N'],row['cards']):
        if family in assigned: expected=assigned[family];fixed+=1
        else: expected=rng.choice([c for c in cards if c['familia']==family]);drawn+=1
        assert expected==card
    assert rng.randrange(1,7)==row['callRoll'];assert rng.randrange(1,7)==row['responseRoll']
assert fixed==12 and drawn==68
print('REPLAY_OK:12fixed+68random+20d6;zero rerolls;canonical deck hash confirmed')
