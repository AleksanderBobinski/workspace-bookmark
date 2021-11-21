#!/usr/bin/env sh

this_directory="$(dirname "$0")"
PATH="$PATH:$(readlink -m "$this_directory")/bin"
g () { 
	p="$(workspace_bookmark.py "$1")";
	e=$?;
	if [ $e -eq 0 ]
	then 
		cd "$p" || return $?
	else 
		echo "$p";
	fi
	return $e;
}