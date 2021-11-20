#!/usr/bin/env bats

function setup () {
  # get the containing directory of this file
  # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
  # as those will point to the bats executable's location or the preprocessed file respectively
  DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
  # make executables in src/ visible to PATH
  PATH="$DIR/bin:$PATH"
  load "./setup.sh"
}

function teardown() {
  cd "$DIR" || exit 1
}

@test "goto workspace root by default" {
  cd "./test/android"
  g
  expected_dir="$DIR/test"
  actual_dir="$(pwd)"
  echo "expected dir: $expected_dir"
  echo "  actual dir: $actual_dir"
  [ "$expected_dir" = "$actual_dir" ]
}