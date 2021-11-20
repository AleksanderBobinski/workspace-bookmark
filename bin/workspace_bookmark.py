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
import os
import sys


def path_to(destination: str) -> str:
    """Return path to desired destination based on a lookup table."""
    current_path = os.getcwd()
    while ".repo" not in os.listdir(current_path):
        current_path = "/".join(current_path.split("/")[:-1])
    return current_path


def main(destination: str = "root"):
    """
    Print path to destination directory.

    This is expected to be later picked up by cd.
    """
    print(path_to(destination))


if __name__ == "__main__":
    main(*(sys.argv[1:]))
