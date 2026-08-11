# Background review

## Status: OPENED, NOT CLOSED

Opened in session three by one finding, which is resolved. Everything else in
the scope below is still unstarted. The standing prohibition remains in force
until the status line says CLOSED.

### Resolved: the family of this preregistration is not this lane's

The family defined in preregistration section (b) is rung P1 of the ladder
deposited at 10.5281/zenodo.21750029. That deposit defines the rung as "a
conditional null that permutes the 32 pairs and flips orientations within
them", "the uniform distribution over all pair-preserving rearrangements",
and computes its cardinal by the same expression this lane declared in its
signed section. Verified against the deposit read only at its tag, in
`analysis/rung_identity.py`, with the output in `results/rung-identity.json`.

The consequence is binding and is written into `RESULTS.md`: the family is
cited, never presented as introduced here. What this lane did was measure on
it a statistic the prior work did not measure.

What this does NOT settle is scope item six below. That the family was prior
does not tell us whether the measurement was. That question is settled in the
next section.

### Resolved: was the measurement prior

**Question, fixed in the effort log of session four before a single file was
read, and not adjusted afterwards.** Does either work measure, on rung P1 or
on any rung, the count of discordant pairs of the King Wen sequence against
the binary order, or any quantity from which that count follows.

**What was read, in full, as artefacts and only at their tags.** The whole of
Appendix A of `kingwen-orderings-replication` at `zenodo-v3`, in the paper and
in the code that produces its table; the section that defines the
pair-preserving null and the four signatures it carries; the results section
that reports the counts against the binary order; the ladder material of
`null-ladder` at its deposit tag, including its abstract, its containment
module and every passage its own files flag with the vocabulary of the
statistic; and the passage of `forced-counts` at `zenodo-v1` that names this
lane's question.

**The term sweep.** Declared groups, run over every text file at the three
tags, counts in `results/prior-sweep.json` and reproducible by
`analysis/prior_sweep.py`. Totals for the statistic vocabulary and the
conditional family vocabulary respectively: kingwen 106 and 322 over seven
files, null-ladder 58 and 1982 over forty-five files with nine skipped under
its retrieved third party tree, forced-counts 386 and 191 over sixty-six
files. Files where both vocabularies co-occur, which is the only place the
measurement could have been hiding: five, eight and six. Every one of them was
opened.

**Verdict: the measurement was not prior. The statistic was, and so was its
evaluation against a different null.** The three findings, with pointers:

1. *The statistic and its observed values are prior, in all four conventions.*
   `forced-counts` at `zenodo-v1`, `paper/06-three-historical-orderings.md`,
   records `inv.KingWen.yang1.bottomMSB`, `inv.KingWen.yang1.bottomLSB`,
   `inv.KingWen.yang0.bottomMSB` and `inv.KingWen.yang0.bottomLSB`, and says:

   > "The count is 1013 under the two conventions that read yang as one, and
   > 1003 under the two that read yang as zero."

   Those are, value for value, the four observed counts this lane recomputed.
   Its recomputation stands as a check, not as a first.

2. *An inferential evaluation of that count is prior, against the free null.*
   `kingwen-orderings-replication` at `zenodo-v3`, `paper.tex`, Result 3.1:

   > "The Kendall inversion counts between the historical orderings and the
   > binary ordering are: King Wen 1013, Mawangdui 1008, Jing Fang 1008, out
   > of a maximum of 2016. The random expectation is exactly 1008, with
   > standard deviation 86.3. All three counts lie within 0.06 standard
   > deviations of the expectation"

   That is the count located inside a null. The null is the unrestricted one.

3. *No evaluation of that count under P1, or under any rung, exists in what
   was read.* Appendix A states its own scope:

   > "We re-evaluate the four signatures of Table~\ref{tab:chan} under a
   > ladder of six nulls ordered by containment"

   and names them in its caption: "mean transition distance, lag-1
   autocorrelation of distances, yang-balanced groups of four, and
   within/between-pair asymmetry". The deposited code agrees: the frozen
   `LADDER` table in `verify_paper.py` carries exactly four keys per rung,
   `transition`, `alternation`, `balanced` and `within`. The inversion count
   against the binary order is not among them, on P1 or on any other rung.

   `null-ladder` does not measure it either. It is an order-theoretic paper
   about when a rung stops being informative; its occurrences of the
   statistic's vocabulary are the King Wen against Mawangdui comparison,
   which is a different pair of orderings and is not taken under a rung.

   And `forced-counts` says of this exact question:

   > "That is an inferential question, and it is not asked in this paper."

**The qualification, which is material and is not buried.** That the
measurement is not prior does not make it worth much. The free null and rung
P1 share their centre exactly: the unrestricted expectation is
n(n-1)/4 = 1008, and this lane's own analytic result is that the P1 mean is
1008 as well. They differ only in dispersion, 86.3 against the 80.450 measured
here, which is about seven per cent. A count five from the centre is ordinary
under either. So the published free-null result already told a careful reader
what the P1 evaluation would say, and this lane confirmed it rather than
discovered it.

What is in this lane and was not found in what was read: the P1 mean as an
exact analytic result rather than an inherited coincidence, the dispersion of
the count under P1, the decomposition of the count into an orientation
component with an exact law and a block order component, and the separate
location of each. Whether that is worth depositing is a decision, not a
finding, and it is listed as pending.

**The limits of this closing, written because they are the point.** What was
read is listed above and is not the literature. It is three deposits by one
author. No journal, no database, no search of anyone else's work was involved
in this question. The absence of this measurement in these three deposits is
absence in these three deposits. It is not absence in the literature, and no
sentence in this repository may use it as though it were.

**No novelty is claimed.** Not of the measurement, not of the analytic result,
not of the decomposition, not of anything. This section closes one question.
The review closes when the status line at the top says CLOSED, and it does
not say that.

### What was decided on this verdict

Alexis Garcia Hurtado, 2026-08-11, session five: this lane does not deposit.
The decision was taken on this verdict and on the qualification recorded with
it, and the reason is the qualification rather than the verdict. The act is
`CLOSED.md` and the decision is recorded in `DECISIONS.md`, decision ten.

Nothing in this file is withdrawn or rewritten by that decision. The verdict
stands as it was written, including the part of it that says the measurement
had not been made before, and including the part that says this matters less
than it sounds.

Session five is the last session of this lane. The review is left open on
scope items one to five, and a later reader should treat it as open rather
than as abandoned: the prohibition below is not lifted by a lane ending.

## Why it does not inherit

The prior lane carried a background review. That review was conducted for a
different question: whether a symmetry group forces a discordance count. This
lane asks an inferential question: where an observed count falls inside a
family that holds a pairing fixed. Those questions have different
literatures. Restricted and conditional permutation nulls, exchangeability,
Monte Carlo inference on constrained sequence families: none of that is what
the prior review had to cover, and there is no reason to think it did.

Inheriting it would be the cheap move and it would be wrong. The review is
started here from nothing.

## Standing prohibition while this file says UNSTARTED

This repository asserts the novelty, priority or originality of nothing. Not
of the question, not of the family, not of the statistic, not of the
decomposition in preregistration section (c), not of any result.

That prohibition binds every artefact of this lane, including commit
messages, session reports, and anything prepared for deposit. A sentence of
the form "this has not been done before", "we are the first to", or "no prior
work addresses" may not be written here until this file says CLOSED.

## What the review has to cover before it can close

1. Statistical work on the King Wen sequence, of any kind, including work
   that reaches conclusions this lane would not.
2. Discordance and inversion counts of a sequence against a structured
   reference order: Kendall's coefficient and its relatives, and their
   distribution theory under restricted permutation groups.
3. Conditional, restricted and non exchangeable permutation nulls: what is
   standard, what the accepted vocabulary is, and whether the family of
   preregistration section (b) is an instance of a named construction.
4. The King Wen pairing itself, before and after Radisic (2026): who
   described it, who characterised it, and whether its optimality was known
   or conjectured earlier.
5. The binary ordering of the hexagrams and its history, since it is the
   reference order of the statistic.
6. Whether the exact question of preregistration section (a) has already
   been asked and answered by somebody.

Point six is the one that decides whether this lane has anything to say.

**Status of the six items after session four.** Item six is answered for the
three deposits of this author, and only for them, in the section above. Items
one to five are unstarted: no journal, no database and no work by anybody else
has been searched for any of them. That is why the status line still says
OPENED and not CLOSED, and why the prohibition below is still in force.

## The lead that matters most, found in session two and not read

While locating the received King Wen sequence at the deposit tag of
`kingwen-orderings-replication`, the listing of that deposit showed that its
appendix A is titled, in the deposited code, "the ladder of conditional
nulls", with a table of its own and a dedicated protocol seed. A sibling
repository named `null-ladder` exists and carries its own deposit tag.

That is a conditional null construction, on the King Wen sequence, by the
same author, already deposited. The question of this lane is where an
observed count falls inside a conditional null. Those two things may be the
same question, may be neighbouring questions, or may be unrelated beyond the
word. **This lane does not know, because it has not read them.**

It was not read in session two, on purpose. Reading it properly is background
review work, and doing it in passing, while looking for a data file, would
produce exactly the half informed impression this file exists to prevent. It
is recorded here instead, at the top, as the first thing the review must
settle.

Until it is settled, the standing prohibition below is not a formality. This
lane may be asking a question its own author has already answered, and it
must not say otherwise, in any direction, until somebody has read them.

Scope item six is where this is decided.

## Queued leads, seen but not reviewed

Recorded so they are not lost, and flagged so they are not mistaken for
review work already done. Each of these was returned incidentally by a term
gate query, was not read, and counts for nothing until it is.

- The appendix A of `kingwen-orderings-replication` at `zenodo-v3`, on a
  ladder of conditional nulls, and the deposited repository `null-ladder`.
  Both are readable under contact rules two and three. Inside scope items one,
  three and six, and see the section above. Not read.
- arXiv:2604.09234, "Statistical Properties of the King Wen Sequence: An
  Anti-Habituation Structure That Does Not Improve Neural Network Training".
  Directly inside scope item one. Not read.
- arXiv:1808.10483, "Permutation tests of non-exchangeable null models".
  Directly inside scope item three. Not read.
- arXiv:2205.01416, "Exact Paired-Permutation Testing for Structured Test
  Statistics". Inside scope item three, and it owns vocabulary this lane must
  not collide with. Not read. See `NAME-GATE.md`.
- arXiv:2607.29242, "How null-model constraints affect statistical validation
  in projected bipartite networks". Inside scope item three, on the general
  question of what relaxing a null constraint does. Not read.

## What closing means

The review is closed by a commit that records, for each scope item: the
databases queried, the queries as run, the dates, what was found, what was
read in full as opposed to by abstract, and the resulting position on point
six. The status line at the top of this file changes to CLOSED in that same
commit, and not before.

Until then this file stands as written, and the prohibition above is in
force.
