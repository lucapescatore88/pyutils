import os, sys, glob

class loc : pass

root_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir,'..'))

loc.ROOT = root_dir
for d in glob.glob(loc.ROOT+'/*') :
    name = os.path.basename(d)
    if '.' in name : continue
    loc.__dict__[name.upper()] = d
loc.LATEX = loc.LHCB+'/latex'


# Import submodules
import processing
import numbers
import db
import editing
import plotting
#from LHCb import LHCbStyle
