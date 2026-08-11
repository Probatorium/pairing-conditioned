# Manifest of files this lane did not produce

Every file this lane did not produce and that has entered the working copy is
listed here, under rule six of `CONTACT-RULES.md`. Entries are written at the
moment of entry. A file present and absent from this table is a rule
violation, not an oversight.

Required for each entry: file name, origin, exact retrieval address,
retrieval date, SHA-256 digest, licence or rights status as stated by the
source, and the use this lane makes of it.

---

## Received from a neighbour under the named exception to rule six

### `data/king-wen-received.json`

| field | value |
| --- | --- |
| origin | `github.com/Probatorium/kingwen-orderings-replication` |
| retrieval address | tag `zenodo-v3`, file `verify_paper.py`, symbol `KING_WEN` |
| access | read only, addressed at the tag; the neighbour's working tree was not moved and was confirmed still on its own branch afterwards |
| retrieval date | 2026-08-11 |
| SHA-256 | `be9aef30ff1bedcffe86ef1e8a5955c39a5a321183a4cf812b2746685d417f3d` |
| rights | Same lane, same author. The neighbour carries a licence file at its deposit tag; this transcription is of a factual sequence, not of expression. |
| use | The received King Wen order, the object of the whole analysis. |
| status | Received data. Never recomputed in this lane. |

**How it was transcribed.** Mechanically, by `tools/receive_kingwen.py`,
which reads the blob at the tag through git and extracts the named symbol. It
was not typed. A copying error is therefore not one of the ways this lane can
be wrong, and the tool can be run again by anyone with a checkout to
reproduce the file byte for byte.

**What was checked on entry.** That the list has sixty-four entries, that they
are distinct, and that each lies in the range of a six bit value. These are
checks on the transcription. They are not a recomputation of the sequence,
which decision five forbids.

**What was not checked, deliberately.** That the adjacency pairing of this
sequence equals the matching of the cited theorem. That is precondition P1 of
the preregistration, it can stop the lane, and it belongs to the analysis
rather than to the loading dock.

**Corroboration, received rather than performed.** The prior lane reports
that this list was corroborated in full against appendix A of Radisic, so it
is not single sourced. This lane did not repeat that corroboration and does
not claim to have. The figure is registered in `FIGURES.jsonl` as
cited-unverified and is refused in commit messages accordingly.

**Where the local checkout path went.** Nowhere. The tool takes it on the
command line and stores it in no file. The repository and the tag identify
the source; a path on one machine identifies an account.

---

## Third party files

None. No file from outside this lane has entered this repository.

`vendor/` does not exist because nothing has needed it.
