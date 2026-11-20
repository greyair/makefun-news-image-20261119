"""Entry point for the make.fun sandbox.

Copies the pre-rendered front page (entry.png, built by build_image.py)
into the output directory the harness provides. No network, no clock,
no randomness: the same bytes come out on every run.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_dir() -> Path:
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def copy_entry() -> Path:
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    return dest


def main() -> None:
    written = copy_entry()
    print(f"entry.png -> {written} ({written.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
