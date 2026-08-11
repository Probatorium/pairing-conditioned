"""Tests for the gates.

A gate nobody has tried to break is a decoration. These tests try to break
each gate in the way it is most likely to fail in use: a forbidden character
that looks innocent, an exemption applied where it was not granted, an edited
past entry in a hash chain, and a numeral smuggled into a commit message.

Run: python tools/test_gates.py
"""

import hashlib
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import dashcheck
import effortlog
import figures

PASSED = []
FAILED = []


def check(label, condition):
    (PASSED if condition else FAILED).append(label)
    print(f"{'ok  ' if condition else 'FAIL'} {label}")


def test_dash_gate():
    # Escapes, not literals, for the reason given in tools/dashcheck.py.
    em = chr(0x2014)
    en = chr(0x2013)
    minus = chr(0x2212)

    check("em dash is caught in an ordinary file",
          len(dashcheck.offences_in_text(f"a{em}b", "PREREGISTRATION.md")) == 1)
    check("em dash is caught even in an exempted file",
          len(dashcheck.offences_in_text(f"a{em}b", "REFERENCES.md")) == 1)
    check("minus sign is caught",
          len(dashcheck.offences_in_text(f"a{minus}b", "PREREGISTRATION.md")) == 1)
    check("en dash is caught outside an exempted file",
          len(dashcheck.offences_in_text(f"12{en}34", "PREREGISTRATION.md")) == 1)
    check("en dash in a numeric range passes inside an exempted file",
          dashcheck.offences_in_text(f"pp. 12{en}34", "REFERENCES.md") == [])
    check("en dash between words is caught inside an exempted file",
          len(dashcheck.offences_in_text(f"well{en}known", "REFERENCES.md")) == 1)
    check("an ASCII hyphen is never an offence",
          dashcheck.offences_in_text("pairing-conditioned", "NAME-GATE.md") == [])
    check("the offence is located on the right line",
          dashcheck.locate(f"one\ntwo{em}", 7) == (2, 4))


def test_effort_chain():
    def sign(entry, prev):
        entry = dict(entry)
        entry["prev"] = prev
        entry["hash"] = effortlog.digest(entry, prev)
        return entry

    base = {"index": 0, "utc": "2026-08-11T00:00:00Z", "session": "S",
            "kind": "OPEN", "class": "GOVERNANCE", "summary": "open",
            "artifacts": [], "commit": ""}
    first = sign(base, effortlog.GENESIS)
    second = sign({**base, "index": 1, "kind": "WORK", "class": "APPARATUS",
                   "summary": "work"}, first["hash"])

    check("a freshly signed entry verifies",
          effortlog.digest(first, effortlog.GENESIS) == first["hash"])
    check("editing an entry breaks its own digest",
          effortlog.digest({**first, "summary": "tampered"},
                           effortlog.GENESIS) != first["hash"])
    check("the chain links the second entry to the first",
          second["prev"] == first["hash"])
    check("editing the first entry orphans the second",
          effortlog.digest({**first, "summary": "tampered"},
                           effortlog.GENESIS) != second["prev"])
    check("canonical form ignores the hash field itself",
          "hash" not in effortlog.canonical(first))
    check("canonical form is stable under key order",
          effortlog.canonical(first)
          == effortlog.canonical(dict(reversed(list(first.items())))))
    check("every class used by this lane is declared",
          set(effortlog.CLASSES) >= {"GOVERNANCE", "APPARATUS", "ANALYSIS"})


def test_figure_gate():
    check("a message with no numeral has no hits",
          figures.scan("Contact rules for the frozen work") == [])
    check("a numeral in the body is a hit",
          figures.scan("the count is 1013 here") == [(1, "1013")])
    check("a trailer line is not scanned",
          figures.scan("Co-Authored-By: Claude Opus 5 <x@y>") == [])
    check("a comment line is not scanned",
          figures.scan("# on branch main with 3 files") == [])
    check("trailing punctuation is stripped from the token",
          figures.scan("the value was 1008.") == [(1, "1008")])
    check("a numeral after a trailer, on its own line, is still caught",
          figures.scan("Co-Authored-By: X\n\nand 42 more") == [(3, "42")])
    check("a decimal is captured whole",
          figures.scan("p below 0.05 was seen") == [(1, "0.05")])


def main():
    print("dash gate")
    test_dash_gate()
    print("\neffort log chain")
    test_effort_chain()
    print("\nfigure gate")
    test_figure_gate()
    print(f"\npassed {len(PASSED)}, failed {len(FAILED)}")
    if FAILED:
        for label in FAILED:
            print(f"  failed: {label}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
