from pathlib import Path
import os
import sys
import re


PASS = 0
FAIL = 1

pattern = re.compile(r'^\s*\[connection\b', re.IGNORECASE)


def has_signal_connection(tscn_path: str) -> bool:
    with open(tscn_path, 'r', encoding='utf-8') as f:
        for line in f:
            if pattern.match(line):
                return True
    return False


def main() -> int:
    root = os.getcwd()
    bad = []

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        filenames = [f for f in filenames if not f.startswith('.')]

        parts = dirpath.split(os.sep)
        if 'addons' in parts:
            continue

        for name in filenames:
            if not name.lower().endswith('.tscn'):
                continue
            file_path = os.path.join(dirpath, name)
            rel_path = os.path.relpath(file_path, root)
            # Prüfe, ob eine Signal-Connection vorhanden ist
            if has_signal_connection(file_path):
                bad.append(rel_path)

    if bad:
        print("Folgende .tscn-Dateien enthalten unerlaubte Signal-Connections:")
        for rel in bad:
            print(f"  - {rel}")
        return FAIL

    print("Keine .tscn-Dateien enthalten Signal-Connections. Alles in Ordnung.")
    return PASS

if __name__ == "__main__":
    sys.exit(main())
