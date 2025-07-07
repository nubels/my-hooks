from pathlib import Path
import os
import re
import sys


SNAKE_CASE = r"[a-z][a-z0-9]*(_[a-z0-9]+)*"
snake_pattern = re.compile(f"^{SNAKE_CASE}$")

def main() -> int:
    root = os.getcwd()
    bad = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        filenames = [f for f in filenames if not f.startswith('.')]
        parts = Path(dirpath).parts

        if 'addons' in parts:
            continue
    
        for name in dirnames + filenames:
            rel = os.path.relpath(os.path.join(dirpath, name), root)
            p = Path(name)
            suffixes = "".join(p.suffixes)
            stem = p.name[:-len(suffixes)] if suffixes else p.name
            if not snake_pattern.fullmatch(stem):
                bad.append(rel)
    if bad:
        for rel in sorted(bad):
            print(f"  - {rel} is not snake_case.")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
