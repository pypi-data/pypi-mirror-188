import pytest

from briefcase.commands.create import git
from briefcase.exceptions import BriefcaseCommandError


def test_no_git(update_command, monkeypatch):
    """If Git is not installed, an error is raised."""

    def monkeypatch_verify_git(*a, **kw):
        raise BriefcaseCommandError("Briefcase requires git, but it is not installed")

    monkeypatch.setattr(git, "verify_git_is_installed", monkeypatch_verify_git)

    # The command will fail tool verification.
    with pytest.raises(
        BriefcaseCommandError, match=r"Briefcase requires git, but it is not installed"
    ):
        update_command()


def test_update(update_command, first_app, second_app):
    """The update command can be called."""
    # Configure no command line options
    options = update_command.parse_options([])

    update_command(**options)

    # The right sequence of things will be done
    assert update_command.actions == [
        ("verify",),
        # Update the first app
        ("code", update_command.apps["first"], False),
        ("cleanup", update_command.apps["first"]),
        # Update the second app
        ("code", update_command.apps["second"], False),
        ("cleanup", update_command.apps["second"]),
    ]


def test_update_single(update_command, first_app, second_app):
    """The update command can be called to update a single app from the
    config."""
    # Configure no command line options
    options = update_command.parse_options([])

    update_command(app=update_command.apps["first"], **options)

    # The right sequence of things will be done
    assert update_command.actions == [
        ("verify",),
        # update the first app
        ("code", update_command.apps["first"], False),
        ("cleanup", update_command.apps["first"]),
    ]


def test_update_with_requirements(update_command, first_app, second_app):
    """The update command can be called, requesting a requirements update."""
    # Configure a requirements update
    options = update_command.parse_options(["-r"])

    update_command(**options)

    # The right sequence of things will be done
    assert update_command.actions == [
        ("verify",),
        # Update the first app
        ("code", update_command.apps["first"], False),
        ("requirements", update_command.apps["first"], False),
        ("cleanup", update_command.apps["first"]),
        # Update the second app
        ("code", update_command.apps["second"], False),
        ("requirements", update_command.apps["second"], False),
        ("cleanup", update_command.apps["second"]),
    ]


def test_update_with_resources(update_command, first_app, second_app):
    """The update command can be called, requesting a resources update."""
    # Configure no command line options
    options = update_command.parse_options(["--update-resources"])

    update_command(**options)

    # The right sequence of things will be done
    assert update_command.actions == [
        ("verify",),
        # Update the first app
        ("code", update_command.apps["first"], False),
        ("resources", update_command.apps["first"]),
        ("cleanup", update_command.apps["first"]),
        # Update the second app
        ("code", update_command.apps["second"], False),
        ("resources", update_command.apps["second"]),
        ("cleanup", update_command.apps["second"]),
    ]
