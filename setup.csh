## Define root variable
setenv PYUTILSROOT "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
setenv PYUTILSMOM "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd .. && pwd )"
setenv PYTHONPATH $PYUTILSMOM:$PYTHONPATH

# Locations

setenv PYUTILS_LHCBINFO $PYUTILSROOT/LHCb/
setenv PYUTILS_LATEX $PYUTILSROOT/LHCb/latex/
setenv PYUTILS_PROCESSING $PYUTILSROOT/processing/

# Aliases

alias addPID python $PYUTILSROOT/nums/addPID.py
alias submit python $PYUTILSROOT/processing/submit.py
