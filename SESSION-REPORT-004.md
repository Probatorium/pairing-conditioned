# Rigour report, session four

Session identifier: S004. Date: 2026-08-11. Scope as instructed: close the
background review on the one question it had left. Nothing measured.

Following the practice from defect three: this report enumerates the commits
of the session, and the commit that carries this report is not among them.

---

## Opening state

Head `cec26bf`, working tree clean, gates passing, local and remote in
agreement.

## The question, and when it was fixed

Written into the effort log, entry thirty-five, before a single file was
opened: does either work measure, on rung P1 or on any rung, the count of
discordant pairs of the King Wen sequence against the binary order, or any
quantity from which that count follows. Two subsidiary questions were fixed at
the same moment. None of the three was adjusted after reading.

That ordering is the whole methodological content of this session. A question
fixed after the reading is a question shaped by it.

## What was read, and how

Read entire, as artefacts, and only at their deposit tags, with no working
tree of any neighbour moved:

- the whole of Appendix A of `kingwen-orderings-replication` at `zenodo-v3`,
  both the prose and the code that produces its table,
- the section of the same paper that defines the pair-preserving null and the
  four signatures carried across the ladder,
- the results section of the same paper that reports the counts against the
  binary order,
- the ladder material of `null-ladder` at its deposit tag, its abstract, its
  containment module and every passage its own files flag with the vocabulary
  of the statistic,
- the passage of `forced-counts` at `zenodo-v1` that names this lane's
  question and declines it.

## The sweep

Term groups declared in `analysis/prior_sweep.py` before the counts were seen,
run over every text file at the three tags, output in
`results/prior-sweep.json`.

| deposit | files swept | statistic vocabulary | conditional family vocabulary | files where both occur |
| --- | --- | --- | --- | --- |
| kingwen-orderings-replication | 7 | 106 | 322 | 5 |
| null-ladder | 45, with 9 skipped | 58 | 1982 | 8 |
| forced-counts | 66 | 386 | 191 | 6 |

The skip is counted and stated: the ladder deposit carries a tree of retrieved
third party material and search records, and a hit inside somebody else's
retrieved file is not a measurement by that deposit.

Every one of the nineteen co-occurrence files was opened. The sweep locates;
it does not decide. The verdict rests on the reading and quotes it.

## The verdict

**The measurement was not prior in what was read.** The ladder carries four
signatures across its six rungs, named in its own caption as mean transition
distance, lag-1 autocorrelation of distances, yang-balanced groups of four,
and within/between-pair asymmetry. The deposited code agrees: its frozen table
has exactly those four keys per rung. The discordance count against the binary
order is not among them, on P1 or on any rung.

**Two things that are prior, and they matter.** The observed counts were
already published in all four conventions, value for value as this lane
recomputed them. And the count was already located inside a null, the
unrestricted one, and reported there as ordinary at 0.06 standard deviations
from an expectation of 1008.

**The qualification, recorded beside the verdict and not beneath it.** The
unrestricted null and rung P1 share their centre exactly and differ only in
dispersion, 86.3 against the 80.450 measured here. A published result
therefore already indicated what this lane would find. This lane confirmed it
rather than discovered it. That sentence is in `BACKGROUND-REVIEW.md`, in
`RESULTS.md` beside the result itself, and in the commit message.

**The limits, written because they are the point.** Three deposits by one
author are not the literature. No journal, no database and no work by anybody
else was searched for this question. Absence there is absence there.

**No novelty is claimed, of anything.** The review status line still says
OPENED and not CLOSED, because scope items one to five are untouched.

## Contact rules

Every read was at a tag. After the session, each neighbour is on the branch it
was on before. Nothing was copied in. Nothing from the untouchable lane was
read, named or cited, and the gate that enforces that ran on every commit.

## State of the chain, sweeps and gates

- Effort log: chain intact, forty entries at close, six added this session,
  session structure sound.
- Dash sweep: working tree clean, every blob of every commit clean.
- Untouchable gate: passing across tree, remotes, config and history.
- Figure gate: three figures usable, the rest still refused. The commit
  message of this session carries no figure.
- Pre publication sweep: run before the push. Same two occurrences as before,
  the accepted residue of defect four, nothing new.

## Commits of this session

One, not counting the commit that carries this report.

- `2461105` the verdict of the review, with its qualification and its limits

## What is pending, and belongs to Alexis

1. **Whether to deposit at all.** This is now the real decision and the review
   has put the material for it on the table. The lane has a clean result: a
   preregistered refutation, run against a signed criterion, on a family whose
   ownership is declared, with a sampler validated against the original's own
   predicate. It also has a small increment: the published free-null result
   already indicated the answer. Deposit as a short note, fold it into the
   lane that owns the ladder, or leave it standing in the repository as a
   verified negative. This report does not recommend one; it makes sure the
   decision is made with the deflation visible rather than after it.
2. **The rename on the forge.** Still not made. `matching-conditioned` does
   not resolve.
3. **The rest of the background review.** Items one to five unstarted. Until
   they are done, no artefact of this lane may claim novelty of anything, and
   that includes anything prepared for deposit.
4. **The multiplicity rule that finding seven exposed**, if this design is
   ever reused.

## What is not claimed

Nothing about design, intention or ancient knowledge. No novelty. Nothing from
the unpublished lane is cited.
