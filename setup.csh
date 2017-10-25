#!/bin/tcsh

set EXE = "$0"
set EXE = `echo $EXE | sed s:"-"::`
set EXE = `basename $EXE`

setenv REPOSYS `readlink -f "$EXE"`
setenv REPOSYS `echo $REPOSYS | sed s:"/$EXE"::`
set STRINGS = "`ls -d $REPOSYS/*/ | sed s:"$REPOSYS/":: | sed s:"/"::`"
#set STRINGS = "$STRINGS `ls -d $REPOSYS/../*/ | sed s:"$REPOSYS/../":: | sed s:"/"::`"
foreach STRING ( $STRINGS )
    setenv REPOSYS `echo $REPOSYS | sed s:"/$STRING"::`
end

# Define root variable
setenv PYUTILSROOT $REPOSYS
setenv PYUTILSMOM `echo $PYUTILSROOT | sed s:"/pyutils"::`
setenv PYTHONPATH ${PYUTILSMOM}:$PYTHONPATH

# Locations
setenv PYUTILS_LHCBINFO $PYUTILSROOT/LHCb
setenv PYUTILS_LATEX $PYUTILSROOT/LHCb/latex
setenv PYUTILS_PROCESSING $PYUTILSROOT/processing

# Aliases
alias addPID python $PYUTILSROOT/nums/addPID.py
alias submit python $PYUTILSROOT/processing/submit.py