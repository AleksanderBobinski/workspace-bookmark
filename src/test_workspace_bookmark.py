#!/usr/bin/env python3
"""
Test the functionality of workspace-bookmark.

A child program cannot change it's parent's location but a bash trick can be
used to work around that.
g () { p=$(workspace-bookmark.py $1) && cd $p || echo $p; }
This function should be defined in the currently used shell and be called like
shown in the tests below.
"""
import json
import os.path
import pytest

import workspace_bookmark


@pytest.mark.parametrize(
    "_workspace_bookmarks_env",
    ["_set_workspace_bookmarks_env", "_no_workspace_bookmarks_env"],
)
def test_print_path_to_workspace_root_by_default(
    capsys,
    repo_workspace,
    _current_location_inside_repo_workspace,
    _workspace_bookmarks_env,
):
    """
    By default print path to directory which contains .repo.

    /test/android $ g
    /test $
    """
    workspace_bookmark.main("")
    assert str(repo_workspace) == capsys.readouterr().out.strip()


def test_print_path_to_specified_destination(
    capsys, _current_location_inside_repo_workspace, repo_workspace, build_directory
):
    """
    Print path to specified directory based on a provided lookup table.

    The lookup table is a JSON file stored in the environment variable
    WORKSPACE_BOOKMARKS.
    """
    os.environ["WORKSPACE_BOOKMARKS"] = json.dumps(
        {"build": str(build_directory.relative_to(repo_workspace))}
    )

    workspace_bookmark.main("build")

    assert str(build_directory) == capsys.readouterr().out.strip()


def test_print_path_to_specified_destination_any_beyond(
    capsys, _current_location_inside_repo_workspace, repo_workspace, build_directory
):
    """
    Print path to specified directory based on a provided lookup table while
    accounting for a path that is appended to the bookmark.

    For example:
    $ workspace_bookmark.py bookmark/some/path
    /abs/path/to/bookmark/some/path
    """
    poky_directory = build_directory.parent
    os.environ["WORKSPACE_BOOKMARKS"] = json.dumps(
        {"poky": str(poky_directory.relative_to(repo_workspace))}
    )
    destination_suffix = build_directory.relative_to(poky_directory)

    workspace_bookmark.main("poky/" + str(destination_suffix))

    assert str(build_directory) == capsys.readouterr().out.strip()


def test_print_warning_if_env_is_unset(capsys, _current_location_inside_repo_workspace):
    """
    Make sure to print a warning with instructions if the lookup table
    is not defined in WORKSPACE_BOOKMARKS.
    """
    del os.environ["WORKSPACE_BOOKMARKS"]
    workspace_bookmark.main("")
    warning_message = (
        "Warning: WORKSPACE_BOOKMARKS is not set.\n"
        + "Try setting it to something similar to this:\n"
        + "export WORKSPACE_BOOKMARKS='{\n"
        + '  "build": "poky/build",\n'
        + '  "android": "android",\n'
        + '  "manifest": ".repo/manifests"\n'
        + "}'"
    )
    assert warning_message == capsys.readouterr().err.strip()


def test_graceful_exit_if_not_in_workspace(
    capsys, _current_location_outside_any_workspace
):
    """
    Make sure to print a helpful error message if workspace root can't be
    found.
    """
    os.environ["WORKSPACE_BOOKMARKS"] = json.dumps({"build": "poky/build"})
    error_code = workspace_bookmark.main("")
    exit_message = (
        "Warning: There is no .repo directory in or above the current "
        "directory.\nThis tool is intended to work in different workspaces "
        "that have a common\nlayout as is often the case with workspaces "
        "downloaded by repo. If this\nis not your use-case switch to "
        "autojump-rs or propose an improvement to\nthis script."
    )
    assert exit_message == capsys.readouterr().err.strip()
    assert error_code == 1


def test_graceful_exit_if_destination_is_not_bookmarked(
    capsys, _current_location_inside_repo_workspace
):
    """
    Make sure to print a helpful error message if a chosen destination is not
    in WORKSPACE_BOOKMARKS.
    """
    bookmarks = {"build": "poky/build"}
    os.environ["WORKSPACE_BOOKMARKS"] = json.dumps(bookmarks)
    destination = "someplace"
    bookmarks[destination] = "<YOUR PATH>"
    exit_message = (
        f'Warning: There is no "{destination}" in WORKSPACE_BOOKMARKS.\n'
        "Try setting it:\n"
        f"export WORKSPACE_BOOKMARKS='{json.dumps(bookmarks, indent=2)}'"
    )

    error_code = workspace_bookmark.main(destination)

    assert exit_message == capsys.readouterr().err.strip()
    assert error_code == 2


# Unit tests
def test_get_path_to_workspace_root(
    repo_workspace, _current_location_inside_repo_workspace
):
    """See if we can guess where the root of a workspace is."""
    path_to_root = workspace_bookmark.path_to("root", {"root": "./"})
    assert str(repo_workspace) == path_to_root


def test_get_path_to_specified_directory(
    _current_location_inside_repo_workspace, repo_workspace, build_directory
):
    """
    Make sure get_path returns a path to the directory specified as a parameter
    that is present in a lookup table.
    """
    bookmarks = {"build": str(build_directory.relative_to(repo_workspace))}

    path_to_destination = workspace_bookmark.path_to(
        destination="build", bookmarks=bookmarks
    )

    assert str(build_directory) == path_to_destination


def test_use_magic_file_instead_of_repo(
    capsys,
    _current_location_inside_repo_workspace,
    magic_workspace,
    magic_directory,
    _workspace_bookmark_magic_file_env,
):
    """
    Search for a user defined magic file instead of .repo.

    In a pathological case where there are multiple .repo directories in a
    workspace search for a user specified magic file instead to determine where
    workspace root is located.
    """
    bookmarks = {"magic": str(magic_directory.relative_to(magic_workspace))}
    os.environ["WORKSPACE_BOOKMARKS"] = json.dumps(bookmarks)

    error_code = workspace_bookmark.main("magic")
    stdout = capsys.readouterr().out.strip()

    assert error_code == 0
    assert str(magic_directory) == stdout
