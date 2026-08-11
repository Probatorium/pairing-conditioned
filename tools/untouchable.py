"""Untouchable gate.

Contact rule four names repositories that this lane does not touch and does
not cite. They are unpublished: no DOI, no deposit, no tag, and third party
verification of that lane is outstanding. A citation to a manuscript a reader
cannot obtain is not a citation, so the rule is not only "do not read" but
also "do not name as a source".

A rule that is only written down is a rule nobody can check. This gate makes
it executable. It fails if:

  1. a remote of this repository points at one of them,
  2. a submodule or an object alternate points at one of them,
  3. one of them is named anywhere in the tracked tree, outside the short
     list of files where declaring the rule requires naming them,
  4. one of them is named anywhere in the history, under the same allowance,
  5. one of them appears in the reference list, which is a citation and is
     refused separately and loudly, because that is the failure this rule
     exists to prevent.

The allowance is deliberately short. Adding a file to it is an edit to this
tool and therefore a reviewable act.

Usage:
    python tools/untouchable.py              tree, history, remotes, config
    python tools/untouchable.py --no-history skip the history scan
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Contact rule four. Named as repository paths, not as deposit tags, because
# they have none.
UNTOUCHABLE = [
    "stasis-antecedentes",
    "minimal-verified-paper",
    "defect-injection-study",
    "stasis",
]

# Files that must name them in order to declare the rule at all.
ALLOWED = {
    "CONTACT-RULES.md",
    "DECISIONS.md",
    "tools/untouchable.py",
}
ALLOWED_GLOBS = ("SESSION-REPORT-",)

# Never allowed to name them, at all, because naming a source there is citing it.
CITATION_FILES = {"REFERENCES.md", "BACKGROUND-REVIEW.md"}

TEXT_SUFFIXES = {".md", ".py", ".txt", ".jsonl", ".json", ".toml", ".cfg",
                 ".yml", ".yaml", ""}


def patterns():
    # Longest first, and bounded so that `stasis` does not fire inside
    # `stasis-antecedentes` and report the same mention twice.
    joined = "|".join(re.escape(name) for name in UNTOUCHABLE)
    return re.compile(r"(?<![A-Za-z0-9-])(" + joined + r")(?![A-Za-z0-9-])",
                      re.IGNORECASE)


def allowed(relpath):
    return relpath in ALLOWED or any(Path(relpath).name.startswith(g)
                                     for g in ALLOWED_GLOBS)


def scan_text(text, relpath, where, rx):
    hits = []
    for m in rx.finditer(text):
        line = text[:m.start()].count("\n") + 1
        hits.append((where, relpath, line, m.group(1)))
    return hits


def check_remotes(rx):
    out = subprocess.run(["git", "remote", "-v"], cwd=ROOT,
                         capture_output=True, text=True).stdout
    return [("remote", "git remote", 0, m.group(1)) for m in rx.finditer(out)]


def check_config(rx):
    problems = []
    modules = ROOT / ".gitmodules"
    if modules.exists():
        problems += scan_text(modules.read_text(encoding="utf-8"),
                              ".gitmodules", "config", rx)
    alternates = ROOT / ".git" / "objects" / "info" / "alternates"
    if alternates.exists():
        problems += scan_text(alternates.read_text(encoding="utf-8"),
                              "objects/info/alternates", "config", rx)
    return problems


def tracked():
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT,
                         capture_output=True, check=True).stdout.decode()
    return [p for p in out.split("\0") if p]


def check_tree(rx):
    problems = []
    for relpath in tracked():
        if Path(relpath).suffix.lower() not in TEXT_SUFFIXES:
            continue
        p = ROOT / relpath
        if not p.is_file():
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        hits = scan_text(text, relpath, "tree", rx)
        if relpath in CITATION_FILES and hits:
            problems += [("CITATION", *h[1:]) for h in hits]
        elif not allowed(relpath):
            problems += hits
    return problems


def check_history(rx):
    commits = subprocess.run(["git", "rev-list", "--all"], cwd=ROOT,
                             capture_output=True, check=True).stdout.decode().split()
    problems, seen = [], set()
    for commit in commits:
        listing = subprocess.run(["git", "ls-tree", "-r", "-z", commit], cwd=ROOT,
                                 capture_output=True, check=True).stdout.decode()
        for record in listing.split("\0"):
            if not record:
                continue
            meta, relpath = record.split("\t", 1)
            blob = meta.split()[2]
            if (blob, relpath) in seen or allowed(relpath):
                continue
            seen.add((blob, relpath))
            if Path(relpath).suffix.lower() not in TEXT_SUFFIXES:
                continue
            raw = subprocess.run(["git", "cat-file", "blob", blob], cwd=ROOT,
                                 capture_output=True, check=True).stdout
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
            hits = scan_text(text, relpath, f"history {commit[:12]}", rx)
            if relpath in CITATION_FILES:
                hits = [("CITATION", *h[1:]) for h in hits]
            problems += hits
    return problems


def main(argv):
    rx = patterns()
    problems = check_remotes(rx) + check_config(rx) + check_tree(rx)
    if "--no-history" not in argv:
        problems += check_history(rx)

    citations = [p for p in problems if p[0] == "CITATION"]
    for where, relpath, line, name in problems:
        if where == "CITATION":
            print(f"{relpath}:{line}: {name!r} named in a reference or review "
                  f"file. That is a citation to an unpublished manuscript and "
                  f"contact rule four forbids it.")
        else:
            print(f"[{where}] {relpath}:{line}: {name!r} named outside the "
                  f"files permitted to declare the rule.")

    if problems:
        print(f"untouchable gate: FAIL, {len(problems)} mention(s), "
              f"of which {len(citations)} would be a citation")
        return 1
    scope = "tree, remotes and config" if "--no-history" in argv else \
            "tree, remotes, config and every blob of every commit"
    print(f"untouchable gate: PASS, no untouchable repository is named, "
          f"linked or cited across {scope}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
