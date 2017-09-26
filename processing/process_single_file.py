import sys, pickle
from glob import glob
import importlib
from argparse import ArgumentParser
from ROOT import *
from utils.utils import loopTrees
from get_data import *

parser = ArgumentParser()
parser.add_argument("-f","--filename", default=None,type=str)
parser.add_argument("-w","--worker",   default=[None,None,None], nargs='*' , help='-w {worker} {MODE} {MVA_TYPE}',type=str)
parser.add_argument("-c","--cuts",     default=[None,None], nargs='*', help='-c {cutter} {MODE}',type=str)
parser.add_argument("--opts",          default=None,type=str)
opts = parser.parse_args()

if opts.worker[0] is None : 
    print "No worker set, no variables will be added"
else : 
    worker = importlib.import_module("routines."+opts.worker[0])
    if opts.worker[1] is not None : worker.dtype = opts.worker[1]
    if opts.worker[2] is not None : worker.method = opts.worker[2]

cutmod, args, cutter = None, None, None
if opts.cuts[0] is not None and opts.cuts[0] != 'None':
    cutmod = importlib.import_module("routines."+opts.cuts[0])
    cutmod.dtype = opts.cuts[1]
    cutter = cutmod.cutEvents
if len(glob(opts.opts)) > 0 :
    args = pickle.load(open(opts.opts))

## Find inputs
myfriends = []
if args.friends != "" : myfriends = args.friends.split(',')
friends = findFriendFiles([opts.filename], myfriends)

tnames = args.tname.split(';')
trees = []
for tname in tnames :

    tree = buildChain(tname,[opts.filename],friends,check=True)
    trees.append(tree)

args.extra = {'ncategories' : 10}
loopTrees(trees,worker,cutter,args)




