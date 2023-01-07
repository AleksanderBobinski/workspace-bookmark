#!/usr/bin/env python3

"""Contains pytest fixtures which are globally available."""

import random
import string

import pytest


@pytest.fixture(name="workspace")
def construct_workspace(tmp_path):
    """Construct a workspace used for testing."""
    workspace_root = tmp_path / "ws"
    workspace_root.mkdir()
    repo = workspace_root / ".repo"
    repo.mkdir()
    android = workspace_root / "android"
    android.mkdir()
    poky = workspace_root / "poky"
    poky.mkdir()
    build = workspace_root / "poky" / "build"
    build.mkdir()
    return workspace_root


@pytest.fixture(name="REPO_DIRECTORY")
def get_workspace_root(workspace):
    """Return path to a workspace's root directory."""
    return str(workspace)


@pytest.fixture(name="ANDROID_DIRECTORY")
def get_android_directory(workspace):
    """Return path to a android directory."""
    return str(workspace / "android")


@pytest.fixture(name="POKY_DIRECTORY")
def get_poky_directory(workspace):
    """Return path to a poky directory."""
    return str(workspace / "poky")


@pytest.fixture(name="BUILD_DIRECTORY")
def get_build_directory(workspace):
    """Return path to a build directory."""
    return str(workspace / "poky/build")


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


@pytest.fixture(name="_current_location_outside_any_workspace")
def set_current_location_to_outside_any_workspace(monkeypatch, tmp_path):
    """Return path to random location outside workspace."""
    current_location = tmp_path / get_random_directory_name()
    current_location.mkdir(parents=True)
    monkeypatch.chdir(current_location)


@pytest.fixture(name="_current_location_inside_repo_workspace")
def set_current_location_to_inside_repo_workspace(monkeypatch, workspace):
    """Return path to random location inside workspace."""
    current_location = workspace / get_random_directory_name()
    current_location.mkdir(parents=True)
    monkeypatch.chdir(current_location)