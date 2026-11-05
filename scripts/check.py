"""Run repository checks with the current Python and npm from PATH, without deploy."""
from pathlib import Path
import argparse
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pdf', action='store_true', help='also verify published PDFs (install deck/requirements-print.lock.txt)')
    args = parser.parse_args()
    node = shutil.which('node')
    npm = shutil.which('npm.cmd' if sys.platform == 'win32' else 'npm')
    if not node or not npm:
        parser.error('Node.js 22 and npm must be available on PATH')
    commands = [
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'tests'],
        [sys.executable, '-m', 'unittest', 'discover', '-s', 'app', '-p', 'test_api.py'],
        [node, '--test', 'app/model.test.mjs', 'app/inspirations.test.mjs'],
        [npm, '--prefix', 'app', 'run', 'build'],
    ]
    if args.pdf:
        commands.append([sys.executable, 'deck/verify_illustrated_print_5_2.py'])
    for command in commands:
        print('CHECK:', ' '.join(command[1:]), flush=True)
        subprocess.run(command, cwd=ROOT, check=True)
    print('CHECK_OK (no deployment; visual checks remain separate)')

if __name__ == '__main__':
    main()
