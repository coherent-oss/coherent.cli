import pathlib
import runpy
import subprocess
import sys
from typing_extensions import Annotated

import typer
from coherent.build import bootstrap
from jaraco.vcs import repo
from jaraco.versioning import semver


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
    tag_name: str,
    context: typer.Context,
    location: Annotated[str, typer.Option('-C', help='Path to repository.')] = '.',
) -> None:
    if tag_name in ('major', 'minor', 'patch'):
        tag_name = semver(repo(location).get_next_version(tag_name))
    subprocess.run(['git', '-C', location, 'tag', '-a', tag_name, *context.args])


if __name__ == '__main__':
    app()
