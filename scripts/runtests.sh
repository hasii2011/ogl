#!/usr/bin/env bash

function changeToProjectRoot {

    areHere=$(basename "${PWD}")
    export areHere
    if [[ ${areHere} = "scripts" ]]; then
        cd ..
    fi

    if [[ ${areHere} = "src" ]]; then
        cd ..
    fi
}

function checkStatus {

    status=$1
    testName=$2

    # echo "checkStatus ${testName} -- ${status}"
    if [ "${status}" -ne 0 ]
    then
        exit "${status}"
    fi
}

function independentlyRunSomeTests {

  python3 -Wdefault -m unittest tests.miniogl.TestRectangleShape -q
  status=$?
  checkStatus ${status} TestRectangleShape

  python3 -Wdefault -m unittest tests.ogl.TestOglInterface2 -q
  status=$?
  checkStatus ${status} TestOglInterface2

  python3 -Wdefault -m unittest tests.ogl.TestLinkRepr -q
  status=$?
  checkStatus ${status} TestLinkRepr
}
changeToProjectRoot

python3 -Wdefault -m tests.TestAll
status=$?

echo "Independently run some tests"
independentlyRunSomeTests

checkStatus ${status} TestAll
exit ${status}

