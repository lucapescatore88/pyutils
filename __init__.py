import os, sys, glob

root_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(root_dir)
sys.path.append(os.path.join(root_dir,'..'))

class loc : pass
loc.ROOT = root_dir
for d in glob.glob(loc.ROOT+'/*') :
    name = os.path.basename(d)
    if '.' in name : continue
    setattr( loc, name.upper(), d )
loc.LATEX = loc.LHCB+'/latex'


# Import submodules
import processing
import nums
import db
import editing
import plotting
import efficiencies
import scripts
import LHCb
