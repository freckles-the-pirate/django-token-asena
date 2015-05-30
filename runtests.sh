#!/bin/bash
TESTDIR=$(pwd)/tests
RUNTESTS=$(pwd)/runtests.py
PYTHON=$(which python)
TESTCASE=$1
export DJANGO_MODE="test"

if [ ! -d "$TESTDIR" ]; then
    echo "`TESTDIR` path "'"$TESTDIR"'" does not exist."
fi;

echo "Entering $TESTDIR"
cd $TESTDIR
echo "EXECUTING: $PYTHON $RUNTESTS $TESTCASE"
$PYTHON $RUNTESTS $TESTCASE
echo "[DONE] $PYTHON $RUNTESTS $TESTCASE"