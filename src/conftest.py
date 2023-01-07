#!/usr/bin/env python3

"""Contains pytest fixtures which are globally available."""

import pytest


@pytest.fixture(name="workspace")
def construct_workspace(tmp_path):
    """Construct a workspace used for testing."""
    workspace_root = tmp_path
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
