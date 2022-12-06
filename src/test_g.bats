#!/usr/bin/env bats

bats_require_minimum_version 1.5.0

function setup () {
  # get the containing directory of this file
  # use $BATS_TEST_FILENAME instead of ${BASH_SOURCE[0]} or $0,
  # as those will point to the bats executable's location or the preprocessed file respectively
  DIR="$( cd "$( dirname "$BATS_TEST_FILENAME" )" >/dev/null 2>&1 && pwd )"
  PATH="$DIR/bin:$PATH"
  load "./setup.sh"

  WORKSPACE_BOOKMARKS="$(jq -n \
                            --arg build "poky/build" \
                            --arg poky "poky" \
                            '{poky: $poky, build: $build}')"
  export WORKSPACE_BOOKMARKS
  echo "bookmarks: $WORKSPACE_BOOKMARKS"
  mkdir -p "$DIR/test/android" \
           "$DIR/test/poky/build" \
           "$DIR/test/.repo/manifests"
  cd "$DIR/test/android" || exit 1
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

@test "exit gracefully when destination is not in bookmarks" {
  dummy_destination="the moon"
  proposed_fix="$(echo ''"${WORKSPACE_BOOKMARKS}" '{'\""$dummy_destination"\": \"\<YOUR PATH\>\"'}''' | jq -s add)"
  exit_message="$(cat <<EOF
Warning: There is no "$dummy_destination" in WORKSPACE_BOOKMARKS.
Try setting it:
export WORKSPACE_BOOKMARKS='$proposed_fix'
EOF
)"

  run g "$dummy_destination"

  echo "expected message: $exit_message"
  echo "  actual message: $output"
  [ "$exit_message" = "$output" ]
	echo "expected return code: 2"
	echo "  actual return code: $status"
	[ 2 -eq "$status" ]
  expected_dir="$DIR/test/android"
  actual_dir="$(pwd)"
  echo "expected dir: $expected_dir"
  echo "  actual dir: $actual_dir"
  [ "$expected_dir" = "$actual_dir" ]
}

@test "do nothing when destination path does not exist" {
  # cd will print an error message, that's enough.
  dummy_destination="the moon"
  WORKSPACE_BOOKMARKS="$(jq -n \
                            --arg the_moon "non-existant" \
                            '{"the moon": $the_moon}')"
  export WORKSPACE_BOOKMARKS
  function run_and_grab_pwd () {
    g "$dummy_destination"
    pwd
  }

  run ! g "$dummy_destination"
  run run_and_grab_pwd
  actual_dir="$(echo "$output" | tail -n 1)"

  expected_dir="$DIR/test/android"
  echo "expected dir: $expected_dir"
  echo "  actual dir: $actual_dir"
  [ "$expected_dir" = "$actual_dir" ]
}

@test "goto specified destination directory and beyond" {
  g poky/build

  expected_dir="$DIR/test/poky/build"
  actual_dir="$(pwd)"
  echo "expected dir: $expected_dir"
  echo "  actual dir: $actual_dir"
  [ "$expected_dir" = "$actual_dir" ]
}
