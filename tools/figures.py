"""Figure gate for commit messages.

Two rules are enforced, both stated in the opening instructions of this lane:

  R1. No figure appears in a commit message before it has come out of a
      checker. This tool is that checker. A numeral in a commit message must
      resolve to a registry record whose status is verified-here.

  R2. No figure is reused from an earlier report once its object has changed.
      The registry keys a figure by its object, not by its digits. A numeral
      whose registry record is cited-unverified, or which resolves to more
      than one object, is refused. Refusal is the correct outcome: the same
      digits standing for a different thing is the failure mode this rule
      exists to catch.

Since decision six of session two the gate also tells an identifier from a
measurement, under three conditions that are the whole substance of that
decision:

  E1. Every exemption carries a stated reason, declared in IDENTIFIERS below.
  E2. Every exemption is counted and printed. No numeral passes silently.
      A run that exempts something says so, says why, and says how many.
  E3. The registry beats the exemption. A token that appears in
      FIGURES.jsonl can never pass as an identifier, however much it looks
      like one. This is what stops a measurement dressing itself as a year.

The registry is FIGURES.jsonl at the repository root, one JSON object per
line, with fields: token, object, status, source, verified_by, utc.

status is one of:
  cited-unverified   the figure is known only from outside this repository
                     and has not been recomputed here. Not usable.
  verified-here      the figure was produced or reproduced inside this
                     repository by the artefact named in verified_by.

Scanning skips trailer lines, that is lines of the form `Word-Word: value`
at the start of a line, and comment lines. Everything else is scanned.

Usage:
    python tools/figures.py check-message PATH
    python tools/figures.py register --token T --object O --status S
                                     --source SRC [--verified-by V]
    python tools/figures.py list
    python tools/figures.py explain
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "FIGURES.jsonl"

STATUSES = {"cited-unverified", "verified-here"}
TRAILER = re.compile(r"^[A-Za-z][A-Za-z-]*:\s")
NUMERAL = re.compile(r"\d[\d.,]*")

# Declared identifier patterns. Each carries the reason printed when it is
# applied. Order matters only for reporting: the longest, most specific
# patterns come first so that a DOI is reported as a DOI and not as a year.
IDENTIFIERS = [
    ("doi", "a DOI, which names a deposit and measures nothing",
     re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")),
    ("orcid", "an ORCID, which names a person",
     re.compile(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b")),
    ("arxiv", "an archive identifier, which names a preprint",
     re.compile(r"\barXiv:\d{4}\.\d{4,5}(?:v\d+)?\b", re.IGNORECASE)),
    ("date", "a calendar date in ISO form",
     re.compile(r"\b\d{4}-\d{2}-\d{2}\b")),
    ("hash", "a hexadecimal object name, which addresses content",
     re.compile(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,40}\b")),
    ("label", "a label whose digits are bound to letters, such as a version, "
              "a session or a defect",
     re.compile(r"\b[A-Za-z][A-Za-z0-9]*-?v?\d+[A-Za-z0-9]*\b")),
    ("year", "a publication year",
     re.compile(r"\b(?:19|20|21)\d{2}\b")),
]


def load():
    if not REGISTRY.exists():
        return []
    records = []
    for lineno, raw in enumerate(REGISTRY.read_text(encoding="utf-8").splitlines(), 1):
        if raw.strip():
            try:
                records.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"FIGURES.jsonl line {lineno}: not JSON: {exc}")
    return records


def normalise(token):
    return token.rstrip(".,")


def scanned_lines(message):
    for lineno, line in enumerate(message.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or TRAILER.match(line):
            continue
        yield lineno, line


def scan(message):
    """Every numeral in the scanned body, as (line number, token)."""
    return [(lineno, normalise(m.group(0)))
            for lineno, line in scanned_lines(message)
            for m in NUMERAL.finditer(line)]


def identifier_spans(line):
    spans = []
    for kind, reason, rx in IDENTIFIERS:
        for m in rx.finditer(line):
            spans.append((m.start(), m.end(), kind, reason))
    return spans


def covering(spans, start, end):
    """The first declared span that wholly contains a numeral, or None.

    Order follows IDENTIFIERS, so a date is reported as a date rather than as
    the year hiding inside it.
    """
    for s, e, kind, reason in spans:
        if s <= start and end <= e:
            return s, e, kind, reason
    return None


def analyse(message, registry_tokens):
    """Split the numerals of a message into exempted and accountable ones.

    An exemption is reported as the whole identifier that earned it, not as
    the digits inside it, and an identifier holding several runs of digits is
    counted once. A token present in the registry is accountable whatever it
    looks like: that is condition E3 and no pattern overrides it.
    """
    exempt, accountable = {}, []
    for lineno, line in scanned_lines(message):
        spans = identifier_spans(line)
        for m in NUMERAL.finditer(line):
            token = normalise(m.group(0))
            if token in registry_tokens:
                accountable.append((lineno, token))
                continue
            hit = covering(spans, m.start(), m.start() + len(token))
            if hit:
                s, e, kind, reason = hit
                exempt.setdefault((lineno, s, e), (lineno, line[s:e], kind, reason))
            else:
                accountable.append((lineno, token))
    return [exempt[k] for k in sorted(exempt)], accountable


def report_exemptions(exempt):
    """Condition E2: nothing passes silently."""
    if not exempt:
        return
    by_kind = {}
    for lineno, token, kind, reason in exempt:
        by_kind.setdefault(kind, []).append((lineno, token, reason))
    total = len(exempt)
    print(f"figure gate: {total} numeral(s) exempted as identifiers, by reason:")
    for kind in sorted(by_kind):
        items = by_kind[kind]
        tokens = ", ".join(f"{t!r} (line {ln})" for ln, t, _ in items)
        print(f"  {kind}: {len(items)}, because it is {items[0][2]}")
        print(f"    {tokens}")


def check_message(path):
    message = Path(path).read_text(encoding="utf-8")
    records = load()
    tokens_in_registry = {r["token"] for r in records}
    exempt, accountable = analyse(message, tokens_in_registry)

    report_exemptions(exempt)

    if not accountable:
        print("figure gate: PASS, no numeral in this message is accountable "
              "as a figure")
        return 0

    refused = 0
    for lineno, token in accountable:
        matching = [r for r in records if r["token"] == token]
        verified = [r for r in matching if r["status"] == "verified-here"]
        unverified = [r for r in matching if r["status"] == "cited-unverified"]

        if not matching:
            print(f"line {lineno}: figure {token!r} is not in the registry and "
                  f"matches no declared identifier pattern. Register it with "
                  f"its object and its status, or remove it from the message.")
            refused += 1
        elif unverified:
            objects = "; ".join(r["object"] for r in unverified)
            print(f"line {lineno}: figure {token!r} is cited-unverified in "
                  f"this repository. Object on record: {objects}. It has not "
                  f"been recomputed here, so it may not go into a commit "
                  f"message.")
            refused += 1
        elif len(verified) > 1:
            objects = "; ".join(r["object"] for r in verified)
            print(f"line {lineno}: figure {token!r} resolves to more than one "
                  f"object: {objects}. Disambiguate in the registry or keep "
                  f"the figure out of the message.")
            refused += 1

    if refused:
        print(f"figure gate: FAIL, {refused} refusal(s) out of "
              f"{len(accountable)} accountable numeral(s)")
        print("A commit message with no accountable numeral always passes.")
        return 1
    print(f"figure gate: PASS, {len(accountable)} accountable numeral(s), "
          f"every one resolving to an object verified here")
    return 0


def register(token, obj, status, source, verified_by):
    if status not in STATUSES:
        raise SystemExit(f"status must be one of: {', '.join(sorted(STATUSES))}")
    if status == "verified-here" and not verified_by:
        raise SystemExit("verified-here requires --verified-by naming the "
                         "artefact in this repository that produced it")
    records = load()
    for r in records:
        if r["token"] == token and r["object"] == obj:
            raise SystemExit("that token and object are already registered; "
                             "append a correction rather than a duplicate")
    record = {
        "token": token,
        "object": obj,
        "status": status,
        "source": source,
        "verified_by": verified_by,
        "utc": datetime.datetime.now(datetime.timezone.utc)
                       .strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    with REGISTRY.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"registered {token!r} as {status}")
    return 0


def listing():
    records = load()
    if not records:
        print("registry: EMPTY. No figure may appear in a commit message.")
        return 0
    for r in records:
        print(f"{r['token']:<12} {r['status']:<18} {r['object']}")
        print(f"{'':<12} source: {r['source']}")
        if r["verified_by"]:
            print(f"{'':<12} verified by: {r['verified_by']}")
    return 0


def explain():
    print("Identifier patterns, in the order they are reported.")
    print("A token in FIGURES.jsonl is never exempted by any of them.\n")
    for kind, reason, rx in IDENTIFIERS:
        print(f"  {kind}: {reason}")
        print(f"    {rx.pattern}")
    print(f"\nRegistered tokens, which no pattern can exempt: "
          f"{', '.join(sorted({r['token'] for r in load()})) or 'none'}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("check-message")
    p.add_argument("path")
    p = sub.add_parser("register")
    p.add_argument("--token", required=True)
    p.add_argument("--object", dest="obj", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--source", required=True)
    p.add_argument("--verified-by", dest="verified_by", default="")
    sub.add_parser("list")
    sub.add_parser("explain")
    a = ap.parse_args()
    if a.cmd == "check-message":
        return check_message(a.path)
    if a.cmd == "register":
        return register(a.token, a.obj, a.status, a.source, a.verified_by)
    if a.cmd == "list":
        return listing()
    if a.cmd == "explain":
        return explain()


if __name__ == "__main__":
    sys.exit(main() or 0)
