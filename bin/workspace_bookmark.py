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
import os
import sys
from typing import Dict, Optional


def path_to(destination: str,
            bookmarks: Optional[Dict[str, str]] = None) -> str:
    """Return path to desired destination based on a lookup table."""
    if bookmarks is None:
        bookmarks = {"root": "./"}
    if "root" not in bookmarks:
        bookmarks["root"] = "./"
    workspace_root = os.getcwd()
    while ".repo" not in os.listdir(workspace_root):
        workspace_root = "/".join(workspace_root.split("/")[:-1])
    path = os.path.join(workspace_root, bookmarks[destination])
    return os.path.abspath(path)


def main(destination: str = "") -> int:
    """
    Print path to destination directory.

    This is expected to be later picked up by cd.
    """
    if destination == "":
        # When g is called without parameters
        # $ g
        # The first parameter $1 is actually ""
        destination = "root"
    try:
        bookmarks = os.environ["WORKSPACE_BOOKMARKS"]
    except KeyError:
        bookmarks = json.dumps({"root": "./"})
        print("Warning: WORKSPACE_BOOKMARKS is not set.\n"
              "Try setting it to something similar to this:\n"
              "export WORKSPACE_BOOKMARKS='{\n"
              "  \"build\": \"poky/build\",\n"
              "  \"android\": \"android\",\n"
              "  \"manifest\": \".repo/manifests\"\n"
              "}'", file=sys.stderr)
    try:
        print(path_to(destination, json.loads(bookmarks)))
    except FileNotFoundError:
        print("Warning: There is no .repo directory in or above the current "
              "directory.\nThis tool is intended to work in different "
              "workspaces that have a common\nlayout as is often the case "
              "with workspaces downloaded by repo. If this\nis not your "
              "use-case switch to autojump-rs or propose an improvement to\n"
              "this script.",
              file=sys.stderr)
        return 1
    except KeyError:
        proposed_bookmarks = json.loads(bookmarks)
        proposed_bookmarks[destination] = "<YOUR PATH>"
        proposed_bookmarks = json.dumps(proposed_bookmarks, indent=2)
        print(f"Warning: There is no \"{destination}\" in WORKSPACE_BOOKMARKS."
              "\nTry setting it:\n"
              f"export WORKSPACE_BOOKMARKS='{proposed_bookmarks}'",
              file=sys.stderr,
              end="")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(*(sys.argv[1:])))
