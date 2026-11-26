#!/usr/bin/env python3
"""Sum 26 R4 entrypoint (stdlib only): copy the pre-rendered entry.png
to the output directory. No third-party imports: the sandbox installs
nothing, so this file must run with the standard library alone."""
import argparse
import os
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description="Write entry.png to the output directory.")
    parser.add_argument("--output", default=None,
                        help="Output directory (overrides MAKEFUN_OUTPUT_DIR).")
    args = parser.parse_args()

    out_dir = args.output or os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
