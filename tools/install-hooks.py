"""Install the versioned hooks into this checkout.

Hooks under `hooks/` are versioned and reviewable. Hooks under `.git/hooks`
are what git actually runs and are not versioned, so they must be installed
in every checkout. This script copies one to the other and reports what it
did, so that a checkout with no gates installed is a visible state rather
than a silent one.

Usage:
    python tools/install-hooks.py            install
    python tools/install-hooks.py --status   report without installing
"""

import filecmp
import shutil
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "hooks"
TARGET = ROOT / ".git" / "hooks"
NAMES = ["pre-commit", "commit-msg"]


def status():
    ok = True
    for name in NAMES:
        src, dst = SOURCE / name, TARGET / name
        if not dst.exists():
            print(f"{name}: NOT INSTALLED")
            ok = False
        elif not filecmp.cmp(src, dst, shallow=False):
            print(f"{name}: INSTALLED BUT STALE, differs from hooks/{name}")
            ok = False
        else:
            print(f"{name}: installed and current")
    return 0 if ok else 1


def install():
    if not TARGET.is_dir():
        raise SystemExit(f"{TARGET} does not exist; is this a git checkout")
    for name in NAMES:
        src, dst = SOURCE / name, TARGET / name
        shutil.copyfile(src, dst)
        dst.chmod(dst.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
        print(f"{name}: installed")
    return status()


if __name__ == "__main__":
    sys.exit(status() if "--status" in sys.argv[1:] else install())
