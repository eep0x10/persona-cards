"""Documentation integrity checks; no network or additional dependencies."""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]

def anchors(source):
    found = set()
    counts = {}
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*$', source, re.MULTILINE):
        slug = re.sub(r'[^\w\s-]', '', heading.lower()).replace(' ', '-')
        count = counts.get(slug, 0)
        found.add(slug if not count else f'{slug}-{count}')
        counts[slug] = count + 1
    return found

class Documentation(unittest.TestCase):
    def test_local_links_and_assets(self):
        folders = ['docs', 'deck', 'examples', 'skills']
        files = list(ROOT.glob('*.md')) + [ROOT/'app/README.md']
        for folder in folders:
            files += list((ROOT/folder).rglob('*.md'))
        for path in files:
            source = path.read_text(encoding='utf-8-sig')
            targets = re.findall(r'\]\(([^\s)]+)(?:\s+[^)]*)?\)', source)
            targets += re.findall(r'(?:src|href)="([^"]+)"', source)
            for target in targets:
                if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                    continue
                relative, _, anchor = unquote(target).partition('#')
                linked = (path.parent/relative).resolve() if relative else path
                with self.subTest(document=str(path.relative_to(ROOT)), target=target):
                    self.assertTrue(linked.is_relative_to(ROOT), 'Reference escapes the repository')
                    self.assertTrue(linked.exists(), 'Missing local reference')
                    if anchor and linked.suffix == '.md':
                        self.assertIn(anchor, anchors(linked.read_text(encoding='utf-8-sig')))

    def test_readme_presentation_contract(self):
        for name in ['README.md', 'README.en.md']:
            source = (ROOT/name).read_text(encoding='utf-8')
            with self.subTest(readme=name):
                self.assertIn('docs/assets/banner.png', source)
                self.assertIn('actions/workflows/checks.yml/badge.svg', source)
                self.assertIn('docs/QUICKSTART.md', source)
                self.assertIn('docs/PRIVACY.md', source)
                self.assertIn('docs/ARCHITECTURE.md', source)
                self.assertIn('git clone https://github.com/eep0x10/persona-cards.git', source)
        self.assertTrue((ROOT/'docs/assets/banner.png').is_file())

if __name__ == '__main__':
    unittest.main()
