# Defects

Signed texts are not amended in this lane. When something is found to be
wrong or badly posed, it is recorded here and corrected forward. This file is
append only in practice: entries are added, and an entry that turns out to be
mistaken gets a later entry saying so rather than an edit.

Every entry states what the defect is, how it was found, what was done, and
what it cost. An entry that cannot say how it was found is a weaker entry and
should say that too.

---

## Defect one: the dash gate carried the characters it forbids

**What.** `tools/dashcheck.py` and `tools/test_gates.py` held the forbidden
dash characters as literals in their own source, in the table of what to
forbid and in the test fixtures. The gate therefore failed its own rule.

**How found.** By the gate, on its first run, before the code was committed.
It reported its own source as the offender.

**Done.** The characters are now written as codepoint escapes in both files,
so no literal occurrence exists anywhere in the tree. The alternative, adding
the enforcer to the exemption list, was rejected: an exemption for the
enforcer is exactly the hole a reader should look for first, and granting it
would have made every later clean sweep worth less.

**Cost.** None beyond the fix. The defect never entered the history. The
sweep over the three commits that were made before the gate existed was run
afterwards and came back clean.

---

## Defect two: a commit message narrower than its commit

**What.** The apparatus commit was staged with a command that sweeps the
whole working tree. It carries `BACKGROUND-REVIEW.md`, `REFERENCES.md`,
`THIRD-PARTY-MANIFEST.md` and the two logs, none of which its message
describes. The message speaks only of the gates and their tests.

**How found.** By listing the contents of the commit after making it, which
is a check that should have run before it.

**Done.** Corrected forward, not rewritten. The commit stands as it is and
this entry is the record of what it actually contains. The history is not
reshaped to look tidier than the work was, because a repository whose whole
claim is that its record is exact cannot buy neatness with a rewrite.

**Cost.** A reader of that commit message alone would underestimate what
landed in it. That cost is real and is not recovered by this entry, only
documented. The practice that follows from it: stage by name, and read the
list of what is staged before writing the message that describes it.

---

## Defect three: the session one report undercounted its own commits

**What.** `SESSION-REPORT-001.md` opens its commit section with a count of
five and enumerates five commits. The commit that carries the report is a
sixth, so a reader standing at the head of that session sees six where the
report says five. The enumeration itself is correct as far as it goes; only
the count is short, and only by the report's own commit.

**How found.** By reading the head of the session against the report
immediately after the report was committed.

**Done.** Nothing to that session. It was closed, and reopening a closed
session to adjust a self referential count would cost more in the integrity
of the record than the count is worth: the correction would itself be a
seventh commit, and the report would be wrong again. Recorded here, and
recorded in the effort log of session two, which is where a reader who
follows the chain will meet it.

**Cost.** A reader who takes the count and not the enumeration is off by one
for that session. The practice that follows: a session report states the
commits it enumerates and says that its own commit is not among them, rather
than stating a total.

---

## Defect four: a machine account name is published in a superseded blob

**What.** The version of `CONTACT-RULES.md` written in session one named
neighbouring repositories by their local checkout directory. Two of those
lines carry the account name of the machine the work was done on. That blob
lives in commit `59283f7` and is published with it.

**How found.** By the pre publication sweep, `tools/prepublish.py`, on its
first run, before the first push. This is the category the sweep exists to
catch and it caught it.

**Done, in two parts.** The working tree was corrected forward in session
two, before the sweep ran and for an independent reason: neighbours are now
named by repository path, because a local path identifies an account rather
than a repository and is not what the rule is about. The current tree is
clean and the sweep confirms it.

The historical blob was accepted rather than removed. Decision by Alexis
Garcia Hurtado, 2026-08-11, taken on the sweep's report before the push.
Removing it would mean rewriting every commit after the root, which would
leave the preregistration's signature intact but would break the commit
references already written into the effort log, and would spend the lane's
declared position on not rewriting history in order to hide an account name
that is not a credential.

**Cost, stated plainly.** The account name of the machine is public in the
history of this repository and will stay public. It is not a secret and it is
not a credential, and the author's identity is already public on the
deposited work this lane cites. That is the whole of the exposure and it is
not reduced by this entry, only recorded.

**Practice that follows.** The sweep runs before every push, not only the
first, and identifying a neighbour by a local path is now a thing this lane
does not do.

---

## Defect five: the signed document required a tolerance and did not fix it

**What.** Preregistration section (c) requires the sampler to reproduce the
analytic mean "within declared Monte Carlo tolerance". Section (g) fixes a
tolerance for p-values. Neither fixes a number for the acceptance test.

**How found.** By trying to run the acceptance test and finding there was no
threshold to run it against.

**Done.** Four standard errors of the sample mean was fixed in
`analysis/validate.py`, in the code and in its docstring, before the run and
before any figure was looked at. Declared here rather than filled quietly.

**Cost.** A tolerance chosen by the person who will use it is weaker than one
chosen in advance by the person who cannot yet see the data, and this one was
chosen in the session that used it. The mitigation is only that it was
written before the run and that the observed deviation, at most 1.37 standard
errors, is far from any threshold a reasonable person would have set. That
mitigation is luck, not design.

---

## Defect six: the multiplicity rule did not say which member of a pair supplies the p

**What.** Preregistration section (e) collapses two tests into one when the
complement invariance holds for them, but the two members are sampled from
independent streams and so return slightly different estimates. The document
does not say which one is carried forward.

**How found.** At the point of applying the correction.

**Done.** The smaller of the two was taken, which is the choice least
favourable to the outcome the document said it expected. Recorded in
`analysis/measure.py` at the point of the choice and in `RESULTS.md`.

**Cost.** None to the verdict: the two members differ by less than 0.0007
throughout, and the verdict is identical under either choice and under no
correction at all. The cost is to the document, which will need the rule
stated properly if this design is ever reused.

---

## Finding seven, which is not a defect of this lane but a gap in its rule

**What.** Reversing which end of the figure carries the most significant bit
swaps the two members of every block that is a reversal pair. Every block
therefore keeps its value set, the between-block table depends only on those
sets, and so the entire law of the block order component is unchanged. The
first and third conventions share a family law, and so do the second and
fourth. Here they also share their observed values, because exactly half of
the twenty-eight reversal blocks are discordant as received.

So the genuine number of distinct tests is four, where the signed rule
computes eight.

**How found.** By checking, after the measurement, whether the two
conventions that produced identical observed values had done so by accident.
They had not.

**Done, which is to say deliberately nothing.** Section (e) collapses tests
only under the complement invariance it named and says "no other value is
permitted". The correction was run over eight as the rule requires. Acting on
the finding would have weakened the correction, which would have made
refutation easier, which is the direction of the outcome the document
expected. Taking the harder road when the rule is silent is the only way the
rule keeps its value.

**Cost.** None to the verdict, which is the same over four and over eight and
over none. The record is that the signed rule anticipated one of the two
collapses that exist.

---

## Defect eight: the session four report miscounted the effort log

Recorded 2026-08-11, in session five.

**What.** `SESSION-REPORT-004.md` states, in its section on the state of the
chain, "forty entries at close, six added this session". Both figures are
wrong. The log held forty-one entries at the moment session four closed, and
seven were added in that session, indices 34 to 40 inclusive, the first being
the opening entry and the last the closing one. The error is an undercount of
one in each figure, and it came from counting the entries of the session
before the closing entry that the same sentence describes.

**How found.** By checking the report against the log after the session had
closed and the report had been pushed.

**Done.** Corrected forward, here, with the figures stated. `SESSION-REPORT-004.md`
is not touched. It is the record of what that session reported, and a record
that gets edited whenever it turns out to be wrong is not a record.

**What the apparatus did, which is worth stating.** The error was visible
immediately and could not be fixed immediately: the effort log tool refuses a
work entry outside an open session, so amending the report would have required
opening a session, which is a deliberate act with its own record. That is the
apparatus working rather than obstructing. The cost of the friction is one
session of delay on a two word correction. The benefit is that no artefact of
this lane can be quietly adjusted between sessions.

**Cost.** A reader who took the count rather than the log itself is off by one
in two places for one session. The log is authoritative and verifies.

**Practice that follows, and it is the same one defect three produced.** A
report that states a count of its own record should derive it rather than
type it. Neither report did.

---

## Known limitation, since decision six: an all digit object name is refused

The figure gate can now tell an identifier from a measurement, but only where
the two are actually distinguishable. A short git object name that happens to
contain no hexadecimal letter, such as a seven character abbreviation made
entirely of digits, is indistinguishable from a number and is refused.

Left as it is. The alternative is a pattern that accepts any seven to forty
digit run as an object name, which is a wide door for a measurement to walk
through. The cost is that such a hash is written in a commit message as the
longer form that contains a letter, or left out.

## Known limitation, not a defect: the figure gate refuses identifiers

The figure gate refuses any digit sequence in a commit message that does not
resolve to a figure verified inside this repository. It does not distinguish
a measured quantity from an identifier, so a defect number, a version, an
arXiv identifier or a date in the body of a message is refused too.

This is recorded as a limitation rather than fixed, because every way of
relaxing it introduces a pattern by which a real figure could be dressed up
as an identifier and walk through. The current cost is that commit messages
are written without numerals, which they have been so far without strain.

Whether to register an identifier pattern is a decision for Alexis and is
listed as pending in the session report.

**Resolved in session two by decision six.** The gate now distinguishes them,
under three conditions: every exemption states a reason, every exemption is
counted and printed so that nothing passes silently, and a token registered
in `FIGURES.jsonl` can never pass as an identifier however much it looks like
one. That last condition is what closes the hole this section worried about:
a measurement cannot dress itself as a year, because the registry outranks
every pattern. The text above stands as the record of the state before the
decision and is not rewritten to agree with it.
