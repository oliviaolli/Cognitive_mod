#!/usr/bin/env python3
"""Git clean filter: strip notebook outputs on the way into git.

The file in the working tree keeps its outputs, so plots stay visible in
Jupyter/VS Code; only what gets committed and pushed is stripped. Enable with:

    git config filter.nbstripout.clean "python3 tools/nbstripout.py"
    git config filter.nbstripout.smudge cat
"""
import json
import sys


def main():
    raw = sys.stdin.read()
    try:
        nb = json.loads(raw)
    except ValueError:
        sys.stdout.write(raw)  # not a notebook; pass through untouched
        return

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None
        cell.get("metadata", {}).pop("execution", None)
    nb.get("metadata", {}).pop("widgets", None)

    json.dump(nb, sys.stdout, indent=1, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
