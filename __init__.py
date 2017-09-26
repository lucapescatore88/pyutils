import processing
import numbers
import db
import editing
import plotting
#from LHCb import LHCbStyle

import os, sys, glob

class loc : pass

loc.ROOT = os.getenv('PYUTILSROOT')
for d in glob.glob(loc.ROOT+'/*') :
    name = os.path.basename(d)
    if '.' in name : continue
    loc.__dict__[name.upper()] = d
loc.LATEX = loc.LHCB+'/latex'


