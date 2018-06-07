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
alias submit='python $PYUTILSROOT/processing/submit.py'


#add pyxrootd
export PYTHONPATH=$PYTHONPATH:/cvmfs/lhcb.cern.ch/lib/lcg/releases/LCG_87/xrootd_python/0.3.0/x86_64-slc6-gcc49-opt/lib/python2.7/site-packages/
