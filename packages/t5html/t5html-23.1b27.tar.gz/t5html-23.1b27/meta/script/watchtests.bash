#!/usr/bin/bash
HELP="
Executes in a continues loop pytest

USAGE:

    $0


an alternative is the test_on_modify.bash script.
"
SCRIPT_NEEDS=(bash watch pytest)


# Scripting Helpers
_abort()   { echo "$1"; exit 1; }
_trycmd()  { which $1 >/dev/null 2>&1; }


# Abort Script On Missing Arguments Or Required Programs 

    [ "$#" -gt 0 ] && _abort "$HELP"
    for CMD in ${SCRIPT_NEEDS[@]}; do
        _trycmd $CMD || PLEASE_INSTALL+="$CMD "
    done

    test -n "$PLEASE_INSTALL" \
        && _abort "Failed to check due to missing programs: $PLEASE_INSTALL" 

## restart pytest every 5 seconds
    watch -n5 pytest
# vi: et sw=4 ts=4 list

