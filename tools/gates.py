"""Run every standing gate of this repository and report a single verdict.

Gates, in the order they run:

  1. dash gate      no forbidden dash in any tracked text file
  2. effort log     the hash chain is intact and the session structure is sound
  3. figure gate    the registry parses and every record is well formed

The figure gate for commit messages runs from the commit-msg hook, not here,
because it needs the message. This runner checks only that the registry it
consults is readable and well formed.

Exit status zero when every gate passes.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"


def run(label, argv):
    print(f"--- {label}")
    proc = subprocess.run([sys.executable, *argv], cwd=ROOT)
    return proc.returncode


def registry_wellformed():
    print("--- figure registry")
    sys.path.insert(0, str(TOOLS))
    import figures
    records = figures.load()
    required = {"token", "object", "status", "source", "verified_by", "utc"}
    bad = 0
    for i, r in enumerate(records):
        missing = required - set(r)
        if missing:
            print(f"record {i}: missing field(s) {', '.join(sorted(missing))}")
            bad += 1
        elif r["status"] not in figures.STATUSES:
            print(f"record {i}: unknown status {r['status']!r}")
            bad += 1
        elif r["status"] == "verified-here" and not r["verified_by"]:
            print(f"record {i}: verified-here with no verifying artefact named")
            bad += 1
    if bad:
        print(f"figure registry: FAIL, {bad} malformed record(s)")
        return 1
    usable = sum(1 for r in records if r["status"] == "verified-here")
    print(f"figure registry: PASS, records well formed, "
          f"usable in a commit message: {usable}")
    return 0


def main():
    codes = [
        run("dash gate", [str(TOOLS / "dashcheck.py")]),
        run("effort log", [str(TOOLS / "effortlog.py"), "verify"]),
        registry_wellformed(),
    ]
    print()
    if any(codes):
        print("GATES: FAIL")
        return 1
    print("GATES: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
