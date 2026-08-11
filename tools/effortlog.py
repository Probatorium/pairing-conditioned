"""Effort log with a hash chain.

The log is EFFORT-LOG.jsonl at the repository root, one JSON object per line,
append only. Each entry carries the digest of the entry before it, so any
edit to a past entry breaks every digest after it and the break is located
exactly.

Chain rule, fixed here and not changed without a declared defect:

    canonical = json.dumps(entry without its own hash field,
                           sort_keys=True, separators=(',', ':'),
                           ensure_ascii=False)
    hash      = sha256((canonical + "|" + prev).encode("utf-8")).hexdigest()

The genesis entry uses prev = sixty-four zeros.

What the log records is what can be checked: the UTC clock at the moment the
entry was appended, the session it belongs to, the declared class of the
work, a summary, the artifacts touched, and where applicable the commit that
carried the work. Elapsed time is derived from the timestamps by the reader.
No effort figure is asserted that the log cannot support.

Sessions open and close. Work entries outside an open session are a
verification failure, as is a session that opens twice or never closes.

Usage:
    python tools/effortlog.py open  --session S --summary TEXT
    python tools/effortlog.py work  --class C --summary TEXT [--artifact A ...] [--commit H]
    python tools/effortlog.py close --summary TEXT
    python tools/effortlog.py verify
    python tools/effortlog.py show [--last N]
"""

import argparse
import datetime
import hashlib
import json
import sys
from pathlib import Path

LOG = Path(__file__).resolve().parent.parent / "EFFORT-LOG.jsonl"
GENESIS = "0" * 64

CLASSES = [
    "GOVERNANCE",       # rules, contact rules, decisions of process
    "PREREGISTRATION",  # the signed design and anything that reads it
    "TERM-GATE",        # the naming check
    "APPARATUS",        # tooling, gates, the log itself
    "LITERATURE",       # background review, citation verification
    "DATA",             # acquisition, manifest, digests
    "IMPLEMENTATION",   # code that computes the object of study
    "ANALYSIS",         # running the declared design
    "WRITING",          # prose intended for a reader outside the lane
    "REPORTING",        # session reports and rigour reports
    "DECISION",         # something referred to Alexis, or resolved by him
]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def canonical(entry):
    body = {k: v for k, v in entry.items() if k != "hash"}
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(entry, prev):
    return hashlib.sha256((canonical(entry) + "|" + prev).encode("utf-8")).hexdigest()


def read():
    if not LOG.exists():
        return []
    entries = []
    for lineno, raw in enumerate(LOG.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            entries.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"EFFORT-LOG.jsonl line {lineno}: not JSON: {exc}")
    return entries


def open_session(entries):
    """Return the id of the session currently open, or None."""
    current = None
    for e in entries:
        if e["kind"] == "OPEN":
            current = e["session"]
        elif e["kind"] == "CLOSE":
            current = None
    return current


def append(kind, klass, summary, session=None, artifacts=None, commit=""):
    entries = read()
    prev = entries[-1]["hash"] if entries else GENESIS
    live = open_session(entries)

    if kind == "OPEN":
        if live is not None:
            raise SystemExit(f"session {live} is still open; close it first")
        if not session:
            raise SystemExit("open requires --session")
    else:
        if live is None:
            raise SystemExit("no session is open; run open first")
        session = live
    if kind == "WORK" and klass not in CLASSES:
        raise SystemExit(f"class must be one of: {', '.join(CLASSES)}")

    entry = {
        "index": len(entries),
        "utc": now(),
        "session": session,
        "kind": kind,
        "class": klass,
        "summary": summary,
        "artifacts": sorted(artifacts or []),
        "commit": commit,
        "prev": prev,
    }
    entry["hash"] = digest(entry, prev)
    with LOG.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
    print(f"appended index {entry['index']} hash {entry['hash'][:16]}")


def verify():
    entries = read()
    if not entries:
        print("effort log: EMPTY, nothing to verify")
        return 1
    prev = GENESIS
    live = None
    seen_sessions = set()
    failures = 0
    for i, e in enumerate(entries):
        if e.get("index") != i:
            print(f"entry {i}: index field says {e.get('index')}")
            failures += 1
        if e.get("prev") != prev:
            print(f"entry {i}: prev does not match the previous hash")
            failures += 1
        recomputed = digest(e, e.get("prev", ""))
        if recomputed != e.get("hash"):
            print(f"entry {i}: hash mismatch, content has been altered")
            print(f"  stored     {e.get('hash')}")
            print(f"  recomputed {recomputed}")
            failures += 1
        kind = e.get("kind")
        if kind == "OPEN":
            if live is not None:
                print(f"entry {i}: session {e['session']} opens while {live} is open")
                failures += 1
            if e["session"] in seen_sessions:
                print(f"entry {i}: session {e['session']} opens a second time")
                failures += 1
            seen_sessions.add(e["session"])
            live = e["session"]
        elif kind == "CLOSE":
            if live is None:
                print(f"entry {i}: close with no session open")
                failures += 1
            live = None
        elif kind == "WORK":
            if live is None:
                print(f"entry {i}: work outside any open session")
                failures += 1
            if e.get("class") not in CLASSES:
                print(f"entry {i}: undeclared class {e.get('class')!r}")
                failures += 1
        else:
            print(f"entry {i}: unknown kind {kind!r}")
            failures += 1
        prev = e.get("hash", "")

    tail = entries[-1]["hash"]
    if failures:
        print(f"effort log: FAIL, {failures} problem(s) across {len(entries)} entries")
        return 1
    state = "closed" if live is None else f"OPEN ({live})"
    print(f"effort log: PASS, {len(entries)} entries, chain intact, session state {state}")
    print(f"head digest {tail}")
    return 0


def show(last):
    entries = read()
    if last:
        entries = entries[-last:]
    for e in entries:
        art = ", ".join(e["artifacts"]) if e["artifacts"] else ""
        commit = f" [{e['commit'][:12]}]" if e.get("commit") else ""
        print(f"{e['index']:>3} {e['utc']} {e['session']} {e['kind']:<5} "
              f"{e['class']:<15} {e['summary']}{commit}")
        if art:
            print(f"     artifacts: {art}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("open")
    p.add_argument("--session", required=True)
    p.add_argument("--summary", required=True)

    p = sub.add_parser("work")
    p.add_argument("--class", dest="klass", required=True)
    p.add_argument("--summary", required=True)
    p.add_argument("--artifact", action="append", default=[])
    p.add_argument("--commit", default="")

    p = sub.add_parser("close")
    p.add_argument("--summary", required=True)

    sub.add_parser("verify")
    p = sub.add_parser("show")
    p.add_argument("--last", type=int, default=0)

    a = ap.parse_args()
    if a.cmd == "open":
        return append("OPEN", "GOVERNANCE", a.summary, session=a.session)
    if a.cmd == "work":
        return append("WORK", a.klass, a.summary, artifacts=a.artifact, commit=a.commit)
    if a.cmd == "close":
        return append("CLOSE", "GOVERNANCE", a.summary)
    if a.cmd == "verify":
        return verify()
    if a.cmd == "show":
        return show(a.last)


if __name__ == "__main__":
    sys.exit(main() or 0)
