#!/usr/bin/env python3
"""News-image entry: copy the front-page image beside this file to /output/entry.png.

Python 3.13, standard library only. Deterministic: same bytes every run, no network.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil


def copy_entry():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(base_dir, "entry.png"), os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    copy_entry()
