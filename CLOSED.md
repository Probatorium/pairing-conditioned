# Closing act

Decision by Alexis Garcia Hurtado, 2026-08-11: this lane does not deposit.

This file records what was asked, what was measured, why nothing is
deposited, what the background review settled and what it did not, and what
may be said about this repository elsewhere. It records nothing else.

---

## What was asked, and what was preregistered

The question: where does the observed count of discordant pairs of the King
Wen sequence against the binary order fall within the distribution of that
count over the family of sequences that realise the King Wen pairing.

The preregistration is `PREREGISTRATION.md`. It is the entire content of the
root commit of this repository, `f89b79918497ba60a4ad1dcc785800f8a17edb00`,
dated 2026-08-11. It fixes the family, the statistic, the four bit
conventions, the four tests and their tails, the sample size, the seed, the
multiplicity correction and the refutation criterion, all before any quantity
of the family was computed.

That text was never amended. Its blob is
`eb62ce33171d3356f4c259c004951c9cee837b5e` at the root commit and the same
blob at the head, and exactly one commit in the history has ever touched it.

## What was measured, and what came out

Under the convention with the bottom line most significant and the solid line
as one:

| quantity | value |
| --- | --- |
| observed count | 1013 |
| family mean | 1007.985 |
| family standard deviation | 80.450 |
| percentile of the observed count | 52.449 |

One million draws per convention, seed 20260811, on all four conventions. The
preconditions of the signed document passed. The sampler was validated against
the analytic mean and against the published membership predicate of the family
it samples.

The signed criterion reads: "H is refuted if every one of the declared tests,
after the multiplicity correction of section (e), yields an adjusted p of at
least 0.05." Every one of the eight declared tests did. The smallest adjusted
p is 0.426112. The criterion was met in its first branch: H, that the observed
count is atypical within the family, is refuted.

Full result in `RESULTS.md`, raw output in `results/`.

## Why nothing is deposited

Prior deposits by the same author already carry both halves of what this lane
measured.

The observed counts, in all four conventions, are published in `forced-counts`
at tag `zenodo-v1`, DOI 10.5281/zenodo.21889328, in
`paper/06-three-historical-orderings.md`:

> "The count is 1013 under the two conventions that read yang as one, and
> 1003 under the two that read yang as zero."

The placement of that count inside a null is published in
`kingwen-orderings-replication` at tag `zenodo-v3`, in `paper.tex`, Result
3.1:

> "The Kendall inversion counts between the historical orderings and the
> binary ordering are: King Wen 1013, Mawangdui 1008, Jing Fang 1008, out of a
> maximum of 2016. The random expectation is exactly 1008, with standard
> deviation 86.3. All three counts lie within 0.06 standard deviations of the
> expectation"

That null is the unrestricted one. This lane's null is the pairing conditioned
family. The two share their centre exactly, 1008, and differ in dispersion:
86.3 there, 80.450 here. This lane therefore confirms under a narrower null
what the published work states under a wider one, and changes no conclusion of
it.

That is the reason. There is no other.

## What the background review settled, and what it did not

Closed for one question only: whether this measurement had been made before.
It had not, in the three deposits that were read. The verdict, its pointers
and its verbatim quotations are in `BACKGROUND-REVIEW.md`.

The limits of that closing are part of it. Three deposits by one author are
not the literature. No journal, no database and no work by anybody else was
searched. Absence in what was read is absence in what was read.

Items one to five of the review's own scope are unstarted.

## What may be said about this repository elsewhere

Nothing in this repository is cited in any work.

No novelty is claimed, of the question, of the family, of the statistic, of
the analytic result, of the decomposition, or of any figure. The family is
rung P1 of the ladder deposited at DOI 10.5281/zenodo.21750029 and belongs to
that deposit.

Nothing is claimed about design, intention, or the knowledge of anyone.

## State at closing

This repository stays as it is. It is not deleted, its history is not
rewritten, and the neighbours it read remain untouched at their tags.
