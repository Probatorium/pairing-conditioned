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


def scan(message):
    hits = []
    for lineno, line in enumerate(message.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or TRAILER.match(line):
            continue
        for m in NUMERAL.finditer(line):
            hits.append((lineno, normalise(m.group(0))))
    return hits


def check_message(path):
    message = Path(path).read_text(encoding="utf-8")
    hits = scan(message)
    if not hits:
        print("figure gate: PASS, the message carries no figure")
        return 0

    records = load()
    refused = 0
    for lineno, token in hits:
        matching = [r for r in records if r["token"] == token]
        verified = [r for r in matching if r["status"] == "verified-here"]
        unverified = [r for r in matching if r["status"] == "cited-unverified"]

        if not matching:
            print(f"line {lineno}: figure {token!r} is not in the registry. "
                  f"Register it with its object and its status, or remove it "
                  f"from the message.")
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
        print(f"figure gate: FAIL, {refused} refusal(s)")
        print("A commit message with no numeral always passes. That is the "
              "intended default until something has been measured here.")
        return 1
    print(f"figure gate: PASS, every figure resolves to a verified object")
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
    a = ap.parse_args()
    if a.cmd == "check-message":
        return check_message(a.path)
    if a.cmd == "register":
        return register(a.token, a.obj, a.status, a.source, a.verified_by)
    if a.cmd == "list":
        return listing()


if __name__ == "__main__":
    sys.exit(main() or 0)
