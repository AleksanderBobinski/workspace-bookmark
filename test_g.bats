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

@test "exit gracefully when not in a workspace" {
	cd "$DIR"

  run g

  exit_message="$(cat << EOF
Warning: There is no .repo directory in or above the current directory.
This tool is intended to work in different workspaces that have a common
layout as is often the case with workspaces downloaded by repo. If this
is not your use-case switch to autojump-rs or propose an improvement to
this script.
EOF
)"
  echo "expected message: $exit_message"
  echo "  actual message: $output"
  [ "$exit_message" = "$output" ]
	echo "expected return code: 1"
	echo "  actual return code: $status"
	[ 1 -eq "$status" ]
}