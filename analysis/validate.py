"""The sampler, validated by two independent routes before anything is read.

Preregistration section (c): "This is an analytic prediction stated in
advance. It is used as the acceptance test of the sampler, and the sampler is
not permitted to produce a single p-value until it reproduces it, together
with the exact mean and variance of W, within declared Monte Carlo
tolerance."

ROUTE A, analytic. Under F the mean of T is exactly 1008, the mean of W is
exactly 16 and the variance of W is exactly 8. The empirical values must
agree.

  Declared tolerance, fixed here before the run and not after it: four
  standard errors of the sample mean, the standard error taken from the
  sample's own dispersion. The signed document required a tolerance and did
  not fix a number; that gap is declared as a defect rather than filled
  quietly, and four standard errors is written down before the figures are
  looked at.

ROUTE B, against the published implementation. The family of this
preregistration is rung P1 of a deposited ladder. That deposit carries its
own membership predicate, written from its own printed definition. Every
draw of this sampler must satisfy it, this lane's independently written
predicate must agree with it draw for draw, and an object outside the family
must be refused by both.

  A reimplementation inherits the verifications of the original or declares
  why not. This is the inheritance.

If the two routes disagree, the run stops.

Usage:
    python analysis/validate.py --ladder-checkout PATH
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import core
import neighbour

SEED = 20260811           # preregistration section (g)
N_VALIDATION = 200_000
TOLERANCE_SE = 4.0        # declared above, before the run
N_PREDICATE = 2_000       # draws handed to the published predicate one by one


def route_a(rng):
    print("ROUTE A, the analytic acceptance test")
    perms, flips = core.draw(rng, N_VALIDATION)
    out = {"draws": N_VALIDATION, "tolerance_standard_errors": TOLERANCE_SE,
           "conventions": []}
    ok = True

    for c, (name, _) in enumerate(core.CONVENTIONS):
        d, K = core.block_tables(c)
        W, X = core.components(perms, flips, d, K)
        T = W + X
        mean_T, se_T = float(T.mean()), float(T.std(ddof=1) / np.sqrt(len(T)))
        mean_W, var_W = float(W.mean()), float(W.var(ddof=1))
        se_W = float(W.std(ddof=1) / np.sqrt(len(W)))
        pass_T = abs(mean_T - core.MEAN_T) <= TOLERANCE_SE * se_T
        pass_W = abs(mean_W - core.MEAN_W) <= TOLERANCE_SE * se_W
        pass_varW = abs(var_W - core.VAR_W) <= 0.1
        ok = ok and pass_T and pass_W and pass_varW
        print(f"  {name}")
        print(f"    mean of T {mean_T:.4f} against the analytic {core.MEAN_T}, "
              f"standard error {se_T:.4f}, "
              f"deviation {abs(mean_T - core.MEAN_T) / se_T:.2f} standard "
              f"errors: {'PASS' if pass_T else 'FAIL'}")
        print(f"    mean of W {mean_W:.4f} against {core.MEAN_W}, "
              f"variance of W {var_W:.4f} against {core.VAR_W}: "
              f"{'PASS' if pass_W and pass_varW else 'FAIL'}")
        out["conventions"].append({
            "convention": name, "mean_T": mean_T, "se_T": se_T,
            "deviation_in_se": abs(mean_T - core.MEAN_T) / se_T,
            "mean_W": mean_W, "var_W": var_W,
            "pass_T": pass_T, "pass_W": pass_W, "pass_var_W": pass_varW,
        })

    out["passed"] = ok
    print(f"  ROUTE A: {'PASS' if ok else 'FAIL'}")
    return out, ok


def route_b(rng, checkout):
    print("\nROUTE B, against the published predicate of rung P1")
    module, digest, scratch = neighbour.import_at_tag(
        checkout, neighbour.LADDER_TAG, "ladder_containment.py",
        "published_ladder")
    print(f"  read at the tag, sha256 {digest}")
    print(f"  executed from a scratch file outside this repository")

    out = {"predicate_source_sha256": digest, "checks": []}
    ok = True

    def record(label, passed, detail=""):
        nonlocal ok
        ok = ok and passed
        out["checks"].append({"check": label, "passed": passed, "detail": detail})
        print(f"  {'PASS' if passed else 'FAIL'}  {label}"
              + (f" ({detail})" if detail else ""))

    identity = tuple(range(core.N_POS))
    record("the received arrangement is in the family, by the published "
           "predicate", module.in_P1(identity))
    record("the received arrangement is in the family, by this lane's "
           "predicate", core.in_family(identity))

    perms, flips = core.draw(rng, N_PREDICATE)
    theirs = mine = roundtrip = assembled_same = 0
    for i in range(N_PREDICATE):
        arr = core.assemble(perms[i], flips[i])
        theirs += bool(module.in_P1(arr))
        mine += bool(core.in_family(arr))
        assembled_same += (arr == module.assemble(tuple(int(x) for x in perms[i]),
                                                  tuple(int(x) for x in flips[i])))
        p, f = module.decompose(arr)
        roundtrip += (list(p) == [int(x) for x in perms[i]]
                      and list(f) == [int(x) for x in flips[i]])
    record("every draw of this sampler satisfies the published predicate",
           theirs == N_PREDICATE, f"{theirs} of {N_PREDICATE}")
    record("every draw satisfies this lane's own predicate",
           mine == N_PREDICATE, f"{mine} of {N_PREDICATE}")
    record("the published assembly agrees with this lane's assembly",
           assembled_same == N_PREDICATE, f"{assembled_same} of {N_PREDICATE}")
    record("the published decomposition recovers the permutation and the "
           "orientations this sampler chose",
           roundtrip == N_PREDICATE, f"{roundtrip} of {N_PREDICATE}")

    # Objects outside the family. Each must be refused by both predicates.
    witnesses = []

    swapped = list(identity)
    swapped[0], swapped[2] = swapped[2], swapped[0]
    witnesses.append(("one hexagram exchanged across two blocks", tuple(swapped)))

    rotated = tuple(list(identity)[1:] + [identity[0]])
    witnesses.append(("the whole arrangement rotated by one position", rotated))

    free = tuple(rng.permutation(core.N_POS).tolist())
    witnesses.append(("a free shuffle of all sixty-four positions", free))

    within = list(identity)
    within[0], within[1] = within[1], within[0]
    witnesses.append(("a within-block flip, which IS in the family and must be "
                      "accepted by both", tuple(within)))

    for label, arr in witnesses:
        t, m = bool(module.in_P1(arr)), bool(core.in_family(arr))
        expected_in = "IS in the family" in label
        passed = (t == m) and (t == expected_in)
        record(f"witness, {label}", passed,
               f"published says {t}, this lane says {m}")

    out["passed"] = ok
    print(f"  ROUTE B: {'PASS' if ok else 'FAIL'}")
    return out, ok


def run(checkout):
    # Streams zero to three belong to the four conventions, in the declared
    # order. Stream four is the validation stream. Spawning a fifth child does
    # not alter the first four, and that is checked rather than assumed.
    four = core.streams(SEED, 4)
    five = core.streams(SEED, 5)
    same = all(np.array_equal(a.integers(0, 2 ** 31, 8),
                              b.integers(0, 2 ** 31, 8))
               for a, b in zip(four, five[:4]))
    print(f"spawning a validation stream leaves the four convention streams "
          f"unchanged: {'PASS' if same else 'FAIL'}")

    rng = core.streams(SEED, 5)[4]
    a_out, a_ok = route_a(rng)
    b_out, b_ok = route_b(rng, checkout)

    verdict = same and a_ok and b_ok
    print(f"\nBOTH ROUTES: {'PASS' if verdict else 'FAIL'}")
    if not verdict:
        print("The routes disagree or an acceptance test failed. The "
              "preregistration forbids reading a p-value from here.")
    return {"stream_independence": same, "route_a": a_out, "route_b": b_out,
            "passed": verdict}, verdict


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ladder-checkout", required=True)
    a = ap.parse_args()
    result, ok = run(a.ladder_checkout)
    (core.ROOT / "results").mkdir(exist_ok=True)
    (core.ROOT / "results" / "validation.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8", newline="\n")
    sys.exit(0 if ok else 1)
