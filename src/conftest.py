#!/usr/bin/env python3

"""Contains pytest fixtures which are globally available."""

import random
import os
import pathlib
import string

import pytest


def get_random_string(alphabet, length):
    """Return a random string of length using a specified alphabet."""
    return "".join(random.choices(alphabet, k=length))


def get_random_directory_name():
    """Return a random directory name."""
    name_length = 20
    alphabet = string.ascii_letters + string.digits
    first_letter = get_random_string(alphabet, 1)
    random_directory_name = first_letter + get_random_string(
        alphabet + "/", name_length - 1
    )
    return random_directory_name


@pytest.fixture(name="magic_filename")
def get_magic_filename():
    """Get name used for WORKSPACE_BOOKMARK_MAGIC_FILE but don't set env."""
    name_length = 20
    alphabet = string.ascii_letters + string.digits
    return get_random_string(alphabet, name_length)


@pytest.fixture(name="bookmark")
def get_bookmark():
    """Return a random bookmark as a str:str pair."""
    alphabet = string.ascii_letters + string.digits
    name_length = 20
    bookmark = {get_random_string(alphabet, name_length): get_random_directory_name()}
    return bookmark


@pytest.fixture
def existing_prefixed_path_bookmark_path(repo_workspace_root):
    """
    Return a path to an existing directory inside a repo workspace.

    The reason to have the directory nested at least three times is that the first
    two subdirectories are supposed to be wrapped inside an optional prefix.
    """
    return (
        repo_workspace_root
        / get_random_directory_name()
        / get_random_directory_name()
        / get_random_directory_name()
    )


@pytest.fixture
def not_existing_prefixed_path_bookmark_backup_path(repo_workspace_root):
    """
    Return a path to an existing directory inside a repo workspace.

    This path is supposed to be extended to include an non-existent optional prefix.
    This path is supposed to be a valid fallback for when it becomes that the path
    with an optional prefix included doesn't exist.
    """
    return repo_workspace_root / get_random_directory_name()


@pytest.fixture
def repo_workspace_root(magic_workspace):
    """Return a path to a repo workspace inside a magic workspace."""
    return magic_workspace / get_random_directory_name()


@pytest.fixture
def existing_prefixed_path_bookmark(
    existing_prefixed_path_bookmark_path, repo_workspace_root
):
    """Return a random bookmark with a prefixed path as a str:str pair."""
    alphabet = string.ascii_letters + string.digits
    name_length = 20
    bookmark_name = get_random_string(alphabet, name_length)
    prefixed_path = "{" + str(
        os.path.relpath(existing_prefixed_path_bookmark_path, repo_workspace_root)
    )
    second_nested_dir = prefixed_path.find("/") + 1
    prefixed_path = prefixed_path[:second_nested_dir] + prefixed_path[
        second_nested_dir:
    ].replace("/", "/}", 1)

    return {bookmark_name: prefixed_path}


@pytest.fixture
def not_existing_prefixed_path_bookmark_backup(
    not_existing_prefixed_path_bookmark_backup_path, repo_workspace_root
):
    """
    Return a path to a repo workspace inside a magic workspace.

    The prefixed path doesn't exist but the backup path, the one
    without the prefix does exist.
    """
    alphabet = string.ascii_letters + string.digits
    name_length = 20
    bookmark_name = get_random_string(alphabet, name_length)
    prefixed_path = (
        "{"
        + get_random_directory_name()
        + "/}"
        + str(
            os.path.relpath(
                not_existing_prefixed_path_bookmark_backup_path, repo_workspace_root
            )
        )
    )
    return {bookmark_name: prefixed_path}


@pytest.fixture(name="_workspace_bookmark_magic_file_env")
def set_workspace_bookmark_magic_file_environment(monkeypatch, magic_filename):
    """Set WORKSPACE_BOOKMARK_MAGIC_FILE."""
    monkeypatch.setenv("WORKSPACE_BOOKMARK_MAGIC_FILE", magic_filename)


@pytest.fixture(name="magic_workspace")
def construct_magic_workspace(tmp_path, magic_filename):
    """Construct an outer magic workspace used for testing."""
    magic_workspace_root = tmp_path / get_random_directory_name()
    magic_workspace_root.mkdir(parents=True)
    wsmagic = magic_workspace_root / magic_filename
    wsmagic.mkdir()
    return magic_workspace_root


@pytest.fixture(name="magic_directory")
def get_magic_file_directory(magic_workspace, magic_filename):
    """Return path to a workspace's magic directory."""
    return magic_workspace / magic_filename


@pytest.fixture(name="repo_workspace")
def construct_repo_workspace(
    magic_workspace,
    bookmark,
    existing_prefixed_path_bookmark_path,
    not_existing_prefixed_path_bookmark_backup_path,
    repo_workspace_root,
):
    """Construct an inner .repo workspace used for testing based on bookmarks."""
    repo_workspace_root.mkdir(parents=True)
    repo = repo_workspace_root / ".repo"
    repo.mkdir()
    android = repo_workspace_root / "android"
    android.mkdir()
    poky = repo_workspace_root / "poky"
    poky.mkdir()
    build = repo_workspace_root / "poky" / "build"
    build.mkdir()
    for path in bookmark.values():
        pathlib.Path(repo_workspace_root / path).mkdir(parents=True)
    existing_prefixed_path_bookmark_path.mkdir(parents=True)
    not_existing_prefixed_path_bookmark_backup_path.mkdir(parents=True)

    return repo_workspace_root


@pytest.fixture(name="build_directory")
def get_build_directory(repo_workspace):
    """Return path to a build directory."""
    return repo_workspace / "poky/build"


@pytest.fixture(name="_cwd_outside_any_workspace")
def set_current_location_to_outside_any_workspace(monkeypatch, tmp_path):
    """Return path to random location outside workspace."""
    current_location = tmp_path / get_random_directory_name()
    current_location.mkdir(parents=True)
    monkeypatch.chdir(current_location)


@pytest.fixture(name="_cwd_inside_repo_workspace")
def set_current_location_to_inside_repo_workspace(monkeypatch, repo_workspace):
    """Return path to random location inside workspace."""
    current_location = repo_workspace / get_random_directory_name()
    current_location.mkdir(parents=True)
    monkeypatch.chdir(current_location)


@pytest.fixture(name="_set_workspace_bookmarks_env")
def set_workspace_bookmarks_env(monkeypatch):
    """Set WORKSPACE_BOOKMARKS environment variable."""
    monkeypatch.setenv("WORKSPACE_BOOKMARKS", "{}")


@pytest.fixture(name="_no_workspace_bookmarks_env")
def remove_workspace_bookmarks_env(monkeypatch):
    """Make sure WORKSPACE_BOOKMARKS environment variable is not set."""
    monkeypatch.delenv("WORKSPACE_BOOKMARKS")
