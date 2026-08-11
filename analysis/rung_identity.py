"""Is the family of this preregistration a family this lane owns.

It is not, and this module establishes that against the published deposit
rather than asserting it.

The background review resolved that the family defined in preregistration
section (b) coincides with rung P1 of the ladder deposited at
10.5281/zenodo.21750029. That deposit defines P1, in its own code, as the
arrangements that keep the thirty-two received pairs as pairs, in any order,
in either orientation, and gives its cardinal as thirty-two factorial times
two to the thirty-two.

Two things are checked here, both against the deposit read only at its tag:

  the cardinal this lane declared in its signed section (b) equals the
  cardinal that deposit computes and prints for P1,

  the definition that deposit gives for P1 is quoted, so a reader can see the
  two definitions side by side and judge the identity rather than take it.

The consequence is stated in RESULTS and governs everything after it: the
family is not new, it has a prior owner, it is cited, and the only thing this
lane does is measure a statistic on it that the prior work did not measure.

Usage:
    python analysis/rung_identity.py --ladder-checkout PATH
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import core
import neighbour

DECLARED_CARDINAL = math.factorial(32) * 2 ** 32


def run(checkout):
    out = {"declared_by_this_lane": str(DECLARED_CARDINAL)}

    orbit, orbit_digest = neighbour.read_at_tag(
        checkout, neighbour.LADDER_TAG, "orbit_from_sampler.py")
    orbit_text = orbit.decode("utf-8")
    out["orbit_from_sampler.py.sha256"] = orbit_digest

    m = re.search(r'"P1":\s*(math\.factorial\(32\)\s*\*\s*2\s*\*\*\s*32)',
                  orbit_text)
    out["deposit_expression_for_P1"] = m.group(1) if m else None
    print(f"the deposit computes its P1 cardinal as: "
          f"{out['deposit_expression_for_P1']}")

    graded, graded_digest = neighbour.read_at_tag(
        checkout, neighbour.LADDER_TAG, "graded_degeneracy.py")
    out["graded_degeneracy.py.sha256"] = graded_digest
    g = re.search(r'"P1":\s*([0-9.]+e[0-9]+)', graded.decode("utf-8"))
    printed = g.group(1) if g else None
    out["deposit_printed_cardinal"] = printed
    print(f"the deposit prints its P1 cardinal as:   {printed}")

    ours = f"{DECLARED_CARDINAL:.4e}".replace("e+", "e")
    theirs = printed.replace("e+", "e") if printed else None
    agree_printed = ours == theirs
    agree_exact = out["deposit_expression_for_P1"] is not None
    print(f"this lane declared, to the same precision: {ours}")
    print(f"printed cardinals agree: {'YES' if agree_printed else 'NO'}")
    print(f"the deposit's exact expression is the one this lane declared: "
          f"{'YES' if agree_exact else 'NO'}")

    containment, cont_digest = neighbour.read_at_tag(
        checkout, neighbour.LADDER_TAG, "ladder_containment.py")
    out["ladder_containment.py.sha256"] = cont_digest
    text = containment.decode("utf-8")
    start = text.index("def in_P1(arr):")
    quote = text[start:text.index('"""', text.index('"""', start) + 3) + 3]
    out["deposit_definition_of_P1"] = quote
    print("\nthe deposit's own definition of P1, quoted:")
    for line in quote.splitlines():
        print(f"  | {line}")

    out["agree_printed"] = agree_printed
    out["agree_exact_expression"] = agree_exact
    out["neighbour_branch_after_reading"] = neighbour.working_tree_untouched(checkout)
    return out, agree_printed and agree_exact


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ladder-checkout", required=True)
    a = ap.parse_args()
    result, ok = run(a.ladder_checkout)
    (core.ROOT / "results").mkdir(exist_ok=True)
    (core.ROOT / "results" / "rung-identity.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"\nrung identity: {'CONFIRMED' if ok else 'NOT CONFIRMED'}")
    sys.exit(0 if ok else 1)
