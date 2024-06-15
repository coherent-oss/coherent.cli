import pathlib
import subprocess
import sys

import typer
from coherent.build import bootstrap


app = typer.Typer()


@app.command()
def install(target: pathlib.Path):
    with bootstrap.write_pyproject(target):
        subprocess.run([sys.executable, '-m', 'pip', 'install', target])


@app.command()
def build():
    subprocess.run([sys.executable, '-m', 'coherent.build'])


@app.command()
def test():
    subprocess.run([sys.executable, '-m', 'coherent.test'])


if __name__ == '__main__':
    app()
