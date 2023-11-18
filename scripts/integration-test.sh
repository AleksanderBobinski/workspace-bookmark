#!/usr/bin/env sh

set -e
set -x

workspace_bookmark_dir="$(pwd)"
test_dir="$(mktemp --directory)"
cd "${test_dir}" && "${workspace_bookmark_dir}/src/test_g.bats"
