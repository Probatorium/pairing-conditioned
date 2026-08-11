# Decisions

Decisions taken by Alexis Garcia Hurtado, recorded with their date, their
decider and what each one changed. A decision recorded here is binding on the
lane until a later decision recorded here supersedes it.

This file records decisions. It does not record the reasoning that was
offered before them, which lives in the artefact that raised the question,
and it does not silently absorb the evidence a decision was taken against.
Where a decision overrode a measurement, the measurement stays where it was
made.

---

## Session two, 2026-08-11. Decider: Alexis Garcia Hurtado

The seven questions left pending by the rigour report of session one, all
answered in one act.

### One. The name is `matching-conditioned`

Adopted, on the two grounds the term gate reported: the compound
`pairing-conditioned` sits in the retrieval basin of the psychology of
conditioning, and the source theorem this lane depends on calls the object a
matching rather than a pairing.

Changed by this: `NAME-GATE.md` gains a decision section and keeps every
measurement that motivated it. The repository is renamed on the forge by
Alexis and the remote address is updated to match. Nothing in the
preregistration changes, because that document defines the family
extensionally and uses no name as a load bearing term.

### Two. Publication authorised

Pushing to the forge is authorised. The house procedure runs first and its
result is reported before and after:

- a one line log of every commit,
- a sweep of every blob of every commit for secrets, tokens and personal
  paths,
- `git ls-remote` to confirm the remote holds nothing.

After the push: the address, the visibility, the local head, the remote head,
and a check that the trees are identical.

Authorising the push authorises this push of this history. It does not make
publication automatic from here on.

### Three. English, confirmed

The documents stay in English. Nothing is corrected backwards. The judgement
made in session one without asking is ratified rather than tolerated, and the
record of it having been made without asking stays in the session one report.

### Four. The asymmetry of the design is the agreed shape of the lane

Deliberate, and the reason is recorded because it is the point: writing down
in advance that the expected outcome is deflation is what stops that outcome
being sold afterwards as a discovery. A lane that can only announce a finding
when the finding is exciting is not measuring anything.

The decomposition of the statistic into its orientation component and its
block order component is registered as the place where the genuinely open
tests live, and the analysis document must say so when it is written, in
those terms, and must not present the low powered location test as though it
carried the weight of the lane.

### Five. The received King Wen sequence and where it comes from

The sequence enters from `github.com/Probatorium/kingwen-orderings-replication`
at its deposit tag, read only, as a transcription with declared provenance:
repository, tag, file, symbol, date. It is marked as received data and it is
never recomputed. This lane does not derive the King Wen sequence, does not
correct it, and does not prefer a reconstruction of its own over it.

Recorded as a fact received from the prior lane and not verified here: that
list was corroborated in full against appendix A of Radisic, so it is not
single sourced. That corroboration was performed in the prior lane. This lane
did not repeat it and does not claim to have.

Changed by this: contact rule five gains a narrow, named exception, discussed
in `CONTACT-RULES.md` where the tension is written out rather than smoothed
over.

### Six. The figure gate learns to tell an identifier from a measurement

The gate stops refusing every numeral. Identifiers may pass: a DOI, an ORCID,
a publication year, a hexadecimal hash, an archive identifier, a version, a
session or defect label.

Three conditions, all binding:

- every exemption carries a stated reason,
- every exemption is counted and printed, so no numeral passes silently,
- the registry beats the exemption. A token registered in `FIGURES.jsonl` as
  a figure can never pass as an identifier, whatever it looks like. This is
  what stops a measurement dressing itself as a year.

The figures inherited from the prior lane stay `cited-unverified` and stay
refused until they are measured here. That is not softened by this decision.

### Seven. The untouchable repositories, by path and not by tag

`github.com/Probatorium/stasis` and its sibling repositories of that lane,
`minimal-verified-paper`, `defect-injection-study` and `stasis-antecedentes`,
are untouchable, and they are identified by repository path rather than by a
deposit tag, because they have none. They are not published: no DOI, no
deposit, no tag, and third party verification is still outstanding.

The consequence is written out and is binding: nothing from those
repositories is cited in this lane. If a technique of theirs is used, it is
described in this lane's own terms without citation, because a citation to an
unpublished manuscript is not a citation.

A check that they are not touched is executable and runs with the standing
gates. See `tools/untouchable.py`.

---

## Session two, 2026-08-11, taken on the sweep's report. Decider: Alexis Garcia Hurtado

Two decisions taken during the publication procedure, on findings the
procedure produced.

### Eight. The account name in the superseded blob is accepted, not removed

The pre publication sweep found the machine account name in the session one
version of the contact rules. Accepted and declared rather than removed,
because removing it means rewriting every commit after the root, which would
break the commit references already written into the effort log in order to
hide something that is not a credential.

Recorded in full, with its cost, as defect four.

### Nine. The push goes to the name that exists

The forge still holds the repository under its old name; the rename had not
been made when the procedure ran. The history is pushed to the address that
exists. The content travels with the repository when it is renamed, and the
remote address is adjusted and verified then.

This does not reopen decision one. The adopted name is `matching-conditioned`
and the artefacts say so already.
