#!/usr/bin/env sh

set -e
set -x


workspace_bookmark_dir="$(pwd)"
test_dir="$(mktemp --directory)"
cd "${test_dir}" && python3 -m pytest "${workspace_bookmark_dir}/src/test_workspace_bookmark.py"
