"""The precondition gate of preregistration section (d).

    "Before any test is run, two facts are checked and the outcome is
    reported whatever it is:

     - P1. The adjacency pairing of the received King Wen sequence equals M
       as a set partition.
     - P2. The observed statistic recomputed here from primary data agrees
       with the value reported by the prior lane.

     If P1 fails, the family F as defined in (b) is not the family that
     conditions on the King Wen pairing, the design of this document does not
     apply, the failure is reported as the result of the lane, and no test
     below is run or reported. If P2 fails, the discrepancy is reported and
     this lane's own recomputed value, not the prior value, is the one
     carried forward."

This module runs both and returns a verdict. It runs no test and reads no
family quantity.

Usage:
    python analysis/precondition.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import core

PRIOR_REPORTED_T = 1013   # from the prior lane, cited-unverified until P2 runs


def run():
    out = {}

    # --- P1
    got = core.adjacency_pairing()
    want = core.radisic_matching()
    p1 = got == want
    out["P1"] = {
        "passed": p1,
        "blocks_in_adjacency_pairing": len(got),
        "blocks_in_matching": len(want),
        "in_adjacency_not_in_matching": sorted(sorted(p) for p in (got - want)),
        "in_matching_not_in_adjacency": sorted(sorted(p) for p in (want - got)),
    }
    print(f"P1 adjacency pairing equals the matching of the cited theorem: "
          f"{'PASS' if p1 else 'FAIL'}")
    print(f"   blocks in each: {len(got)} and {len(want)}, "
          f"symmetric difference: {len(got ^ want)}")
    if not p1:
        print("   P1 has failed. The design of the preregistration does not "
              "apply and no test is run or reported.")
        return out, False

    # --- consistency of the decomposition against the direct count
    identity = tuple(range(core.N_POS))
    checks = []
    for c, (name, _) in enumerate(core.CONVENTIONS):
        direct = core.T_of(identity, c)
        W, X = core.observed_components(c)
        checks.append({"convention": name, "T_direct": direct,
                       "W": W, "X": X, "W_plus_X": W + X,
                       "agrees": direct == W + X})
        print(f"   decomposition check, {name}: direct {direct}, "
              f"W plus X {W + X}, "
              f"{'agree' if direct == W + X else 'DISAGREE'}")
    out["decomposition_check"] = checks
    if not all(c["agrees"] for c in checks):
        print("   the decomposition disagrees with the direct count; stopping")
        return out, False

    # --- P2
    observed = {name: core.T_of(identity, c)
                for c, (name, _) in enumerate(core.CONVENTIONS)}
    matching = [n for n, v in observed.items() if v == PRIOR_REPORTED_T]
    p2 = bool(matching)
    out["P2"] = {
        "passed": p2,
        "prior_reported": PRIOR_REPORTED_T,
        "recomputed": observed,
        "conventions_reproducing_the_prior_value": matching,
    }
    print(f"P2 recomputed observed statistic agrees with the prior lane: "
          f"{'PASS' if p2 else 'FAIL'}")
    for name, v in observed.items():
        mark = "  <- reproduces the prior value" if v == PRIOR_REPORTED_T else ""
        print(f"   {name}: {v}{mark}")
    if not p2:
        print("   No convention reproduces the value the prior lane reported. "
              "The discrepancy is reported and this lane carries forward its "
              "own recomputed values, as the preregistration requires.")

    return out, True


if __name__ == "__main__":
    result, ok = run()
    (core.ROOT / "results").mkdir(exist_ok=True)
    (core.ROOT / "results" / "precondition.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    sys.exit(0 if ok else 1)
