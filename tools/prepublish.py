"""Pre publication sweep.

The house procedure before a first push, from decision two of session two.
This tool performs the second of its three steps: it sweeps every blob of
every commit for things that should not be published. The other two steps,
the one line log of every commit and the check that the remote is empty, are
git commands and are run alongside it.

The sweep looks for secrets, tokens and personal paths. It is deliberately
noisy: a false positive costs a glance, and a false negative is published.

What it cannot do, and does not pretend to do: it cannot find a secret that
looks like ordinary prose, and it cannot judge whether a personal path
matters. It reports; a person decides.

A finding in a blob that is already committed cannot be removed without
rewriting history, and in this repository history cannot be rewritten,
because the root commit is the signature of the preregistration and its hash
is what that signature is. So a finding here is either accepted and declared,
or it stops the push. There is no third option and the tool says so.

Usage:
    python tools/prepublish.py            sweep every blob of every commit
    python tools/prepublish.py --tree     sweep the working tree only
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PATTERNS = [
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}\b")),
    ("google api key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("bearer credential", re.compile(r"\b[Aa]uthorization:\s*(?:Bearer|Basic)\s+\S+")),
    ("assigned secret", re.compile(
        r"\b(?:SECRET|TOKEN|PASSWORD|PASSWD|API[_-]?KEY|ACCESS[_-]?KEY)\b\s*[=:]\s*"
        r"['\"]?[A-Za-z0-9/+_-]{8,}")),
    ("windows user path", re.compile(r"[A-Za-z]:\\+Users\\+[^\\\s'\"]+")),
    ("unix home path", re.compile(r"/(?:home|Users)/[A-Za-z0-9._-]+")),
    ("email address", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
]

# Places where the string is the subject matter rather than an exposure.
# Each allowance names why. Nothing is allowed silently.
ALLOWED = [
    ("tools/prepublish.py", "the patterns themselves live here"),
]

TEXT_SUFFIXES = {".md", ".py", ".txt", ".jsonl", ".json", ".toml", ".cfg",
                 ".yml", ".yaml", ""}


def allowed(relpath):
    for path, why in ALLOWED:
        if relpath == path:
            return why
    return None


def scan(text, relpath, where):
    hits = []
    for label, rx in PATTERNS:
        for m in rx.finditer(text):
            line = text[:m.start()].count("\n") + 1
            hits.append((where, relpath, line, label, m.group(0)))
    return hits


def blobs():
    """Every distinct blob in every commit, with the commit that introduced it.

    Oldest first, so that a finding is reported against the commit where it
    entered the history rather than against the newest one that still carries
    it. Where it entered is what a person needs in order to judge it.
    """
    commits = subprocess.run(["git", "rev-list", "--all", "--reverse"], cwd=ROOT,
                             capture_output=True, check=True).stdout.decode().split()
    seen, out = set(), []
    for commit in commits:
        listing = subprocess.run(["git", "ls-tree", "-r", "-z", commit], cwd=ROOT,
                                 capture_output=True, check=True).stdout.decode()
        for record in listing.split("\0"):
            if not record:
                continue
            meta, relpath = record.split("\t", 1)
            blob = meta.split()[2]
            if (blob, relpath) in seen:
                continue
            seen.add((blob, relpath))
            out.append((commit, blob, relpath))
    return out


def sweep_history():
    hits, skipped = [], []
    for commit, blob, relpath in blobs():
        why = allowed(relpath)
        if why:
            skipped.append((relpath, why))
            continue
        if Path(relpath).suffix.lower() not in TEXT_SUFFIXES:
            continue
        raw = subprocess.run(["git", "cat-file", "blob", blob], cwd=ROOT,
                             capture_output=True, check=True).stdout
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        hits += scan(text, relpath, f"commit {commit[:12]}")
    return hits, skipped


def sweep_tree():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, check=True).stdout.decode()
    hits, skipped = [], []
    for relpath in [p for p in out.split("\0") if p]:
        why = allowed(relpath)
        if why:
            skipped.append((relpath, why))
            continue
        p = ROOT / relpath
        if not p.is_file() or Path(relpath).suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            hits += scan(p.read_text(encoding="utf-8"), relpath, "tree")
        except UnicodeDecodeError:
            continue
    return hits, skipped


def main(argv):
    tree_only = "--tree" in argv
    hits, skipped = sweep_tree() if tree_only else sweep_history()

    for relpath, why in skipped:
        print(f"not swept: {relpath}, because {why}")

    if not hits:
        scope = "the working tree" if tree_only else "every blob of every commit"
        print(f"prepublish sweep: CLEAN, nothing found across {scope}")
        return 0

    by_label = {}
    for where, relpath, line, label, text in hits:
        by_label.setdefault(label, []).append((where, relpath, line, text))
    for label in sorted(by_label):
        print(f"\n{label}: {len(by_label[label])} occurrence(s)")
        for where, relpath, line, text in by_label[label]:
            shown = text if len(text) <= 80 else text[:77] + "..."
            print(f"  [{where}] {relpath}:{line}: {shown}")

    print(f"\nprepublish sweep: {len(hits)} finding(s)")
    if not tree_only:
        print("A finding in a committed blob cannot be removed without "
              "rewriting history, and this repository does not rewrite "
              "history, because the root commit is the signature of the "
              "preregistration. Each finding is therefore either accepted "
              "and declared before the push, or it stops the push.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
