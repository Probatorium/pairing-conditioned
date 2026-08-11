"""Receive the King Wen sequence from the neighbour, at its deposit tag.

Decision five of session two. The sequence is received, not derived. This
lane does not reconstruct the King Wen order, does not correct it, and does
not prefer any reconstruction of its own over the received list.

The transcription is mechanical rather than typed, so that a copying error is
not one of the ways this lane can be wrong. The tool reads the blob at the
tag through git, without moving the neighbour's working tree, extracts the
named symbol, and writes it with its provenance.

The local checkout is passed on the command line and is never stored. A path
on one machine identifies an account and is not part of the public record;
the repository and the tag are what identify the source.

Checks run on the received list before it is written. They are checks on the
transcription, not a recomputation of the sequence:

  the list has sixty-four entries,
  the entries are distinct,
  every entry lies in the range of a six bit value.

A precondition of the preregistration, that the adjacency pairing of this
sequence equals the matching of the cited theorem, is NOT checked here. That
is gate P1 of the analysis and it belongs to the analysis.

Usage:
    python tools/receive_kingwen.py --checkout PATH [--write]
"""

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "data" / "king-wen-received.json"

SOURCE = {
    "repository": "github.com/Probatorium/kingwen-orderings-replication",
    "tag": "zenodo-v3",
    "file": "verify_paper.py",
    "symbol": "KING_WEN",
}
SYMBOL_RX = re.compile(r"^KING_WEN\s*=\s*(\[[^\]]*\])", re.MULTILINE)


def read_blob(checkout):
    ref = f"{SOURCE['tag']}:{SOURCE['file']}"
    proc = subprocess.run(["git", "-C", checkout, "show", ref],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"could not read {ref} from the checkout given: "
                         f"{proc.stderr.strip()}")
    return proc.stdout


def extract(text):
    m = SYMBOL_RX.search(text)
    if not m:
        raise SystemExit(f"symbol {SOURCE['symbol']} not found at "
                         f"{SOURCE['tag']}:{SOURCE['file']}")
    return ast.literal_eval(m.group(1))


def check(values):
    problems = []
    if len(values) != 64:
        problems.append(f"the list has {len(values)} entries, not sixty-four")
    if len(set(values)) != len(values):
        problems.append("the entries are not distinct")
    out_of_range = [v for v in values if not isinstance(v, int) or not 0 <= v < 64]
    if out_of_range:
        problems.append(f"entries outside the range of a six bit value: "
                        f"{out_of_range}")
    return problems


def build(values, retrieved):
    return {
        "what": "The received King Wen sequence: position, zero indexed, to "
                "hexagram value. King Wen number k occupies position k minus "
                "one.",
        "status": "received data, never recomputed in this lane",
        "provenance": {**SOURCE, "retrieved": retrieved,
                       "access": "read only, addressed at the tag, the "
                                 "neighbour's working tree was not moved"},
        "corroboration": "Recorded as received from the prior lane and not "
                         "verified here: this list was corroborated in full "
                         "against appendix A of Radisic in that lane, so it "
                         "is not single sourced. This lane did not repeat "
                         "that corroboration and does not claim to have.",
        "bit_convention_note": "The source states that its trigram bit "
                               "patterns are read bottom to top with the "
                               "solid line as one. That is the convention of "
                               "the values below. The four conventions of the "
                               "preregistration are derived from these values "
                               "by the analysis, not by re-reading the source.",
        "not_checked_here": "That the adjacency pairing of this sequence "
                            "equals the matching of the cited theorem. That "
                            "is precondition P1 of the preregistration and it "
                            "belongs to the analysis.",
        "values": values,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--checkout", required=True,
                    help="local checkout of the neighbour; not stored anywhere")
    ap.add_argument("--retrieved", required=True, help="retrieval date, ISO")
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    values = extract(read_blob(a.checkout))
    problems = check(values)
    for p in problems:
        print(f"transcription check: {p}")
    if problems:
        print("receive: FAIL, nothing written")
        return 1
    print(f"transcription check: PASS, sixty-four distinct entries, all in range")

    payload = build(values, a.retrieved)
    text = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()

    if a.write:
        TARGET.parent.mkdir(exist_ok=True)
        TARGET.write_text(text, encoding="utf-8", newline="\n")
        print(f"written: {TARGET.relative_to(ROOT).as_posix()}")
    else:
        print("dry run, nothing written; pass --write to write")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
