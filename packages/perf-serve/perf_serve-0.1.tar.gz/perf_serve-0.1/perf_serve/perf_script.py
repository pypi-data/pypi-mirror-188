from tempfile import NamedTemporaryFile, _TemporaryFileWrapper
from pathlib import Path

import subprocess


def run_perf_script(path: Path) -> _TemporaryFileWrapper:
    command = ['perf', 'script', '-F', '+pid', '-i', str(path)]
    tempfile = NamedTemporaryFile(mode='w+t')

    print(f"Running {' '.join(command)} > {tempfile.name}")
    subprocess.run(command, check=True, stdout=tempfile)
    return tempfile
