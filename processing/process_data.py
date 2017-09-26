from ROOT import *
from argparse import ArgumentParser
from array import array
import os, sys, re, pickle
from Lb2LemuEnv import loc
from utils.utils import loopTrees
import subprocess as sb
import importlib
from glob import glob
from get_data import *

parser = ArgumentParser()
parser.add_argument("-m","--maxev",   default=1e14,type=float)
parser.add_argument("-O","--outfile", default="out")
parser.add_argument("-T","--outtree", default=None)
parser.add_argument("-t","--tname",   default="DecayTreeTuple/DecayTree")
parser.add_argument("-d","--dtype",   default=None)
parser.add_argument("-i","--fromid",  default=None)
parser.add_argument("-q","--queue",   default="1nd")
parser.add_argument("-w","--worker",  default=[None,None,None], nargs='*',help='-w addMVA/addVariablesAndMVA MODE MVA_TYPE ')
parser.add_argument("-c","--cuts",    default=[None, None], nargs='*', help='-c cutStripPID Prompt or SL or MCSLLc2pKpi or MCLc2pmm/MCLc2pmm')
parser.add_argument("--friends",      default="")
parser.add_argument("--local",        action="store_true")
parser.add_argument("--clone",        action="store_true")
parser.add_argument("--makeFriends",  action="store_true")
parser.add_argument("--force",        action="store_true")
parser.add_argument("--checkjobs",    action="store_true")
parser.add_argument("--checkoutfile", action="store_true")
parser.add_argument("-f","--inputs",  nargs="+")
args = parser.parse_args()

if args.local :
   
    worker = None
    if args.worker[0] is not None :
        worker = importlib.import_module("routines."+args.worker[0])
        worker.dtype = args.worker[1]
        worker.method = args.worker[2]
    cutter = None
    if args.cuts[0] is not None :
        cutmod = importlib.import_module("routines."+args.cuts[0])
        cutmod.dtype = args.cuts[1]
        cutter = cutmod.cutEvents
ncategories = 10

trees = []

files = args.inputs
friends = None
if files is None :
    if args.dtype is not None or args.fromid is not None :
        myfriends = []
        if args.friends != "" : myfriends = args.friends.split(',')
        print "Retrieving files and friends (", myfriends, ")"
        files, friends = getDataFiles(opts=args,friends = myfriends)
        print "Files retrieved, building chains"
        for tname in args.tname.split(';') :
            tree = buildChain(tname,files,friends,check = False)
            print "Tree", tname,":", tree.GetEntries(), "entries found"
            trees.append(tree)
    else :
        print "No files to reduce"
        sys.exit()
else :
    for tname in args.tname.split(';') :
        tree = TChain(tname)
        for f in files : 
            print "Adding file: ", f
            tree.AddFile(f)
        trees.append(tree)

#sys.exit()

args.extra = {'ncategories' : ncategories}

if not args.makeFriends :
    loopTrees(trees,worker,cutter=cutter,args=args)
else :    
    usr=os.getenv('USER')
    if usr=="pluca":
        tuplePath=loc.FRIENDS
    elif usr=="mstamenk":
        tuplePath=loc.MARKOFRIENDS
    else:
        print "Please specify friends tuple path"
        sys.exit()
    rootdir = tuplePath+args.outtree.replace(".root","")

    os.system("mkdir -p "+rootdir)
    print "Friends will go into", rootdir
    for fi,f in enumerate(files) : 

        ids = re.findall('/(\d+)/(\d+)/',f)[0]
        os.system("mkdir -p "+rootdir+'/'+str(ids[0]))
        curdir = rootdir+'/'+'/'.join(ids)
        os.system("mkdir -p "+curdir)

        args.outtree = args.outtree.replace(".root","")
        args.outfile = curdir + "/{name}.root".format(name=args.outtree)

        ## Check if already done correctly
        redo = False
        if len(glob(args.outfile)) > 0 : 
            if args.checkoutfile :
                
                myf = TFile.Open(args.outfile)
                if "0x(nil)" in myf.__str__() : redo = True
                else :
                    for tname in args.tname.split(';') :
                        outTname = tname.replace("/DecayTree","")
                        if args.outtree is not None : outTname += '_'+args.outtree
                        myt = myf.Get(outTname)
                        if "0x(nil)" in myt.__str__():
                            redo = True
                            print "Relaunching because of missing tree"
                            break
                    
            if not redo and not args.force :
                print '\rProcessed {i} / {tot} files'.format(i=fi+1,tot=len(files)),
                continue

        if args.checkjobs :
            jobs = sb.check_output('bjobs')
            if '_'.join(ids) in jobs : 
                print "Job", ids, "already submitted"
                continue

        if args.local : 
            
            trees = []
            for tname in args.tname.split(';') : 
                if friends is not None : tree = buildChain(tname,[f],[friends[fi]])
                else : tree = buildChain(tname,[f])
                trees.append(tree)

            loopTrees(trees,worker,cutter=cutter,args=args)

            print '\nProcessed {i} / {tot} files'.format(i=fi+1,tot=len(files))

        else :

            pickle.dump(args,open(curdir+'/opts.pkl','w'))
            runf = open(curdir+'/run.sh','w')
            if args.cuts[0]==None : 
                runf.write("python "+loc.PYTHON+"utils/process_single_file.py -f {filename} -w {worker} {wparam1} {wparam2} -c {cutter}  --opts {options}".format(
                    filename = f, worker = args.worker[0], wparam1 = args.worker[1], wparam2 = args.worker[2] , cutter = args.cuts[0] , options = curdir+'/opts.pkl' ))
            else :
                runf.write("python "+loc.PYTHON+"utils/process_single_file.py -f {filename} -w {worker} {wparam1} {wparam2} -c {cutter} {cparam}  --opts {options}".format(
                    filename = f, worker = args.worker[0], wparam1 = args.worker[1], wparam2 = args.worker[2] , cutter = args.cuts[0], cparam = args.cuts[1] , options = curdir+'/opts.pkl' ))
            runf.close()
            cmd = "bsub -R 'pool>30000' -o {dir}/out -e {dir}/err -q {queue} -J {jname} < {dir}/run.sh ".format(
                dir = curdir, jname = args.outtree+'_'+'_'.join(ids), queue = args.queue )
            print cmd
            os.system(cmd)




