# TODO: Validate
import os
import runpy
import subprocess
import sys
from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parent
VENV_PATH = PROJECT_PATH / ".venv"
VENV_PYTHON_PATH = (
    VENV_PATH / "Scripts" / "python.exe"
    if os.name == "nt"
    else VENV_PATH / "bin" / "python"
)

if __name__ == "__main__":
    if VENV_PYTHON_PATH.exists() and Path(sys.prefix).resolve() != VENV_PATH:
        venv_run = subprocess.run(  # noqa: S603 - Runs this file again.
            [str(VENV_PYTHON_PATH), __file__, *sys.argv[1:]],
            check=False,
        )
        sys.exit(venv_run.returncode)

    os.chdir(PROJECT_PATH)
    sys.path.insert(0, str(PROJECT_PATH))
    runpy.run_module("generate.generate_models", run_name="__main__")
