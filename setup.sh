#!/bin/bash

# Define root variable
export PYUTILSROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYUTILSMOM="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"
export PYTHONPATH=${PYUTILSMOM}:$PYTHONPATH

# Locations
export PYUTILS_LHCBINFO=$PYUTILSROOT/LHCb
export PYUTILS_LATEX=$PYUTILSROOT/LHCb/latex
export PYUTILS_PROCESSING=$PYUTILSROOT/processing

# Aliases
alias addPID='python $PYUTILSROOT/nums/addPID.py'
alias submit='python $PYUTILSROOT/processing/submit.py'
