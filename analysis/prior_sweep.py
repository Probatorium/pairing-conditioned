"""Term sweep of the deposited neighbours, for the one question the review has left.

QUESTION, fixed in the effort log before a single file was read and not
adjusted afterwards: does either work measure, on rung P1 or on any rung, the
count of discordant pairs of the King Wen sequence against the binary order,
or any quantity from which that count follows.

The sweep does not answer that question. Reading answers it. The sweep exists
so that the reading can be audited: it says where the vocabulary of the
statistic occurs, where the vocabulary of the conditional family occurs, and
where the two occur in the same file, which is the only place the measurement
could be hiding.

Term groups are declared here and are not adjusted after seeing the counts.

Everything is read only at the deposit tags. Checkout paths are passed on the
command line and stored nowhere.

Usage:
    python analysis/prior_sweep.py --kingwen PATH --ladder PATH --forced PATH
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import core
import neighbour

FORCED_TAG = "zenodo-v1"

# Declared before the counts were seen.
GROUPS = {
    "statistic": [r"inversion", r"kendall", r"\btau\b", r"discordan",
                  r"concordan", r"spearman", r"footrule",
                  r"rank correlation"],
    "reference order": [r"binary order", r"binary ordering", r"binary count",
                        r"against binary", r"vs\.? binary"],
    "conditional family": [r"pair-preserving", r"pair preserving",
                           r"conditional null", r"\brung\b", r"\bladder\b",
                           r"\bP1\b", r"\bP2\b", r"\bP3\b", r"\bP4\b",
                           r"\bP5\b"],
    "witness figures": [r"\b1013\b", r"\b1008\b", r"\b2016\b", r"\b86\.3\b"],
}

SUFFIXES = {".py", ".md", ".tex", ".txt"}


def listing(checkout, tag):
    import subprocess
    out = subprocess.run(["git", "-C", str(checkout), "ls-tree", "-r",
                          "--name-only", tag], capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit(f"could not list {tag}: {out.stderr.strip()}")
    return [p for p in out.stdout.split("\n")
            if p and Path(p).suffix.lower() in SUFFIXES]


def sweep(checkout, tag, label, skip_prefix=None):
    print(f"\n=== {label}, at {tag}")
    compiled = {g: [re.compile(p, re.IGNORECASE) for p in pats]
                for g, pats in GROUPS.items()}
    per_file, totals = {}, {g: 0 for g in GROUPS}
    both = []
    files = listing(checkout, tag)
    skipped = 0
    for path in files:
        if skip_prefix and path.startswith(skip_prefix):
            skipped += 1
            continue
        blob, _ = neighbour.read_at_tag(checkout, tag, path)
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
        counts = {g: sum(len(rx.findall(text)) for rx in rxs)
                  for g, rxs in compiled.items()}
        if any(counts.values()):
            per_file[path] = counts
            for g, n in counts.items():
                totals[g] += n
        if counts["statistic"] and counts["conditional family"]:
            both.append(path)

    print(f"  files swept: {len(files) - skipped}"
          + (f", skipped under {skip_prefix}: {skipped}" if skipped else ""))
    for g, n in totals.items():
        print(f"  {g}: {n}")
    print(f"  files where the statistic and the conditional family co-occur: "
          f"{len(both)}")
    for p in both:
        c = per_file[p]
        print(f"    {p}: statistic {c['statistic']}, "
              f"family {c['conditional family']}, "
              f"reference order {c['reference order']}, "
              f"witness figures {c['witness figures']}")
    return {"tag": tag, "files_swept": len(files) - skipped,
            "skipped": skipped, "totals": totals,
            "cooccurrence_files": both, "per_file": per_file}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kingwen", required=True)
    ap.add_argument("--ladder", required=True)
    ap.add_argument("--forced", required=True)
    a = ap.parse_args()

    out = {"question": (
        "does either work measure, on rung P1 or on any rung, the count of "
        "discordant pairs of the King Wen sequence against the binary order, "
        "or any quantity from which that count follows"),
        "groups": {g: p for g, p in GROUPS.items()}}

    out["kingwen"] = sweep(a.kingwen, neighbour.KINGWEN_TAG,
                           "kingwen-orderings-replication")
    # The ladder deposit carries a raw/ tree of retrieved third party material
    # and search records. It is skipped and the skip is counted, because a hit
    # in somebody else's retrieved file is not a measurement by this deposit.
    out["ladder"] = sweep(a.ladder, neighbour.LADDER_TAG, "null-ladder",
                          skip_prefix="raw/")
    out["forced"] = sweep(a.forced, FORCED_TAG, "forced-counts")

    (core.ROOT / "results").mkdir(exist_ok=True)
    (core.ROOT / "results" / "prior-sweep.json").write_text(
        json.dumps(out, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("\nThe sweep locates. It does not decide. The verdict is in "
          "BACKGROUND-REVIEW.md and rests on reading, with the passages "
          "quoted there.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
