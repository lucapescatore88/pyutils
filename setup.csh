#!/bin/tcsh

# Define root variable
set EXE = "$0"
set EXE = `echo $EXE | sed s:"-"::`
set EXE = `basename $EXE`
setenv PYUTILSROOT `readlink -f "$EXE"`
setenv PYUTILSROOT `echo $PYUTILSROOT | sed s:"/$EXE"::`
set STRINGS = "`ls -d $PYUTILSROOT/*/ | sed s:"$PYUTILSROOT/":: | sed s:"/"::`"
#set STRINGS = "$STRINGS `ls -d $PYUTILSROOT/../*/ | sed s:"$PYUTILSROOT/../":: | sed s:"/"::`"
foreach STRING ( $STRINGS )
    setenv PYUTILSROOT `echo $PYUTILSROOT | sed s:"/$STRING"::`
end
setenv PYUTILSMOM `echo $PYUTILSROOT | sed s:"/pyutils"::`
setenv PYTHONPATH ${PYUTILSMOM}:$PYTHONPATH

# Locations
setenv PYUTILS_LHCBINFO $PYUTILSROOT/LHCb
setenv PYUTILS_LATEX $PYUTILSROOT/LHCb/latex
setenv PYUTILS_PROCESSING $PYUTILSROOT/processing

# Aliases
alias addPID python $PYUTILSROOT/nums/addPID.py
alias submit python $PYUTILSROOT/processing/submit.py
