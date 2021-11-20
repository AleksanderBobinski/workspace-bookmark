#!/usr/bin/env sh

this_directory="$(dirname "$0")"
PATH="$PATH:$(readlink -m "$this_directory")/bin"
g () { p="$(workspace_bookmark.py "$1")" && cd "$p" || echo "$p"; }