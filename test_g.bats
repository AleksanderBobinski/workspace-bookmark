#!/usr/bin/env bats

function setup () {
  # get the containing directory of this file
  # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
  # as those will point to the bats executable's location or the preprocessed file respectively
  DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
  # make executables in src/ visible to PATH
  PATH="$DIR/bin:$PATH"
  load "./setup.sh"
  cd "./test/android" || exit 1
}

function teardown() {
  cd "$DIR" || exit 1
}

@test "goto workspace root by default" {
  g

  expected_dir="$DIR/test"
  actual_dir="$(pwd)"
  echo "expected dir: $expected_dir"
  echo "  actual dir: $actual_dir"
  [ "$expected_dir" = "$actual_dir" ]
}

@test "goto specified destination directory" {
  WORKSPACE_BOOKMARKS="$(jq -n \
                            --arg build "poky/build" \
                            '{build: $build}')"
  export WORKSPACE_BOOKMARKS
  echo "bookmarks: $WORKSPACE_BOOKMARKS"

  g build

  expected_dir="$DIR/test/poky/build"
  actual_dir="$(pwd)"
  echo "expected dir: $expected_dir"
  echo "  actual dir: $actual_dir"
  [ "$expected_dir" = "$actual_dir" ]
}