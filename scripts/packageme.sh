#!/bin/bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi
}

changeToProjectRoot

clear

python3 -m build --sdist --wheel

# Check package
twine check dist/*
