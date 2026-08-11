"""Read a neighbour's file at its deposit tag, without copying it in.

Contact rules one to three: read only, and only at the tag. This helper
addresses the tag through git, never moves the neighbour's working tree, and
records the digest of what it read so that a later run can tell whether it
read the same bytes.

The local checkout is passed on the command line by the caller and is stored
nowhere. The repository and the tag identify the source.

Nothing read here enters the history of this repository. When a neighbour's
module has to be executed, it is written to a scratch file outside the
repository and imported from there.
"""

import hashlib
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

LADDER_TAG = "zenodo-10.5281-zenodo.21750029"
KINGWEN_TAG = "zenodo-v3"


def read_at_tag(checkout, tag, path):
    """Bytes of one file at one tag, and their digest."""
    proc = subprocess.run(["git", "-C", str(checkout), "show", f"{tag}:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(f"could not read {tag}:{path} from the checkout "
                         f"given: {proc.stderr.decode(errors='replace').strip()}")
    blob = proc.stdout
    return blob, hashlib.sha256(blob).hexdigest()


def working_tree_untouched(checkout):
    """The branch the neighbour is on, so the caller can show it did not move."""
    proc = subprocess.run(["git", "-C", str(checkout), "rev-parse",
                           "--abbrev-ref", "HEAD"], capture_output=True, text=True)
    return proc.stdout.strip()


def import_at_tag(checkout, tag, path, module_name):
    """Import a neighbour's module from its tag, via a scratch file.

    The scratch file is outside this repository and is removed by the
    operating system's temporary directory policy. It is never added to the
    history, and this function returns the digest of exactly what was run so
    that the report can name it.
    """
    blob, digest = read_at_tag(checkout, tag, path)
    scratch = Path(tempfile.gettempdir()) / f"{module_name}-{digest[:12]}.py"
    scratch.write_bytes(blob)
    spec = importlib.util.spec_from_file_location(module_name, scratch)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module, digest, str(scratch)
