import pathlib
import runpy
import subprocess
import sys

import typer
from coherent.build import bootstrap


app = typer.Typer()

passthrough_command = app.command(
    context_settings={
        'allow_extra_args': True,
        'ignore_unknown_options': True,
    },
)


@app.command()
def install(target: pathlib.Path) -> None:
    with bootstrap.write_pyproject(target):
        subprocess.run([sys.executable, '-m', 'pip', 'install', target])


@passthrough_command
def build() -> None:
    del sys.argv[1]
    runpy.run_module('coherent.build', run_name='__main__')


@passthrough_command
def test() -> None:
    del sys.argv[1]
    runpy.run_module('coherent.test', run_name='__main__')


if __name__ == '__main__':
    app()
