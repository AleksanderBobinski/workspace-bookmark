#!/usr/bin/env sh

set -e
set -x

black --check --diff ./src
flake8 ./src
find ./src -iregex '.*py' -print0 | xargs -n 1 -0 pylint
