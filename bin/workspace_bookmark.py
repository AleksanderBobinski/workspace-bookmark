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


def main(destination: str = "root"):
    """
    Print path to destination directory.

    This is expected to be later picked up by cd.
    """
    if destination == "":
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
    print(path_to(destination, json.loads(bookmarks)))


if __name__ == "__main__":
    main(*(sys.argv[1:]))
