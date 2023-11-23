#!/usr/bin/env python3
"""
g - a utility to move around a .repo workspace more conveniently.

Example usage:
    g - goto workspace root
    g build - goto poky/build
    g android - goto android

This script works along with a function defined in .bashrc
g () { p=$(workspace-bookmark.py $1) && cd $p || echo $p; }
"""
import json
import copy
import re
import os
import sys
from typing import Dict


def path_to(
    destination: str, bookmarks: Dict[str, str], magic_file: str = ".repo"
) -> str:
    """Return path to desired destination based on a lookup table."""
    workspace_root = os.getcwd()
    while magic_file not in os.listdir(workspace_root):
        workspace_root = "/".join(workspace_root.split("/")[:-1])
    path = os.path.join(workspace_root, bookmarks[destination])
    return os.path.abspath(path)


def expand_optional_prefix(bookmarks: Dict[str, str]) -> Dict[str, str]:
    """
    The lookup table comes with paths which contain a special syntax '{}'.
    This syntax can only begin at the beginning of the path.
    The portion inside '{}' is optional. Expand the optional part by removing
    '{' and '}'. Thus creating a lookup table for preferred jump location.
    """
    bookmarks = copy.deepcopy(bookmarks)
    for bookmark, path in bookmarks.items():
        bookmarks[bookmark] = path.replace("{", "").replace("}", "")
    return bookmarks


def remove_optional_prefix(bookmarks: Dict[str, str]) -> Dict[str, str]:
    """
    Return bookmarks with but '{''}' and everything inside them removed. This creates
    a backup lookup table in case the preferred location is not found.
    """
    bookmarks = copy.deepcopy(bookmarks)
    for bookmark, path in bookmarks.items():
        bookmarks[bookmark] = re.sub("{.*}", "", path)
    return bookmarks


class WorkspaceRootNotFoundError(Exception):
    """This error is thrown when .repo or WORKSPACE_BOOKMARK_MAGIC_FILE is not found."""


class BookmarkNotFoundError(Exception):
    """This error is thrown when the requested bookmark is not found."""


def get_bookmarked_path(desired_destination: str = "") -> str:
    """
    Print path to destination directory.

    This is expected to be later picked up by cd.
    """
    default_destination = {"root": "./"}
    try:
        magic_file = os.environ["WORKSPACE_BOOKMARK_MAGIC_FILE"]
    except KeyError:
        magic_file = ".repo"
    try:
        bookmarks = os.environ["WORKSPACE_BOOKMARKS"]
    except KeyError:
        bookmarks = json.dumps(default_destination)
        print(
            "Warning: WORKSPACE_BOOKMARKS is not set.\n"
            "Try setting it to something similar to this:\n"
            "export WORKSPACE_BOOKMARKS='{\n"
            '  "build": "poky/build",\n'
            '  "android": "android",\n'
            '  "manifest": ".repo/manifests"\n'
            "}'",
            file=sys.stderr,
        )
    if desired_destination == "":
        # When g is called without parameters
        # $ g
        # The first parameter $1 is actually ""
        desired_destination = list(default_destination)[0]
        overwritten_bookmarks = json.loads(bookmarks)
        overwritten_bookmarks[desired_destination] = default_destination[
            desired_destination
        ]
        bookmarks = json.dumps(overwritten_bookmarks)

    # There are many edge cases here but none of them are considered.
    # 1. Bookmark has a '/' in it's name.
    # 2. There are two or more bookmarks named "one" and "one/one".
    # 3. A bookmark is in the path destination_bookmark/path/bookmark/
    bookmark_path = desired_destination.split("/")
    if len(bookmark_path) > 1:
        path_to_append = "/" + "/".join(bookmark_path[1:])
    else:
        path_to_append = ""
    desired_destination = bookmark_path[0]
    preferred_bookmarks = expand_optional_prefix(json.loads(bookmarks))
    backup_bookmarks = remove_optional_prefix(json.loads(bookmarks))
    try:
        resulting_destination = path_to(
            desired_destination, preferred_bookmarks, magic_file
        )
        if not os.path.isdir(resulting_destination):
            resulting_destination = path_to(
                desired_destination, backup_bookmarks, magic_file
            )
        final_destination = resulting_destination + path_to_append
        return final_destination
    except FileNotFoundError as exception:
        print(
            "Warning: There is no .repo directory in or above the current "
            "directory.\nThis tool is intended to work in different "
            "workspaces that have a common\nlayout as is often the case "
            "with workspaces downloaded by repo. If this\nis not your "
            "use-case switch to autojump-rs or propose an improvement to\n"
            "this script.",
            file=sys.stderr,
        )
        raise WorkspaceRootNotFoundError() from exception
    except KeyError as exception:
        proposed_bookmarks = json.loads(bookmarks)
        proposed_bookmarks[desired_destination] = "<YOUR PATH>"
        proposed_bookmarks = json.dumps(proposed_bookmarks, indent=2)
        print(
            f'Warning: There is no "{desired_destination}" in WORKSPACE_BOOKMARKS.'
            "\nTry setting it:\n"
            f"export WORKSPACE_BOOKMARKS='{proposed_bookmarks}'",
            file=sys.stderr,
            end="",
        )
        raise BookmarkNotFoundError from exception


def main(destination: str = ""):
    """Print out commands that after executing them will cd into the right place."""
    try:
        absolute_destination = get_bookmarked_path(destination)
        print(absolute_destination)
    except WorkspaceRootNotFoundError:
        return 1
    except BookmarkNotFoundError:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(*(sys.argv[1:])))
