"""Build the active 5.2 deck, references and illustrated PDFs; stop on failure."""
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    for name in ['build_5_2.py','build_5_2_docs.py','render_print_illustrated_5_2.py','verify_illustrated_print_5_2.py']:
        print('==>',name,flush=True)
        subprocess.run([sys.executable,'-X','utf8',str(ROOT/'deck'/name)],cwd=ROOT,check=True)
