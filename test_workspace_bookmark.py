#!/usr/bin/env python3
"""
Test the functionality of workspace-bookmark.

A child program cannot change it's parent's location but a bash trick can be
used to work around that.
g () { p=$(workspace-bookmark.py $1) && cd $p || echo $p; }
This function should be defined in the currently used shell and be called like
shown in the tests below.
"""
import os.path
from bin import workspace_bookmark

REPO_DIRECTORY = os.path.join(os.path.dirname(__file__), "test")
ANDROID_DIRECTORY = os.path.join(REPO_DIRECTORY, "android")


# Main function tests
def test_print_path_to_workspace_root_by_default(capsys):
    """
    By default print path to  directory which contains .repo.

    /test/android $ g
    /test $
    """
    os.chdir(ANDROID_DIRECTORY)
    workspace_bookmark.main()
    assert REPO_DIRECTORY == capsys.readouterr().out.strip()


# Unit tests
def test_get_path_to_workspace_root():
    """See if we can guess where the root of a workspace is."""
    os.chdir(ANDROID_DIRECTORY)
    path_to_root = workspace_bookmark.path_to("root")
    assert REPO_DIRECTORY == path_to_root
