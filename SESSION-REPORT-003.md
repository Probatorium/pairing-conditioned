# Rigour report, session three

Session identifier: S003. Date: 2026-08-11. Scope as instructed: run the
measurement the preregistration declares.

The measurement was run. The full result, with the restatement of what the
signed document fixes and the verdict against its criterion, is in
`RESULTS.md`. This report is the rigour record around it and does not repeat
it.

Following the practice from defect three: this report enumerates the commits
of the session, and the commit that carries this report is not among them.

---

## Opening state

Head `e19cad1`, working tree clean, nothing pending, local and remote in
agreement, all gates passing.

The signed text was checked before anything else: `PREREGISTRATION.md` is the
same blob at the head as at the root commit, `eb62ce3`, and exactly one
commit in the history has ever touched it. The signature holds.

## What was run, in order

The order was not chosen afterwards and it matters.

1. The precondition gate, which the signed document declared as able to stop
   the lane, and which session two deliberately left for the analysis. Both
   preconditions passed.
2. The identity of the family against the deposit that owns it, read only at
   its tag.
3. The two validations of the sampler, both passed, before any p-value was
   read.
4. The analysis code committed, before the measurement was looked at.
5. The measurement.
6. The verdict taken against the signed criterion.

## The result, in one paragraph

Every one of the eight declared tests, after the correction the signed rule
fixes, yields an adjusted p at or above the declared level. The first branch
of the refutation criterion is the one that was met: the hypothesis that the
observed count is atypical within its family is refuted. The observed count
sits near the middle of its family. The document said in advance that this
was the outcome it expected and wrote down what would have had to be true for
the other branch; the advance bound it recorded held. The verdict is the same
under no correction at all, so it does not turn on how many tests were
counted.

## The family is not this lane's

Verified, not assumed. The deposit at 10.5281/zenodo.21750029 defines the
same object, by the same definition, and computes its cardinal by the same
expression this lane declared in its signed section. That deposit came first.
Every artefact of this lane cites it and none describes the family as
introduced here.

## Preconditions and validations

| check | outcome |
| --- | --- |
| P1, adjacency pairing equals the matching of the cited theorem | PASS, symmetric difference empty |
| decomposition against a direct count, all four conventions | PASS, added because an unchecked decomposition is an assumption |
| P2, recomputed observed statistic against the prior lane | PASS, two conventions reproduce the reported value |
| route A, the analytic acceptance test | PASS, worst deviation 1.37 standard errors |
| route B, against the published predicate of the rung | PASS, every draw accepted, both predicates agreeing on four witnesses |

Route B is the inheritance the rules require: a reimplementation inherits the
verifications of the original or declares why not. It inherited them, by
being handed to the original's own predicate rather than by resembling it.

## Defects declared this session

Three, all in `DEFECTS.md`, none of them reinterpreted into something
harmless.

- **Five**, the signed document required an acceptance tolerance and fixed no
  number. One was fixed in the code before the run. The cost is recorded
  honestly: a tolerance chosen in the session that uses it is weaker than one
  chosen in advance, and the fact that no plausible threshold would have
  changed the outcome is luck rather than design.
- **Six**, the multiplicity rule did not say which member of a collapsed pair
  supplies the p. The smaller was taken, being least favourable to the
  expected outcome.
- **Seven**, a second collapse exists that the signed rule did not anticipate:
  reversing which end carries the most significant bit leaves every block's
  value set intact and therefore leaves the whole law of the block order
  component unchanged. The genuine number of distinct tests is four where the
  rule computes eight. The rule says no other value is permitted, so the
  correction was run over eight and the finding was reported and not acted
  on. Acting on it would have eased refutation, which is the direction the
  document expected, and the rule keeps its value only if it is followed when
  it is inconvenient in that direction.

## The figure gate, used in earnest for the first time

The registry held every figure as cited and unverified through two sessions,
so no commit message could carry one. The measurement changed that for three
of them, and the gate gained the one mechanism it was missing: a cited record
is retired by a record that names its exact token and object, so a figure
moves from cited to measured without anything being deleted and without a
retirement that could be guessed.

The commit that carries the measurement is the first in this repository
allowed a figure, and the gate passed it while still refusing the figures of
the prior lane whose objects this lane never measured.

## State of the chain, sweeps and gates

- Effort log: chain intact, thirty-two entries at the time of writing, nine
  added this session, session structure sound.
- Dash sweep: working tree clean, every blob of every commit clean.
- Untouchable gate: passing across tree, remotes, config and history.
- Pre publication sweep: run before the push, as the practice from defect
  four requires and not only on the first push. It reports the same two
  occurrences it reported in session two, which are the accepted and declared
  residue of defect four, and nothing new.

## Commits of this session

Two, not counting the commit that carries this report.

- `42cb727` the analysis apparatus, the preconditions, and a sampler
  validated twice
- `e39b9bf` the measurement

Pushed, local and remote heads in agreement at each push.

## What is pending, and belongs to Alexis

1. **The rename on the forge.** Still not made. `matching-conditioned` does
   not resolve; the repository is still published under its old name. The
   adopted name is in every artefact that names it. When the rename happens
   the remote address is adjusted and verified, one command.
2. **The background review.** Now opened, not closed. One item is resolved,
   that the family is prior. What that does not settle is whether the
   measurement is prior, and nobody has read the appendix that carries that
   ladder. Until somebody does, this lane claims nothing about novelty in
   either direction. This is the recommendation for session four.
3. **Deposit and tagging.** Not authorised, not done, not requested.
4. **The rule that finding seven exposed.** If this design is reused, its
   multiplicity rule needs stating properly, because it anticipated one of
   the two collapses that exist. That is a decision about a future lane, not
   about this one, whose signed text stands.

## What is not claimed

Nothing about design, intention or ancient knowledge. No novelty of anything
while the background review is unclosed. Nothing from the unpublished lane is
cited, and the gate that enforces that ran on every commit of this session.
