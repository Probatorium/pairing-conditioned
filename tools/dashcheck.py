"""Dash gate.

Policy, in force from the apparatus commit of this repository:

  U+2014 EM DASH is forbidden everywhere, with no exemption of any kind.
  U+2010, U+2011, U+2012, U+2015 and U+2212 are forbidden everywhere.
  U+2013 EN DASH is forbidden except where explicitly exempted.

The only exemption granted at the opening of this lane is the numeric range
of an APA reference, that is an en dash standing between two digits, and only
inside a file registered in EXEMPT_FILES below. Registration is by path and
is deliberately narrow: adding a file to that list is a visible edit to this
tool and therefore a reviewable act.

Exit status is zero when the tree is clean and one when it is not. Every
offence is printed with its file, line, column and the offending codepoint.

Usage:
    python tools/dashcheck.py                 sweep every tracked text file
    python tools/dashcheck.py PATH [PATH ...] sweep the named files
    python tools/dashcheck.py --history       sweep every blob in every commit
"""

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

# Written as escapes, never as literals. A gate whose own source carries the
# character it forbids would need an exemption for itself, and an exemption
# for the enforcer is the first hole anyone should look for. There is none.
FORBIDDEN_ALWAYS = {
    chr(0x2010): "HYPHEN",
    chr(0x2011): "NON-BREAKING HYPHEN",
    chr(0x2012): "FIGURE DASH",
    chr(0x2014): "EM DASH",
    chr(0x2015): "HORIZONTAL BAR",
    chr(0x2212): "MINUS SIGN",
}
EN_DASH = chr(0x2013)

# Files permitted to carry an en dash, and only in a numeric range.
EXEMPT_FILES = {
    "REFERENCES.md",
}

APA_RANGE = re.compile(r"(?<=\d)" + EN_DASH + r"(?=\d)")

TEXT_SUFFIXES = {".md", ".py", ".txt", ".jsonl", ".json", ".toml", ".cfg",
                 ".yml", ".yaml", ".gitattributes", ".gitignore", ""}


def tracked_files():
    out = subprocess.run(["git", "ls-files", "-z"], capture_output=True,
                         check=True).stdout.decode("utf-8")
    return [p for p in out.split("\0") if p]


def offences_in_text(text, relpath):
    exempt = relpath in EXEMPT_FILES
    allowed_spans = set()
    if exempt:
        allowed_spans = {m.start() for m in APA_RANGE.finditer(text)}
    found = []
    for offset, ch in enumerate(text):
        if ch in FORBIDDEN_ALWAYS:
            found.append((offset, ch, FORBIDDEN_ALWAYS[ch], "forbidden everywhere"))
        elif ch == EN_DASH and offset not in allowed_spans:
            reason = ("en dash outside a numeric range" if exempt
                      else "en dash in a file with no exemption")
            found.append((offset, ch, "EN DASH", reason))
    return found


def locate(text, offset):
    head = text[:offset]
    line = head.count("\n") + 1
    col = offset - (head.rfind("\n") + 1) + 1
    return line, col


def report(relpath, text, found):
    for offset, ch, name, reason in found:
        line, col = locate(text, offset)
        print(f"{relpath}:{line}:{col}: U+{ord(ch):04X} {name}: {reason}")
    return len(found)


def sweep_worktree(paths):
    total = 0
    for relpath in paths:
        p = Path(relpath)
        if not p.is_file():
            continue
        if p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"{relpath}: not valid UTF-8, not swept")
            total += 1
            continue
        total += report(relpath, text, offences_in_text(text, relpath))
    return total


def sweep_history():
    commits = subprocess.run(["git", "rev-list", "--all"], capture_output=True,
                             check=True).stdout.decode().split()
    total = 0
    seen = set()
    for commit in commits:
        listing = subprocess.run(["git", "ls-tree", "-r", "-z", commit],
                                 capture_output=True, check=True).stdout.decode()
        for record in listing.split("\0"):
            if not record:
                continue
            meta, relpath = record.split("\t", 1)
            blob = meta.split()[2]
            if (blob, relpath) in seen:
                continue
            seen.add((blob, relpath))
            if Path(relpath).suffix.lower() not in TEXT_SUFFIXES:
                continue
            raw = subprocess.run(["git", "cat-file", "blob", blob],
                                 capture_output=True, check=True).stdout
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                continue
            found = offences_in_text(text, relpath)
            if found:
                print(f"in commit {commit[:12]}:")
                total += report(relpath, text, found)
    return total


def main(argv):
    if argv and argv[0] == "--history":
        bad = sweep_history()
        scope = "every blob of every commit"
    elif argv:
        bad = sweep_worktree(argv)
        scope = "the named files"
    else:
        bad = sweep_worktree(tracked_files())
        scope = "every tracked text file"
    if bad:
        print(f"dash gate: FAIL, {bad} offence(s) across {scope}")
        return 1
    print(f"dash gate: PASS, {scope} clean")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
