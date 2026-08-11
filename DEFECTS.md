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
