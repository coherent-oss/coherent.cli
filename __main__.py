import pathlib
import subprocess
import sys

import typer
from coherent.build import bootstrap


app = typer.Typer()


@app.command()
def install(target: pathlib.Path):
    with bootstrap.write_pyproject(target):
        subprocess.run([sys.executable], '-m', 'pip', 'install', target)


if __name__ == '__main__':
    app()
