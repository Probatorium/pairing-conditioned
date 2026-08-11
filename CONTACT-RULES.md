# Contact rules

Binding from the second commit of this repository. These rules govern how
this lane touches anything outside itself. They are operational, not
aspirational: each one states what may be done, what may not, and how the
permitted action is performed.

---

## 1. forced-counts

Deposited work, `10.5281/zenodo.21889328`. Local checkout at
`C:\Users\AlexDesk\Documents\forced-counts`.

- READ ONLY, and only at the tag `zenodo-v1`.
- It is deposited and frozen. It is not edited. Nothing is added to it. No
  correction, no erratum, no note, no file, no branch, no tag.
- Its working tree is not checked out to that tag or to anything else. Its
  branch is not changed. Reading is done without moving anything, by
  addressing the tag directly:

      git -C <path> show zenodo-v1:<file>
      git -C <path> ls-tree -r --name-only zenodo-v1

- No fetch, no pull, no push, no gc, no reflog expiry is run against it from
  this lane.
- Its HEAD is not read as a source. If HEAD and `zenodo-v1` differ, the tag
  is what exists for this lane and HEAD does not.
- Nothing is copied from it into this repository except under rule 5.

## 2. kingwen-orderings-replication

Local checkout at `C:\Users\AlexDesk\Documents\kingwen-orderings-replication`.

- READ ONLY, and only at the tag `zenodo-v3`.
- Recorded at the opening of this lane, as a fact about that repository and
  not as a comment on it: its HEAD is on a branch that is not the deposit,
  and it carries tags other than `zenodo-v3`. None of that is visible to this
  lane. Only `zenodo-v3` is.
- Same mechanics as rule 1: address the tag, move nothing.

## 3. Stasis

- Untouchable. Not read, not written, not referenced as a source, not
  depended upon.
- Its location was not resolved in the inaugural session and is deliberately
  not resolved. Untouchable does not require knowing where it is.

## 4. Remote

The intent of this lane is that it is born without a remote, and that
creating one requires an explicit request from Alexis.

The state of affairs is recorded truthfully rather than tidily:

- A remote named `origin` exists in this working copy. It exists because
  Alexis created the repository `Probatorium/pairing-conditioned` and
  instructed that it be cloned. That instruction is the explicit request the
  rule requires, and it is logged as such.
- Nothing has been pushed. The remote holds no commit from this lane.
- Publication is a separate act from the existence of a remote. No push, no
  branch publication, no tag publication, no release and no change of
  repository visibility happens without a further explicit instruction from
  Alexis naming that act. Being asked to clone is not being asked to push.
- If Alexis prefers the stricter reading, `git remote remove origin` restores
  it, and the local history is unaffected either way. That decision is his
  and is listed as pending in the session report.

## 5. Third party files

Any file that this lane did not produce and that enters the working copy is a
third party file. This includes data, and in particular it includes any table
of the King Wen sequence or of hexagram line values, which the analysis will
need and which this lane does not own.

- Third party files live under `vendor/` and stay out of the public history.
  `vendor/` is ignored by version control.
- Every third party file is recorded in `THIRD-PARTY-MANIFEST.md`, which is
  versioned, with: the file name, its origin, the exact retrieval address,
  the retrieval date, its SHA-256 digest, its licence or rights status as
  stated by the source, and what this lane uses it for.
- The manifest is written at the moment of entry, not afterwards.
- A digest recorded in the manifest is checked before the file is used, on
  every run, and a mismatch is a hard stop.
- Derived data that this lane computes from a third party file is not itself
  third party and may enter the history, provided the manifest entry for its
  source is present and the derivation is in the repository.
- Nothing under rules 1, 2 or 3 becomes a third party file by being copied.
  It is not copied.

## 6. Standing on the frozen work

- The prior lane is cited. It is not continued inside itself.
- No figure of the prior lane is reused here as an established quantity. If
  this lane needs a value the prior lane reported, it recomputes it from
  primary data and reports both, agreement or disagreement.
- If this lane finds a defect in the deposited work, that finding is recorded
  here, in this repository, and the deposited work is still not touched.

## 7. Amendment

These rules may be extended by a later commit. Rules 1, 2, 3 and 5 may not be
weakened. Rule 4 records a state of affairs and is updated when that state of
affairs changes, by Alexis or on his instruction, with the change and its
authorization recorded in the effort log.
