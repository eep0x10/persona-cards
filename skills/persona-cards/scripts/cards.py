"""Consulta e sorteio do deck oficial, somente biblioteca padrão."""
import argparse
import json
from pathlib import Path
import random
import unicodedata

def fold(value):
    return ''.join(c for c in unicodedata.normalize('NFD', value.casefold()) if not unicodedata.combining(c))

def main():
    cards = json.loads((Path(__file__).resolve().parent.parent / 'references' / 'deck.json').read_text(encoding='utf-8-sig'))['cartas']
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('get').add_argument('codes', nargs='+')
    commands.add_parser('search').add_argument('query')
    draw = commands.add_parser('draw')
    draw.add_argument('--families', nargs='+', default=['D', 'F', 'V'])
    draw.add_argument('--modules', nargs='+', default=['nucleo', 'expansao', 'expansao_5'])
    draw.add_argument('--seed', type=int)
    args = parser.parse_args()
    if args.command == 'get':
        lookup = {c['codigo']: c for c in cards}
        unknown = set(args.codes) - lookup.keys()
        if unknown:
            parser.error('Códigos desconhecidos: ' + ', '.join(sorted(unknown)))
        result = [lookup[code] for code in args.codes]
    elif args.command == 'search':
        result = [c for c in cards if fold(args.query) in fold(json.dumps(c, ensure_ascii=False))]
    else:
        if len(set(args.families)) != len(args.families) or set(args.families) - set('DFNLVP'):
            parser.error('Use famílias distintas D/F/N/L/V/P. U/G são consulta.')
        if set(args.modules) - {'nucleo', 'expansao', 'expansao_5'}:
            parser.error('Módulos válidos: nucleo, expansao, expansao_5.')
        rng = random.Random(args.seed)
        result = []
        for family in args.families:
            pool = [c for c in cards if c['familia'] == family and c['modulo'] in args.modules]
            if not pool:
                parser.error('Nenhuma carta disponível para ' + family)
            result.append(rng.choice(pool))
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
