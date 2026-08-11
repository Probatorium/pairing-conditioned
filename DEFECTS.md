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
