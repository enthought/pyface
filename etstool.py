# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Tasks for Test Runs
===================

This file is intended to be used with a python environment with the
click library to automate the process of setting up test environments
and running the test within them.  This improves repeatability and
reliability of tests be removing many of the variables around the
developer's particular Python environment.  Test environment setup and
package management is performed using `EDM
http://docs.enthought.com/edm/`_

To use this to run you tests, you will need to install EDM and click
into your working environment.  You will also need to have git
installed to access required source code from github repositories.
You can then do::

    python etstool.py install --runtime=... --toolkit=...

to create a test environment from the current codebase and::

    python etstool.py test --runtime=... --toolkit=...

to run tests in that environment.  You can remove the environment with::

    python etstool.py cleanup --runtime=... --toolkit=...

If you need to make frequent changes to the source, it is often convenient
to install the source in editable mode::

    python etstool.py install --editable --runtime=... --toolkit=...

You can run all three tasks at once with::

    python etstool.py test_clean --runtime=... --toolkit=...

which will create, install, run tests, and then clean-up the environment.  And
you can run tests in all supported runtimes and toolkits (with cleanup)
using::

    python etstool.py test-all

Currently supported runtime values include ``3.6``, and currently
supported toolkits are ``null``, ``pyqt5``, ``pyside2`` and ``wx``.  Not all
combinations of toolkits and runtimes will work, but the tasks will fail with
a clear error if that is the case.

Tests can still be run via the usual means in other environments if that suits
a developer's purpose.

Changing This File
------------------

To change the packages installed during a test run, change the dependencies
variable below.  To install a package from github, or one which is not yet
available via EDM, add it to the `ci-src-requirements.txt` file (these will be
installed by `pip`).

Other changes to commands should be a straightforward change to the listed
commands for each task. See the EDM documentation for more information about
how to run commands within an EDM environment.

"""

import glob
import os
import subprocess
import sys
from shutil import rmtree, copy as copyfile
from tempfile import mkdtemp
from contextlib import contextmanager

import click

supported_combinations = {
    "3.6": {"pyqt5", "pyside2", "wx"},
}

# Traits version requirement (empty string to mean no specific requirement).
# The requirement is to be interpreted by EDM
TRAITS_VERSION_REQUIRES = os.environ.get("TRAITS_REQUIRES", "")

dependencies = {
    "importlib_metadata",
    "importlib_resources>=1.1.0",
    "traits" + TRAITS_VERSION_REQUIRES,
    "traitsui",
    "numpy",
    "pygments",
    "coverage",
    "pillow",
    "flake8",
    "flake8_ets",
}

source_dependencies = {
    "traits": "git+http://github.com/enthought/traits.git#egg=traits",
    "traitsui": "git+http://github.com/enthought/traitsui.git#egg=traitsui",
}

extra_dependencies = {
    # XXX once pyside2 is available in EDM, we will want it here
    "pyside2": set(),
    "pyqt5": {"pyqt5"},
    # XXX once wxPython 4 is available in EDM, we will want it here
    "wx": set(),
    "null": set(),
}

doc_dependencies = {
    "sphinx",
    "enthought_sphinx_theme",
}

doc_ignore = {
    "pyface/wx/*",
    "pyface/qt/*",
    "pyface/ui/*",
    "pyface/dock/*",
    "pyface/util/fix_introspect_bug.py",
    "pyface/grid/*",
    "*/tests",
}

environment_vars = {
    "pyside2": {"ETS_TOOLKIT": "qt4", "QT_API": "pyside2"},
    "pyqt5": {"ETS_TOOLKIT": "qt4", "QT_API": "pyqt5"},
    "wx": {"ETS_TOOLKIT": "wx"},
    "null": {"ETS_TOOLKIT": "null"},
}

# Options shared between the various commands.
edm_option = click.option(
    "--edm",
    help=(
        "Path to the EDM executable to use. The default is to use the first "
        "EDM found in the path. The EDM executable can also be specified "
        "by setting the ETSTOOL_EDM environment variable."
    ),
    envvar="ETSTOOL_EDM",
)


@click.group()
def cli():
    pass


@cli.command()
@edm_option
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--toolkit", default="pyqt5", help="Toolkit and API to use")
@click.option("--environment", default=None, help="EDM environment to use")
@click.option(
    "--editable/--not-editable",
    default=False,
    help="Install main package in 'editable' mode?  [default: --not-editable]",
)
@click.option('--source/--no-source', default=False)
def install(edm, runtime, toolkit, environment, editable, source):
    """ Install project and dependencies into a clean EDM environment.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    packages = " ".join(dependencies | extra_dependencies.get(toolkit, set()))

    # Install local source
    install_pyface = (
        "{edm} run -e {environment} -- "
        "pip install --no-deps --force-reinstall "
    )
    if editable:
        install_pyface += "--editable "
    install_pyface += "."

    # edm commands to setup the development environment
    if sys.platform == 'linux':
        commands = [
            "edm environments create {environment} --platform=rh6-x86_64 --force --version={runtime}",  # noqa: E501
        ]
    else:
        commands = [
            "edm environments create {environment} --force --version={runtime}"
        ]

    commands.extend([
        "{edm} install -y -e {environment} " + packages,
        "{edm} run -e {environment} -- pip install -r ci-src-requirements.txt --no-dependencies",  # noqa: E501
        "{edm} run -e {environment} -- python setup.py clean --all",
        install_pyface,
    ])

    # pip install pyqt5 and pyside2, because we don't have them in EDM yet
    if toolkit == "pyside2":
        commands.extend(
            [
                "{edm} run -e {environment} -- pip install shiboken2",
                "{edm} run -e {environment} -- pip install pyside2",
            ]
        )
    elif toolkit == "wx":
        if sys.platform == "darwin":
            commands.append(
                "{edm} run -e {environment} -- python -m pip install wxPython<4.1"  # noqa: E501
            )
        elif sys.platform == "linux":
            # XXX this is mainly for TravisCI workers; need a generic solution
            commands.append(
                "{edm} run -e {environment} -- pip install -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04/ wxPython<4.1"  # noqa: E501
            )
        else:
            commands.append(
                "{edm} run -e {environment} -- python -m pip install wxPython"
            )

    click.echo("Creating environment '{environment}'".format(**parameters))
    execute(commands, parameters)

    if source:
        cmd_fmt = (
            "edm plumbing remove-package --environment {environment} --force "
        )
        commands = [
            cmd_fmt+dependency for dependency in source_dependencies.keys()
        ]
        execute(commands, parameters)
        source_pkgs = source_dependencies.values()
        commands = [
            "python -m pip install {pkg} --no-deps".format(pkg=pkg)
            for pkg in source_pkgs
        ]
        commands = [
            "edm run -e {environment} -- " + command for command in commands
        ]
        execute(commands, parameters)

    click.echo("Done install")


@cli.command()
@edm_option
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--toolkit", default="pyqt5", help="Toolkit and API to use")
@click.option("--environment", default=None, help="EDM environment to use")
def shell(edm, runtime, toolkit, environment):
    """ Create a shell into the EDM development environment
    (aka 'activate' it).

    """
    parameters = get_parameters(edm ,runtime, toolkit, environment)
    commands = [
        "{edm} shell -e {environment}",
    ]
    execute(commands, parameters)


@cli.command()
@edm_option
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--toolkit", default="pyqt5", help="Toolkit and API to use")
@click.option("--environment", default=None, help="EDM environment to use")
@click.option(
    "--no-environment-vars",
    is_flag=True,
    help="Do not set ETS_TOOLKIT and QT_API",
)
def test(edm, runtime, toolkit, environment, no_environment_vars=False):
    """ Run the test suite in a given environment with the specified toolkit.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    if toolkit == "wx":
        parameters["exclude"] = "qt"
    elif toolkit in {"pyqt5", "pyside2"}:
        parameters["exclude"] = "wx"
    else:
        parameters["exclude"] = "(wx|qt)"

    if no_environment_vars:
        environ = {}
    else:
        environ = environment_vars.get(toolkit, {}).copy()
    environ["PYTHONUNBUFFERED"] = "1"

    if toolkit == "wx":
        environ["EXCLUDE_TESTS"] = "qt"
    elif toolkit in {"pyqt5", "pyside2"}:
        environ["EXCLUDE_TESTS"] = "wx"
    else:
        environ["EXCLUDE_TESTS"] = "(wx|qt)"

    commands = [
        "{edm} run -e {environment} -- python -Xfaulthandler -m coverage run -p -m "
        "unittest discover -v pyface",
    ]

    # We run in a tempdir to avoid accidentally picking up wrong pyface
    # code from a local dir.  We need to ensure a good .coveragerc is in
    # that directory, plus coverage has a bug that means a non-local coverage
    # file doesn't get populated correctly.
    click.echo("Running tests in '{environment}'".format(**parameters))
    with do_in_tempdir(
        files=[".coveragerc"], capture_files=[os.path.join(".", ".coverage*")]
    ):
        os.environ.update(environ)
        execute(commands, parameters)
    click.echo("Done test")


@cli.command()
@edm_option
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--toolkit", default="pyqt5", help="Toolkit and API to use")
@click.option("--environment", default=None, help="EDM environment to use")
def cleanup(edm, runtime, toolkit, environment):
    """ Remove a development environment.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    commands = [
        "{edm} run -e {environment} -- python setup.py clean",
        "{edm} environments remove {environment} --purge -y",
    ]
    click.echo("Cleaning up environment '{environment}'".format(**parameters))
    execute(commands, parameters)
    click.echo("Done cleanup")


@cli.command()
@edm_option
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--toolkit", default="pyqt5", help="Toolkit and API to use")
@click.option(
    "--no-environment-vars",
    is_flag=True,
    help="Do not set ETS_TOOLKIT and QT_API",
)
def test_clean(edm, runtime, toolkit, no_environment_vars=False):
    """ Run tests in a clean environment, cleaning up afterwards

    """
    args = ["--toolkit={}".format(toolkit), "--runtime={}".format(runtime)]
    if edm is not None:
        args.append("--edm={}".format(edm))

    test_args = args[:]
    if no_environment_vars:
        test_args.append("--no-environment-vars")

    try:
        install(args=args, standalone_mode=False)
        test(args=test_args, standalone_mode=False)
    finally:
        cleanup(args=args, standalone_mode=False)


@cli.command()
@edm_option
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--toolkit", default="pyqt5", help="Toolkit and API to use")
@click.option("--environment", default=None, help="EDM environment to use")
def update(edm, runtime, toolkit, environment):
    """ Update/Reinstall package into environment.

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    commands = ["{edm} run -e {environment} -- python setup.py install"]
    click.echo("Re-installing in  '{environment}'".format(**parameters))
    execute(commands, parameters)
    click.echo("Done update")


@cli.command()
@edm_option
@click.option("--runtime", default="3.6", help="Python version to use")
@click.option("--toolkit", default="pyqt5", help="Toolkit and API to use")
@click.option("--environment", default=None, help="EDM environment to use")
def docs(edm, runtime, toolkit, environment):
    """ Autogenerate documentation

    """
    parameters = get_parameters(edm, runtime, toolkit, environment)
    packages = " ".join(doc_dependencies)
    ignore = " ".join(doc_ignore)
    commands = [
        "{edm} install -y -e {environment} " + packages,
        "{edm} run -e {environment} -- pip install -r doc-src-requirements.txt --no-dependencies",  # noqa: E501
    ]
    click.echo(
        "Installing documentation tools in  '{environment}'".format(
            **parameters
        )
    )
    execute(commands, parameters)
    click.echo("Done installing documentation tools")

    click.echo(
        "Regenerating API docs in  '{environment}'".format(**parameters)
    )
    api_path = os.path.join("docs", "source", "api")
    if os.path.exists(api_path):
        rmtree(api_path)
    os.makedirs(api_path)
    commands = [
        "{edm} run -e {environment} -- sphinx-apidoc -e -M -o "
        + api_path
        + " pyface "
        + ignore
    ]
    execute(commands, parameters)
    click.echo("Done regenerating API docs")

    os.chdir("docs")
    command = (
        "{edm} run -e {environment} -- sphinx-build -b html "
        "-d build/doctrees "
        "source "
        "build/html"
    )
    click.echo(
        "Building documentation in  '{environment}'".format(**parameters)
    )
    try:
        execute([command], parameters)
    finally:
        os.chdir("..")
    click.echo("Done building documentation")


@cli.command()
@edm_option
def test_all(edm):
    """ Run test_clean across all supported environment combinations.

    """
    error = False
    for runtime, toolkits in supported_combinations.items():
        for toolkit in toolkits:
            args = [
                "--toolkit={}".format(toolkit),
                "--runtime={}".format(runtime),
            ]
            if edm is not None:
                args.append("--edm={}".format(edm))

            try:
                test_clean(args, standalone_mode=True)
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    error = True
                    click.echo(str(exc))

    if error:
        sys.exit(1)


@cli.command()
@edm_option
@click.option('--runtime', default="3.6")
@click.option('--toolkit', default="pyqt5")
@click.option(
    "--environment", default=None, help="Name of EDM environment to check."
)
@click.option(
    '--strict/--not-strict',
    default=False,
    help="Use strict configuration for flake8 [default: --not-strict]",
)
def flake8(edm, runtime, toolkit, environment, strict):
    """Run a flake8 check in a given environment."""
    parameters = get_parameters(edm, runtime, toolkit, environment)
    config = ""
    if strict:
        config = "--config=flake8_strict.cfg "
    commands = [
        "edm run -e {environment} -- python -m flake8 " + config,
    ]
    execute(commands, parameters)


# ----------------------------------------------------------------------------
# Utility routines
# ----------------------------------------------------------------------------


def get_parameters(edm, runtime, toolkit, environment):
    """ Set up parameters dictionary for format() substitution """
    parameters = {
        "runtime": runtime,
        "toolkit": toolkit,
        "environment": environment,
    }
    if toolkit not in supported_combinations[runtime]:
        msg = (
            "Python {runtime} and toolkit {toolkit} not supported by "
            + "test environments"
        )
        raise RuntimeError(msg.format(**parameters))
    if environment is None:
        parameters["environment"] = "pyface-test-{runtime}-{toolkit}".format(
            **parameters
        )
    if edm is None:
        edm = locate_edm()
    parameters["edm"] = edm

    return parameters


@contextmanager
def do_in_tempdir(files=(), capture_files=()):
    """ Create a temporary directory, cleaning up after done.

    Creates the temporary directory, and changes into it.  On exit returns to
    original directory and removes temporary dir.

    Parameters
    ----------
    files : sequence of filenames
        Files to be copied across to temporary directory.
    capture_files : sequence of filenames
        Files to be copied back from temporary directory.
    """
    path = mkdtemp()
    old_path = os.getcwd()

    # send across any files we need
    for filepath in files:
        click.echo("copying file to tempdir: {}".format(filepath))
        copyfile(filepath, path)

    os.chdir(path)
    try:
        yield path
        # retrieve any result files we want
        for pattern in capture_files:
            for filepath in glob.iglob(pattern):
                click.echo("copying file back: {}".format(filepath))
                copyfile(filepath, old_path)
    finally:
        os.chdir(old_path)
        rmtree(path)


def execute(commands, parameters):
    for command in commands:
        click.echo("[EXECUTING] {}".format(command.format(**parameters)))
        try:
            subprocess.check_call(
                [arg.format(**parameters) for arg in command.split()]
            )
        except subprocess.CalledProcessError as exc:
            print(exc)
            sys.exit(1)


def locate_edm():
    """
    Locate an EDM executable if it exists, else raise an exception.

    Returns the first EDM executable found on the path. On Windows, if that
    executable turns out to be the "edm.bat" batch file, replaces it with the
    executable that it wraps: the batch file adds another level of command-line
    mangling that interferes with things like specifying version restrictions.

    Returns
    -------
    edm : str
        Path to the EDM executable to use.

    Raises
    ------
    click.ClickException
        If no EDM executable is found in the path.
    """
    # Once Python 2 no longer needs to be supported, we should use
    # shutil.which instead.
    which_cmd = "where" if sys.platform == "win32" else "which"
    try:
        cmd_output = subprocess.check_output([which_cmd, "edm"])
    except subprocess.CalledProcessError:
        raise click.ClickException(
            "This script requires EDM, but no EDM executable was found."
        )

    # Don't try to be clever; just use the first candidate.
    edm_candidates = cmd_output.decode("utf-8").splitlines()
    edm = edm_candidates[0]

    # Resolve edm.bat on Windows.
    if sys.platform == "win32" and os.path.basename(edm) == "edm.bat":
        edm = os.path.join(os.path.dirname(edm), "embedded", "edm.exe")

    return edm


if __name__ == "__main__":
    cli()
