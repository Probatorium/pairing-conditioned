# Contact rules

Binding from the second commit of this repository. These rules govern how
this lane touches anything outside itself. They are operational, not
aspirational: each one states what may be done, what may not, and how the
permitted action is performed.

Restated in full in session two, after the decisions recorded in
`DECISIONS.md`. Rules one, two, three and six are unchanged in substance.
Rule four is new. Rule five records a state of affairs that changed. Rule six
gains one narrow, named exception.

**Neighbours are identified by repository path, not by where they happen to
sit on a disk.** Session one named local checkout directories. That was
replaced here: a local path is an accident of one machine, it identifies a
person's account, and it is not what the rule is about. The rules below name
repositories. Finding a local checkout of one, when a rule permits reading
it, is a local matter and is not part of the public record.

---

## 1. forced-counts

`github.com/Probatorium/forced-counts`. Deposited work,
`10.5281/zenodo.21889328`.

- READ ONLY, and only at the tag `zenodo-v1`.
- It is deposited and frozen. It is not edited. Nothing is added to it. No
  correction, no erratum, no note, no file, no branch, no tag.
- Its working tree is not checked out to that tag or to anything else. Its
  branch is not changed. Reading is done without moving anything, by
  addressing the tag directly:

      git -C <checkout> show zenodo-v1:<file>
      git -C <checkout> ls-tree -r --name-only zenodo-v1

- No fetch, no pull, no push, no gc, no reflog expiry is run against it from
  this lane.
- Its HEAD is not read as a source. If HEAD and `zenodo-v1` differ, the tag
  is what exists for this lane and HEAD does not.

## 2. kingwen-orderings-replication

`github.com/Probatorium/kingwen-orderings-replication`.

- READ ONLY, and only at the tag `zenodo-v3`.
- Recorded as a fact about that repository and not as a comment on it: its
  HEAD is on a branch that is not the deposit, and it carries tags other than
  `zenodo-v3`. None of that is visible to this lane. Only `zenodo-v3` is.
- Same mechanics as rule one: address the tag, move nothing.
- This is the source of the received King Wen sequence under rule six.

## 3. null-ladder

`github.com/Probatorium/null-ladder`.

- READ ONLY, and only at its deposit tag, which is
  `zenodo-10.5281-zenodo.21750029`.
- Same mechanics as rule one.

## 4. Stasis and its sibling repositories

`github.com/Probatorium/stasis`, and the sibling repositories of that lane:
`minimal-verified-paper`, `defect-injection-study`, `stasis-antecedentes`.

- UNTOUCHABLE. Not read, not written, not fetched, not cloned, not linked,
  not depended upon.
- Identified by repository path and not by a deposit tag, because they have
  no deposit tag. They are not published: no DOI, no deposit, no tag, and
  third party verification of that lane is still outstanding.
- **Not citable, and this is the operative consequence.** Nothing from those
  repositories is cited in this lane, in any artefact, including anything
  prepared for deposit. A citation to an unpublished manuscript is not a
  citation: it points at something a reader cannot obtain, cannot check and
  cannot hold the author to.
- If a technique originating in that lane turns out to be useful here, it is
  described in this lane's own terms, in full, so that a reader can follow it
  without the missing source. It is not cited, not credited to a document
  that does not exist publicly, and not gestured at.
- The prohibition is not a judgement about the quality of that work. It
  follows only from the fact that it is not published.
- This rule is checked mechanically. `tools/untouchable.py` runs with the
  standing gates and fails if any of those repository names appears anywhere
  in the tracked tree or in the history outside the places where declaring
  the rule requires naming them, or if any remote, submodule or alternate of
  this repository points at one of them.

## 5. Remote and publication

- The remote is `github.com/Probatorium/matching-conditioned`, renamed on the
  forge by Alexis in session two when the name was adopted.
- Publication is authorised, as recorded in `DECISIONS.md`, decision two.
- Before a first push, the house procedure runs and its output is reported: a
  one line log of every commit, a sweep of every blob of every commit for
  secrets, tokens and personal paths, and `git ls-remote` to confirm the
  remote is empty. After the push: address, visibility, local head, remote
  head, and confirmation that the trees are identical.
- The authorisation is for publishing this history. It does not make every
  later push automatic, and it does not authorise a change of visibility, a
  release, or a deposit.

## 6. Files that this lane did not produce

Any file this lane did not produce and that enters the working copy is
recorded, whether it comes from a third party or from a neighbour under rules
one to three.

- Third party files live under `vendor/` and stay out of the public history.
  `vendor/` is ignored by version control.
- Every such file is recorded in `THIRD-PARTY-MANIFEST.md`, which is
  versioned, with: the name, the origin, the exact retrieval address, the
  retrieval date, the SHA-256 digest, the licence or rights status as stated
  by the source, and what this lane uses it for.
- The manifest is written at the moment of entry, not afterwards.
- A digest recorded in the manifest is checked before the file is used, on
  every run, and a mismatch is a hard stop.
- Derived data that this lane computes from such a file is not itself
  foreign and may enter the history, provided the manifest entry for its
  source is present and the derivation is in the repository.

### The one exception, named and bounded

Session one wrote that nothing under rules one, two or three is copied at
all. Decision five of session two overrides that for exactly one object: the
received King Wen sequence, which enters as a transcription from
`kingwen-orderings-replication` at `zenodo-v3`.

The tension is written out rather than smoothed over. The original clause
existed to stop deposited work being laundered into this repository and
re-presented as this lane's own. The exception does not do that: the
transcription carries its provenance in the file, is marked as received data,
is never recomputed here, and is credited to the deposit it came from. It
enters the versioned history rather than `vendor/` because it is small,
because a reader must be able to see exactly what was analysed, and because
hiding the input of an analysis behind an ignore rule would defeat the point
of the lane.

The general prohibition stands for everything else. This exception covers one
named object and does not generalise.

## 7. Standing on the frozen work

- The prior lanes are cited where they are published. They are not continued
  inside themselves.
- No figure of a prior lane is reused here as an established quantity. If
  this lane needs a value a prior lane reported, it recomputes it from
  primary data and reports both, agreement or disagreement. The single
  exception is data explicitly received rather than derived, under rule six,
  which is marked as received and is never recomputed by definition.
- If this lane finds a defect in a deposited work, that finding is recorded
  here, in this repository, and the deposited work is still not touched.

## 8. Amendment

These rules may be extended by a later commit. Rules one, two, three, four
and six may not be weakened, and an exception to them is only valid if it is
recorded in `DECISIONS.md` with its decider and its date, and written out in
the rule itself as rule six now writes out its one exception. Rule five
records a state of affairs and is updated when that state of affairs changes,
with the change and its authorisation recorded in the effort log.
