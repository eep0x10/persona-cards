"""Build the active deck, references and illustrated PDFs, then verify them."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STEPS = (
    "build_5_1.py",
    "build_5_1_docs.py",
    "render_print_illustrated_5_1.py",
    "verify_illustrated_print_5_1.py",
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        epilog=("Requires ReportLab, pypdf, Pillow, Windows Georgia/Arial fonts "
                "in C:/Windows/Fonts, and the existing illustration assets. "
                "Uses the current Python interpreter; stops on the first failed step. "
                "Regenerates the three active JSON copies, references and four 5.1 PDFs; "
                "preserves the frozen 5.0 deck and PDFs."),
    )
    parser.parse_args()
    for script in STEPS:
        print(f"==> {script}", flush=True)
        subprocess.run(
            [sys.executable, "-X", "utf8", str(ROOT / "deck" / script)],
            cwd=ROOT, check=True,
        )


if __name__ == "__main__":
    main()
