r"""CLI entrypoint for oracle evaluation"""

import math
from pathlib import Path
import json
import sys
from tdc import Oracle

_SUPPORTED_ORACLES = ["gsk3b", "jnk3", "drd2"]

_ORACLE_CACHE_PATH = Path.home() / ".local" / "share" / "tdc-cache" / "oracle"


def main() -> None:
    name = sys.argv[1]
    if name not in _SUPPORTED_ORACLES:
        print(json.dumps(f"Unsupported Oracle {name}"))
        sys.exit(1)

    oracle = Oracle(name, verbose=False)
    results = oracle(sys.argv[2:])
    print(json.dumps(results))

def clean() -> None:
    for f in sorted(_ORACLE_CACHE_PATH.glob("*.pkl")):
        f.unlink()
    print("Done!")

_TEST_SMI = 'CC(C)(C)[C@H]1CCc2c(sc(NC(=O)COc3ccc(Cl)cc3)c2C(N)=O)C1'
_TEST_RESULTS = {"gsk3b": 0.03, "jnk3": 0.01, "drd2": 0.0015465365340340924}

def download() -> None:
    print("Downloading oracles...")
    downloaded_files = sorted(_ORACLE_CACHE_PATH.glob("*.pkl"))
    for name in _SUPPORTED_ORACLES:
        if any(f.name.startswith(name) for f in downloaded_files):
            print(f"Found oracle '{name}' locally")
        else:
            print(f"Downloading '{name}' oracle")
            _ = Oracle(name, verbose=False)
    print("Done!")
    print()
    print("Testing oracles...")
    for name in _SUPPORTED_ORACLES:
        oracle = Oracle(name, verbose=False)
        if not math.isclose(oracle(_TEST_SMI), _TEST_RESULTS[name]):
            print(f"ERROR: Oracle {name} failed test")
        else:
            print(f"SUCCESS: Oracle {name} passed test")


def ls() -> None:
    print(" ".join(_SUPPORTED_ORACLES))
