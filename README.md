# Bookmark your .repo workspace (Android/YOCTO)

## Purpose

Provide an easier way to navigate a workspace created with repo than using `cd`.

The available tools to navigate quickly around the commands line are scripts
that set CDPATH and autojump (and z and v and fasd etc). Both are great but
their usability in specific use case can be bested.

In CDPATH if two directories contain a sub-directory of the same name the one
first in CDPATH will always be chosen. This is a no-go when frequently going to
many directories named "scripts".

Autojump is not predictable enough to make use of it in scripts. There is also
the fact that there can be multiple workspaces and autojump can jump into the
wrong one. The solution to that is to use jc but that would require one to be
in workspace root when calling it.

## Design

## Idea

This tool guesses the root of a workspace by looking for .repo and than based
on it's location jumps to a bookmark that is defined as a key: value pair. The
key being the name and the value being a path relative to the workspace root.

This is predictable since a workspace only has one .repo directory. It allows
to have two or more directories of the same name but different paths to be
bookmarked and will always jump the the correct directory inside the currently
used workspace regardless of where inside the workspace the caller is.

## Code

The tool is separated into two parts:

* `g` - the tool which calls cd
* `workspace_bookmarks.py` - the tool which provides an absolute path to jump to

## Usage

Things to put into your .bashrc or .zshrc:

```sh
source /path/to/setup.sh
export WORKSPACE_BOOKMARKS='{
  "build": "poky/build",
  "android": "android",
  "manifest": ".repo/manifests"
}'
```

Things to use daily:

```sh
cd some_workspace # with a .repo directory
some_workspace $ g manifest
some_workspace/.repo/manifests $ g android
some_workspace/android $ g
some_workspace $ g build
some_workspace/poky/build $ g android
some_workspace/android $ g poky/build # you can append paths relative to bookmark
some_workspace/poky/build $
```
