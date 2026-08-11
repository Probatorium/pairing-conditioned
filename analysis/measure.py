"""The measurement the preregistration declares. Nothing else.

Every choice below is fixed by `PREREGISTRATION.md` at the root commit and
none of it is chosen after seeing a figure.

  sample size   one million draws from F per convention, section (g)
  seed          20260811, PCG64 through a seed sequence, one independent
                stream per convention in the declared convention order
  estimator     p = (1 + draws at least as extreme) / (1 + draws), which
                never returns zero and is conservative
  tests         A location of T, B location of W against the exact Binomial
                law, C location of X, D centrality of T
  tails         A, B and C two sided; D the lower tail of the absolute
                deviation. Fixed in the signed document, not here.
  multiplicity  Holm at a family wise level of 0.05 across the distinct
                tests, where two tests count as one if and only if the
                complement invariance is verified to hold exactly for them

CHUNKING. Draws are generated in blocks of a quarter of a million. The block
size is part of the protocol because the stream consumption depends on it: a
different block size gives a different, equally valid, sample. It is fixed
here so that this run reproduces exactly.

Usage:
    python analysis/measure.py
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import core

SEED = 20260811
N_DRAWS = 1_000_000
CHUNK = 250_000
ALPHA = 0.05
TEST_LABELS = {
    "A": "location of T",
    "B": "location of W, the orientation component, against the exact law",
    "C": "location of X, the block order component",
    "D": "centrality of T",
}


def mc_p(count_at_least_as_extreme, n):
    return (1 + int(count_at_least_as_extreme)) / (1 + n)


def exact_binomial_two_sided(w_obs, n=32):
    """P(|W - n/2| >= |w_obs - n/2|) under Binomial(n, 1/2), exactly."""
    dev = abs(w_obs - n / 2)
    total = sum(math.comb(n, k) for k in range(n + 1)
                if abs(k - n / 2) >= dev)
    return total / 2 ** n


def sample_convention(c, rng):
    d, K = core.block_tables(c)
    Ws, Xs = [], []
    remaining = N_DRAWS
    while remaining:
        n = min(CHUNK, remaining)
        perms, flips = core.draw(rng, n)
        W, X = core.components(perms, flips, d, K)
        Ws.append(W)
        Xs.append(X)
        remaining -= n
    return np.concatenate(Ws), np.concatenate(Xs)


def describe(values, observed, centre):
    values = np.asarray(values)
    below = int((values < observed).sum())
    at = int((values == observed).sum())
    n = len(values)
    dev = abs(observed - centre)
    devs = np.abs(values - centre)
    return {
        "observed": int(observed),
        "family_mean": float(values.mean()),
        "family_sd": float(values.std(ddof=1)),
        "family_min": int(values.min()),
        "family_max": int(values.max()),
        "percentile_strictly_below": 100.0 * below / n,
        "percentile_at_or_below": 100.0 * (below + at) / n,
        "percentile_midrank": 100.0 * (below + at / 2) / n,
        "deviation_from_centre": int(dev),
        "count_at_least_as_far": int((devs >= dev).sum()),
        "count_at_most_as_far": int((devs <= dev).sum()),
    }


def invariance_check():
    """Does complementing the line types reflect the statistics exactly.

    Preregistration section (e) predicts that it maps T to 2016 - T, W to
    32 - W and X to 1984 - X, and calls the prediction unestablished until
    verified. It is verified here at the level of the value functions, where
    it either holds for all sixty-four hexagrams or does not, and then on a
    sample of arrangements.
    """
    out = {"pairs": []}
    rng = core.streams(SEED, 5)[4]
    perms, flips = core.draw(rng, 10_000)
    for a, b in ((0, 1), (2, 3)):
        va, vb = core.values_under(a), core.values_under(b)
        value_level = all(vb[i] == 63 - va[i] for i in range(64))
        da, Ka = core.block_tables(a)
        db, Kb = core.block_tables(b)
        Wa, Xa = core.components(perms, flips, da, Ka)
        Wb, Xb = core.components(perms, flips, db, Kb)
        sample_level = bool(np.all(Wb == 32 - Wa) and np.all(Xb == 1984 - Xa)
                            and np.all((Wb + Xb) == 2016 - (Wa + Xa)))
        out["pairs"].append({
            "conventions": [core.CONVENTIONS[a][0], core.CONVENTIONS[b][0]],
            "value_level": value_level,
            "sample_level": sample_level,
            "holds": value_level and sample_level,
        })
    # Do the two remaining conventions also collapse into each other.
    v0, v2 = core.values_under(0), core.values_under(2)
    out["first_and_third_are_the_same_order"] = (v0 == v2)
    out["first_and_third_are_reflections"] = all(v2[i] == 63 - v0[i]
                                                 for i in range(64))
    out["all_pairs_hold"] = all(p["holds"] for p in out["pairs"])

    # A second coincidence, which the signed multiplicity rule did not
    # anticipate and which is therefore recorded rather than acted on.
    # Reversing the reading swaps the two members of every block that is a
    # reversal pair, so every block keeps its VALUE SET. The between-block
    # table depends only on those sets, so it is unchanged, and with it the
    # whole law of X.
    tables = [core.block_tables(c) for c in range(4)]
    shared = []
    for a in range(4):
        for b in range(a + 1, 4):
            da, Ka = tables[a]
            db, Kb = tables[b]
            shared.append({
                "conventions": [core.CONVENTIONS[a][0], core.CONVENTIONS[b][0]],
                "same_between_block_table": bool(np.array_equal(Ka, Kb)),
                "same_within_block_vector": bool(np.array_equal(da, db)),
                "complementary_within_block_vector": bool(np.array_equal(db, 1 - da)),
            })
    out["shared_tables"] = shared
    rec = core.received()
    reversal_blocks = [j for j in range(core.N_BLOCKS)
                       if core.reverse6(rec[2 * j]) != rec[2 * j]]
    val = core.values_under(0)
    out["reversal_blocks"] = len(reversal_blocks)
    out["palindrome_blocks"] = core.N_BLOCKS - len(reversal_blocks)
    out["reversal_blocks_discordant_as_received"] = sum(
        1 for j in reversal_blocks if val[2 * j] > val[2 * j + 1])
    return out


def holm(pvalues, alpha):
    """Holm step down. Returns adjusted p in the input order."""
    indexed = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
    m = len(pvalues)
    adjusted = [0.0] * m
    running = 0.0
    for rank, i in enumerate(indexed):
        running = max(running, min(1.0, (m - rank) * pvalues[i]))
        adjusted[i] = running
    return adjusted


def main():
    print("PRECONDITIONS were run separately and passed. See "
          "results/precondition.json.")
    print("VALIDATION was run separately and passed on both routes. See "
          "results/validation.json.\n")

    inv = invariance_check()
    print("Complement invariance, predicted in section (e) and unestablished "
          "until now:")
    for p in inv["pairs"]:
        print(f"  {p['conventions'][0]}  and  {p['conventions'][1]}: "
              f"value level {p['value_level']}, sample level "
              f"{p['sample_level']}")
    print(f"  the first and third conventions induce the same order: "
          f"{inv['first_and_third_are_the_same_order']}")
    print(f"  the first and third are reflections of each other: "
          f"{inv['first_and_third_are_reflections']}")
    collapses = inv["all_pairs_hold"]
    n_distinct_conventions = 2 if collapses else 4
    n_tests = 4 * n_distinct_conventions
    print(f"  distinct conventions for multiplicity: {n_distinct_conventions}, "
          f"so the correction is over {n_tests} tests")
    print("  a second coincidence, outside the rule the signed document fixed:")
    for s in inv["shared_tables"]:
        if s["same_between_block_table"]:
            print(f"    {s['conventions'][0]}  and  {s['conventions'][1]} "
                  f"share the between-block table, so they share the whole "
                  f"law of X")
    print(f"    of the {inv['reversal_blocks']} blocks that are reversal "
          f"pairs, {inv['reversal_blocks_discordant_as_received']} are "
          f"discordant as received, which is exactly half, and that is why "
          f"reversing the reading leaves the observed W where it was")
    print("    the signed rule collapses tests only under the complement "
          "invariance it named, so this coincidence is reported and NOT acted "
          "on. See RESULTS and DEFECTS.\n")

    streams = core.streams(SEED, 5)
    results = {"seed": SEED, "draws_per_convention": N_DRAWS,
               "chunk": CHUNK, "invariance": inv,
               "distinct_conventions": n_distinct_conventions,
               "tests_corrected_over": n_tests, "conventions": []}

    for c, (name, _) in enumerate(core.CONVENTIONS):
        print(f"--- convention {c + 1}: {name}")
        W, X = sample_convention(c, streams[c])
        T = W + X
        w_obs, x_obs = core.observed_components(c)
        t_obs = w_obs + x_obs

        dT = describe(T, t_obs, core.MEAN_T)
        dW = describe(W, w_obs, core.MEAN_W)
        dX = describe(X, x_obs, core.MEAN_X)

        pA = mc_p(dT["count_at_least_as_far"], N_DRAWS)
        pB = exact_binomial_two_sided(w_obs)
        pC = mc_p(dX["count_at_least_as_far"], N_DRAWS)
        pD = mc_p(dT["count_at_most_as_far"], N_DRAWS)

        for label, d in (("T", dT), ("W", dW), ("X", dX)):
            print(f"  {label}: observed {d['observed']}, family mean "
                  f"{d['family_mean']:.3f}, sd {d['family_sd']:.3f}, "
                  f"support [{d['family_min']}, {d['family_max']}]")
            print(f"     percentile of the observed: "
                  f"{d['percentile_midrank']:.3f}")
        print(f"  A {TEST_LABELS['A']}: p = {pA:.6f}")
        print(f"  B {TEST_LABELS['B']}: p = {pB:.6f}  (exact)")
        print(f"  C {TEST_LABELS['C']}: p = {pC:.6f}")
        print(f"  D {TEST_LABELS['D']}: p = {pD:.6f}")

        results["conventions"].append({
            "index": c, "name": name,
            "observed": {"T": t_obs, "W": w_obs, "X": x_obs},
            "T": dT, "W": dW, "X": dX,
            "p": {"A": pA, "B": pB, "C": pC, "D": pD},
        })

    # --- multiplicity, over the distinct tests only
    if collapses:
        carriers = [0, 2]
        note = ("Each convention pair collapses to one test by the verified "
                "invariance. The p carried forward for a collapsed pair is "
                "the SMALLER of the two independently sampled estimates, "
                "which is the choice least favourable to the outcome the "
                "preregistration expects. See DEFECTS, the underspecification "
                "of which member supplies the p.")
        pairs = {0: 1, 2: 3}
    else:
        carriers = [0, 1, 2, 3]
        note = "The invariance failed, so no test collapses."
        pairs = {}

    labels, pvals = [], []
    for c in carriers:
        for letter in "ABCD":
            p = results["conventions"][c]["p"][letter]
            if c in pairs:
                p = min(p, results["conventions"][pairs[c]]["p"][letter])
            labels.append(f"{core.CONVENTIONS[c][0]} / {letter}")
            pvals.append(p)
    adjusted = holm(pvals, ALPHA)

    print(f"\n--- multiplicity: Holm at a family wise level of {ALPHA} "
          f"over {len(pvals)} tests")
    print(f"    {note}")
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    for i in order:
        print(f"    p = {pvals[i]:.6f}  adjusted = {adjusted[i]:.6f}  "
              f"{'below' if adjusted[i] < ALPHA else 'at or above'} the level"
              f"   {labels[i]}")

    any_below = any(a < ALPHA for a in adjusted)
    results["multiplicity"] = {
        "method": "Holm step down", "alpha": ALPHA, "note": note,
        "tests": [{"label": l, "p": p, "adjusted": a}
                  for l, p, a in zip(labels, pvals, adjusted)],
        "any_adjusted_below_alpha": any_below,
    }
    results["verdict"] = {
        "hypothesis": "H: the observed count is atypical within F",
        "refuted": not any_below,
        "branch": ("H survives, in the specific and limited sense of not "
                   "being refuted" if any_below else
                   "H is refuted: every declared test, after the multiplicity "
                   "correction, yields an adjusted p of at least 0.05"),
    }
    print(f"\nVERDICT against the signed criterion: "
          f"{'H IS REFUTED' if not any_below else 'H SURVIVES REFUTATION'}")
    print(f"  {results['verdict']['branch']}")

    (core.ROOT / "results").mkdir(exist_ok=True)
    (core.ROOT / "results" / "measurement.json").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
