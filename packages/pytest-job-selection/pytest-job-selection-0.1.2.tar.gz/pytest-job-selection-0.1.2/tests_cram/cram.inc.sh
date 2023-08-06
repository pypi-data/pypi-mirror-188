#!/bin/sh

_pytest() {
    pytest "$@" \
        | grep -v 'tests collected in' \
        | grep -v 'tests ran in' \
        | grep -v ' passed in '
}
