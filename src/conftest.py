#!/usr/bin/env python3

"""Contains pytest fixtures which are globally available."""

import random
import string

import pytest


def get_random_string(alphabet, length):
    """Return a random string of length using a specified alphabet."""
    return ''.join(random.choices(alphabet, k=length))


def get_random_directory_name():
    """Return a random directory name."""
    name_length = 20
    alphabet = string.ascii_letters + string.digits
    first_letter = get_random_string(alphabet, 1)
    random_directory_name = first_letter + \
        get_random_string(alphabet + "/", name_length - 1)
    return random_directory_name


@pytest.fixture(name="magic_filename")
def get_magic_filename():
    """Get name used for WORKSPACE_BOOKMARK_MAGIC_FILE but don't set env."""
    name_length = 20
    alphabet = string.ascii_letters + string.digits
    return get_random_string(alphabet, name_length)


@pytest.fixture(name="magic_workspace")
def construct_magic_workspace(tmp_path, magic_filename):
    """Construct an outer magic workspace used for testing."""
    magic_workspace_root = tmp_path / get_random_directory_name()
    magic_workspace_root.mkdir(parents=True)
    wsmagic = magic_workspace_root / magic_filename
    wsmagic.mkdir()
    return magic_workspace_root


@pytest.fixture(name="repo_workspace")
def construct_repo_workspace(magic_workspace):
    """Construct an inner .repo workspace used for testing."""
    repo_workspace_root = magic_workspace / get_random_directory_name()
    repo_workspace_root.mkdir(parents=True)
    repo = repo_workspace_root / ".repo"
    repo.mkdir()
    android = repo_workspace_root / "android"
    android.mkdir()
    poky = repo_workspace_root / "poky"
    poky.mkdir()
    build = repo_workspace_root / "poky" / "build"
    build.mkdir()
    return repo_workspace_root


@pytest.fixture(name="REPO_DIRECTORY")
def get_workspace_root(repo_workspace):
    """Return path to a workspace's root directory."""
    return str(repo_workspace)


@pytest.fixture(name="ANDROID_DIRECTORY")
def get_android_directory(repo_workspace):
    """Return path to a android directory."""
    return str(repo_workspace / "android")


@pytest.fixture(name="POKY_DIRECTORY")
def get_poky_directory(repo_workspace):
    """Return path to a poky directory."""
    return str(repo_workspace / "poky")


@pytest.fixture(name="BUILD_DIRECTORY")
def get_build_directory(repo_workspace):
    """Return path to a build directory."""
    return str(repo_workspace / "poky/build")


@pytest.fixture(name="_current_location_outside_any_workspace")
def set_current_location_to_outside_any_workspace(monkeypatch, tmp_path):
    """Return path to random location outside workspace."""
    current_location = tmp_path / get_random_directory_name()
    current_location.mkdir(parents=True)
    monkeypatch.chdir(current_location)


@pytest.fixture(name="_current_location_inside_repo_workspace")
def set_current_location_to_inside_repo_workspace(monkeypatch, repo_workspace):
    """Return path to random location inside workspace."""
    current_location = repo_workspace / get_random_directory_name()
    current_location.mkdir(parents=True)
    monkeypatch.chdir(current_location)
