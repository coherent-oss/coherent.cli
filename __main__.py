import pathlib
import runpy
import subprocess
import sys
from typing_extensions import Annotated

import typer
from coherent.build import bootstrap
from jaraco.vcs import Repo
from jaraco.versioning import Versioned, semver


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
def test() -> None:
    del sys.argv[1]
    runpy.run_module('coherent.test', run_name='__main__')


@passthrough_command
def build() -> None:
    del sys.argv[1]
    runpy.run_module('coherent.build', run_name='__main__')


@app.command(context_settings=dict(allow_extra_args=True))
def tag(
    kind_or_name: str,
    context: typer.Context,
    repository: Annotated[
        Repo,
        typer.Option(
            '-R', '--repository',
            help='Path to repository.',
            parser=Repo.detect,
        ),
    ] = '.',
) -> None:
    if kind_or_name in Versioned.semantic_increment:
        name = semver(repository.get_next_version(kind_or_name))
    else:
        name = kind_or_name
    subprocess.run([
        'git', '-C', repository.location, 'tag', '-a', name,
        '-m', '', *context.args]
    )


if __name__ == '__main__':
    app()
