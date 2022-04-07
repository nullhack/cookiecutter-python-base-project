# -*- coding: utf-8 -*-
"""Nox file used to run default routines."""

from pathlib import Path

import nox

nox.options.sessions = ["pre-commit"]


@nox.session(python=False, name="tests")
def tests(session):
    """Run default tests."""
    session.run("poetry", "run", "pytest")


@nox.session(python=False, name="pre-commit")
def pre_commit(session):
    """Run pre-commit checks."""
    session.run("poetry", "run", "pre-commit", "run", "--all-files")


@nox.session(python=False, name="black")
def black(session):
    """Fix code structure using black."""
    session.run("poetry", "run", "black", "src", "tests", "noxfile.py")


@nox.session(python=False, name="lint")
def lint(session):
    """Check styling using Flake8 and external packages."""
    session.run("poetry", "run", "flake8")


@nox.session(python=False, name="uml")
def uml(session):
    """Generate UML diagrams."""
    p = Path(r"src").glob("*")
    folders = [x for x in p if x.is_dir()]
    for folder in folders:
        package_name = folder.name
        session.run(
            "poetry",
            "run",
            "pyreverse",
            "-ASmy",
            package_name,
            "-d",
            "docs/uml/artifacts",
            "-p",
            package_name,
        )
        session.run(
            "poetry",
            "run",
            "pyreverse",
            "-ASmy",
            package_name,
            "-d",
            "docs/uml/diagrams",
            "-p",
            package_name,
            "-o",
            "png",
        )


@nox.session(python=False, name="test-docs")
def test_docs(session):
    """Run default tests."""
    session.run(
        "poetry",
        "run",
        "pytest",
        "--html=docs/pytest_report.html",
        "--self-contained-html",
    )


@nox.session(python=False, name="api-docs")
def api_docs(session):
    """Generate API documentation using docstrings and pdoc3."""
    session.run(
        "poetry",
        "run",
        "pdoc",
        "--html",
        ".",
        "--force",
        "--output-dir",
        "docs/api",
    )