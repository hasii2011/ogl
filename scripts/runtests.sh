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

    echo "checkStatus ${testName} -- ${status}"
    if [ "${status}" -ne 0 ]
    then
        exit "${status}"
    fi
}

function independentlyRunSomeTests {

  python3 -m unittest tests.miniogl.TestRectangleShape
  status=$?
  checkStatus ${status} TestRectangleShape

  python3 -m unittest tests.ogl.TestOglInterface2
  status=$?
  checkStatus ${status} TestOglInterface2

  python3 -m unittest tests.ogl.TestLinkRepr
  status=$?
  checkStatus ${status} TestLinkRepr
}
changeToProjectRoot

echo "Travis Build directory: ${TRAVIS_BUILD_DIR}"

python3 -Wdefault -m tests.TestAll
status=$?

echo "Independently run some tests"
independentlyRunSomeTests

checkStatus ${status} TestAll
exit ${status}

