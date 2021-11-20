#!/usr/bin/env bats

function setup () {
  # get the containing directory of this file
  # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
  # as those will point to the bats executable's location or the preprocessed file respectively
  DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
  PATH="$DIR/bin:$PATH"
  load "./setup.sh"

  WORKSPACE_BOOKMARKS="$(jq -n \
                            --arg build "poky/build" \
                            '{build: $build}')"
  export WORKSPACE_BOOKMARKS
  echo "bookmarks: $WORKSPACE_BOOKMARKS"
  cd "./test/android" || exit 1
}

function teardown() {
  unset WORKSPACE_BOOKMARKS
  cd "$DIR" || exit 1
}

@test "goto workspace root by default when env is not set" {
  unset WORKSPACE_BOOKMARKS
  g

  expected_dir="$DIR/test"
  actual_dir="$(pwd)"
  echo "expected dir: $expected_dir"
  echo "  actual dir: $actual_dir"
  [ "$expected_dir" = "$actual_dir" ]
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
  g build

  expected_dir="$DIR/test/poky/build"
  actual_dir="$(pwd)"
  echo "expected dir: $expected_dir"
  echo "  actual dir: $actual_dir"
  [ "$expected_dir" = "$actual_dir" ]
}

@test "warn if WORKSPACE_BOOKMARKS is not set" {
  unset WORKSPACE_BOOKMARKS

  run g

  warning_message="$(cat << EOF
Warning: WORKSPACE_BOOKMARKS is not set.
Try setting it to something similar to this:
export WORKSPACE_BOOKMARKS='{
  "build": "poky/build",
  "android": "android",
  "manifest": ".repo/manifests"
}'
EOF
)"
  echo "$warning_message"
  echo "$output"
  [ "$warning_message" = "$output" ]
}