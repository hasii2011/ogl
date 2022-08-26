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

  python3 -m unittest -v tests.miniogl.TestRectangleShape
  status=$?
  checkStatus ${status} TestRectangleShape

  python3 -m unittest -v tests.ogl.TestOglInterface2
  status=$?
  checkStatus ${status} TestOglInterface2

}
changeToProjectRoot

echo "Travis Build directory: ${TRAVIS_BUILD_DIR}"


echo "Independently run some tests"
independentlyRunSomeTests

python3 -m tests.TestAll
status=$?

cd -  > /dev/null 2>&1 || ! echo "No such directory"

checkStatus ${status} TestAll
exit ${status}

