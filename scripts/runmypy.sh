#!/usr/bin/env bash

function changeToProjectRoot {

    export areHere=`basename ${PWD}`
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

mypy --config-file .mypi.ini --pretty --no-color-output --show-error-codes miniogl ogl
# mypy --config-file .mypi.ini --pretty  --show-error-codes org
status=$?

echo "Exit with status: ${status}"
exit ${status}

