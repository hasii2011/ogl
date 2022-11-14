#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes --check-untyped-defs miniogl ogl tests
# mypy --config-file .mypi.ini --pretty  --show-error-codes org
status=$?

echo "Exit with status: ${status}"
exit ${status}

