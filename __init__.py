from processing import *
from nums import *
from db import *
from editing import *
from plotting import *
from LHCb import LHCbStyle

import os, sys, glob

class loc : pass

loc.ROOT = os.path.dirname(os.path.realpath(__file__))
for d in glob.glob(loc.ROOT+'/*') :
    name = os.path.basename(d)
    if '.' in name : continue
    loc.__dict__[name.upper()] = d
loc.LATEX = loc.LHCB+'/latex'


