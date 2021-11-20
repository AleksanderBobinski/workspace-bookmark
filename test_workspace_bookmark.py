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
from bin import workspace_bookmark

REPO_DIRECTORY = os.path.join(os.path.dirname(__file__), "test")
ANDROID_DIRECTORY = os.path.join(REPO_DIRECTORY, "android")
BUILD_DIRECTORY = os.path.join(REPO_DIRECTORY, "poky/build")


# Main function tests
def test_print_path_to_workspace_root_by_default(capsys):
    """
    By default print path to directory which contains .repo.

    /test/android $ g
    /test $
    """
    os.chdir(ANDROID_DIRECTORY)
    workspace_bookmark.main("")
    assert REPO_DIRECTORY == capsys.readouterr().out.strip()


def test_print_path_to_specified_destination(capsys):
    """
    Print path to specified directory based on a provided lookup table.

    The lookup table is a JSON file stored in the environment variable
    WORKSPACE_BOOKMARKS.
    """
    os.chdir(ANDROID_DIRECTORY)
    os.environ["WORKSPACE_BOOKMARKS"] = json.dumps({"build": "poky/build"})
    workspace_bookmark.main("build")
    assert BUILD_DIRECTORY == capsys.readouterr().out.strip()


# Unit tests
def test_get_path_to_workspace_root():
    """See if we can guess where the root of a workspace is."""
    os.chdir(ANDROID_DIRECTORY)
    path_to_root = workspace_bookmark.path_to("root", {"root": "./"})
    assert REPO_DIRECTORY == path_to_root


def test_get_path_to_specified_directory():
    """
    Make sure get_path returns a path to the directory specified as a parameter
    that is present in a lookup table.
    """
    os.chdir(ANDROID_DIRECTORY)
    bookmarks = {"build": "poky/build"}
    path_to_destination = workspace_bookmark.path_to(
                                                    destination="build",
                                                    bookmarks=bookmarks)
    assert BUILD_DIRECTORY == path_to_destination
