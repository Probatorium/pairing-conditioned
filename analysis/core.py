"""The objects the preregistration defines, and nothing else.

Every definition here is fixed by `PREREGISTRATION.md` at the root commit.
Where this file makes a choice the signed document did not force, it says so
in a comment. Nothing here reads a result.

The received sequence is loaded from `data/king-wen-received.json`, which is
received data and is never recomputed. See `THIRD-PARTY-MANIFEST.md`.

REPRESENTATION. The received sequence has sixty-four positions. Position i
carries King Wen number i plus one. Positions 2j and 2j+1 are block j, so
there are thirty-two blocks. An arrangement is a tuple `arr` of length
sixty-four where `arr[k]` is the received position now sitting at output
position k. This is the same representation the published rung uses, which
is deliberate: it is what allows a sample of this lane to be handed to that
rung's own predicate without translation.
"""

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
N_POS = 64
N_BLOCKS = 32
N_PAIRS_TOTAL = 2016      # C(64, 2), the number of unordered pairs compared
N_WITHIN = 32             # one comparison per block
N_BETWEEN = 1984          # 4 * C(32, 2)
MEAN_T = 1008             # analytic, preregistration section (c)
MEAN_W = 16
MEAN_X = 992
VAR_W = 8.0


def received():
    """The received King Wen sequence: received position to hexagram value."""
    payload = json.loads((ROOT / "data" / "king-wen-received.json")
                         .read_text(encoding="utf-8"))
    values = payload["values"]
    assert len(values) == N_POS and len(set(values)) == N_POS
    return values


# --- the six lines, as figures -------------------------------------------
# The received values encode the six lines with the bottom line as the most
# significant bit and the solid line as one, which is what the source states.
# Reversal is turning the figure upside down; complement is changing every
# line. Both are properties of the figure and neither depends on how the
# figure is read as a number.

def reverse6(v):
    return int(format(v, "06b")[::-1], 2)


def complement6(v):
    return v ^ 63


# --- the four bit conventions, in the declared order ----------------------
# Preregistration section (c): "bottom-significant with solid as one;
# bottom-significant with solid as zero; top-significant with solid as one;
# top-significant with solid as zero." The order below is that order and is
# not to be reordered.

CONVENTIONS = [
    ("bottom-significant, solid as one", lambda v: v),
    ("bottom-significant, solid as zero", lambda v: complement6(v)),
    ("top-significant, solid as one", lambda v: reverse6(v)),
    ("top-significant, solid as zero", lambda v: complement6(reverse6(v))),
]


def values_under(convention_index):
    """Value of each received position under one convention."""
    _, f = CONVENTIONS[convention_index]
    return [f(v) for v in received()]


# --- the matching M, from the cited theorem -------------------------------

def radisic_matching():
    """M by the reverse priority rule of Radisic (2026), arXiv 2601.07175.

    "pair each element with its reversal unless it is a palindrome, in which
    case pair with its complement". Taken from that source as given. This
    lane does not reprove it.
    """
    pairs = set()
    for v in range(64):
        r = reverse6(v)
        partner = complement6(v) if r == v else r
        pairs.add(frozenset((v, partner)))
    return pairs


def adjacency_pairing():
    """The pairing the received sequence itself exhibits, as a set partition."""
    rec = received()
    return {frozenset((rec[2 * j], rec[2 * j + 1])) for j in range(N_BLOCKS)}


# --- the statistic and its decomposition ----------------------------------

def inversions(sequence):
    """Discordant pairs of a sequence of distinct values, counted directly.

    Sixty-four elements, so the quadratic count is exact and fast enough. It
    is used to check the decomposition rather than to replace it.
    """
    n = len(sequence)
    return sum(1 for i in range(n) for j in range(i + 1, n)
               if sequence[i] > sequence[j])


def T_of(arr, convention_index):
    """T for an arrangement, computed directly from its definition."""
    val = values_under(convention_index)
    return inversions([val[k] for k in arr])


def block_tables(convention_index):
    """The two tables the decomposition needs, for one convention.

    d[j]  1 if block j in its received orientation puts the larger value
          first, that is if the within-block comparison is discordant as
          received. Preregistration section (c): exactly one of the two
          orientations is discordant, so the other is d[j] flipped.

    K[p][q]  the number of the four cross comparisons between block p and
          block q that are discordant when p is placed before q. Untouched by
          orientation, again by section (c).
    """
    val = values_under(convention_index)
    d = np.array([1 if val[2 * j] > val[2 * j + 1] else 0
                  for j in range(N_BLOCKS)], dtype=np.int8)
    K = np.zeros((N_BLOCKS, N_BLOCKS), dtype=np.int8)
    for p in range(N_BLOCKS):
        pv = (val[2 * p], val[2 * p + 1])
        for q in range(N_BLOCKS):
            if p == q:
                continue
            qv = (val[2 * q], val[2 * q + 1])
            K[p, q] = sum(1 for a in pv for b in qv if a > b)
    return d, K


def observed_components(convention_index):
    """W and X of the received arrangement itself, by the decomposition."""
    d, K = block_tables(convention_index)
    # Both tables are int8 because the sampler wants them small. Accumulate in
    # Python integers: 496 entries of an int8 array overflow a naive sum, and
    # that overflow is silent.
    W = int(d.astype(np.int64).sum())
    X = int(K.astype(np.int64)[np.triu_indices(N_BLOCKS, k=1)].sum())
    return W, X


# --- membership, this lane's own test -------------------------------------

def in_family(arr):
    """True if arr realises the received pairing.

    Written from the preregistration's own definition of F in section (b),
    independently of any other implementation, so that agreement with the
    published rung's predicate is evidence rather than tautology.
    """
    if sorted(arr) != list(range(N_POS)):
        return False
    for j in range(N_BLOCKS):
        a, b = arr[2 * j], arr[2 * j + 1]
        if a // 2 != b // 2 or a == b:
            return False
    return True


def assemble(perm, flips):
    """An arrangement from a block permutation and an orientation vector."""
    out = []
    for j in range(N_BLOCKS):
        a, b = 2 * int(perm[j]), 2 * int(perm[j]) + 1
        out += [b, a] if flips[j] else [a, b]
    return tuple(out)


# --- the sampler ----------------------------------------------------------

def streams(seed, count):
    """One independent stream per convention, in the declared order.

    Preregistration section (g): "The generator is the PCG64 bit generator,
    seeded from a seed sequence on that integer, with one independent stream
    spawned per convention in the declared convention order."
    """
    children = np.random.SeedSequence(seed).spawn(count)
    return [np.random.Generator(np.random.PCG64(c)) for c in children]


def draw(rng, n):
    """n uniform members of F, as block permutations and orientation vectors.

    Both free choices are sampled exactly: a uniform permutation of thirty-two
    objects, and thirty-two independent fair bits. No rejection, no
    approximation, no burn-in.
    """
    perms = np.tile(np.arange(N_BLOCKS, dtype=np.int8), (n, 1))
    perms = rng.permuted(perms, axis=1)
    flips = rng.integers(0, 2, size=(n, N_BLOCKS), dtype=np.int8)
    return perms, flips


def components(perms, flips, d, K):
    """W and X for a batch of draws, by the decomposition of section (c)."""
    W = (d[np.newaxis, :] ^ flips).sum(axis=1).astype(np.int32)
    n = perms.shape[0]
    X = np.zeros(n, dtype=np.int32)
    flat = K.astype(np.int32).ravel()
    left = perms.astype(np.int32) * N_BLOCKS
    for i in range(N_BLOCKS - 1):
        li = left[:, i]
        for j in range(i + 1, N_BLOCKS):
            X += flat[li + perms[:, j]]
    return W, X
