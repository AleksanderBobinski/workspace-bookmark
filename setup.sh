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

# https://askubuntu.com/questions/68175/how-to-create-script-with-auto-complete
_g()
{
  possible_destinations=$(echo "$WORKSPACE_BOOKMARKS" | jq --sort-keys 'keys' | sed -E 's/\[|\]/ /g' | tr '"' ' ' | tr ',' ' ')

  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  COMPREPLY=( $(compgen -W "${possible_destinations}" -- ${cur}) )

  return 0
}
complete -o nospace -F _g g
