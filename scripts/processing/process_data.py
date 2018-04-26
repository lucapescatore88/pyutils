from ROOT import *
from argparse import ArgumentParser
from array import array
import os, sys, re, pickle
from utils import loopTrees
import subprocess as sb
import importlib
from glob import glob

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-O","--outfile", default="out")
    parser.add_argument("-T","--outtree", default="tree")
    parser.add_argument("-P","--outpath", default="")
    parser.add_argument("-t","--tname",   default="DecayTreeTuple/DecayTree")
    parser.add_argument("-f","--inputs",  nargs="+")
    parser.add_argument("-M","--modpath", default=os.getenv("PWD"))
    parser.add_argument("-w","--worker",  default=[None], nargs='*')
    parser.add_argument("-c","--cuts",    default=[None], nargs='*')
    parser.add_argument("-q","--queue",   default="1nd")
    parser.add_argument("-m","--maxev",   default=1e14,type=float)
    parser.add_argument("--local",        action="store_true")
    parser.add_argument("--clone",        action="store_true")
    parser.add_argument("--merge",        action="store_true")
    parser.add_argument("--force",        action="store_true")
    parser.add_argument("--checkjobs",    action="store_true")
    parser.add_argument("--checkoutfile", action="store_true")
    
    args = parser.parse_args()
    
    sys.path.append(args.modpath)

    if args.local :
       
        worker = None
        print args.worker[0]
        if args.worker[0] is not None :
            worker = importlib.import_module(args.worker[0])
            print worker
        cutter = None
        if args.cuts[0] is not None :
            cutmod = importlib.import_module(args.cuts[0])
            cutter = cutmod.cutEvents
    ncategories = 10
    
    trees = []
    
    files = []
    for inpt in args.inputs :
        files.extend(glob(inpt))
     
    args.extra = {'ncategories' : ncategories}
    
    if args.merge :
        
        print "Output will be merged in a single file"
        for tname in args.tname.split(';') :
            tree = TChain(tname)
            for f in files :
                print "Adding file: ", f
                tree.AddFile(f)
            trees.append(tree)
    
        loopTrees(trees,worker,cutter=cutter,args=args)

    else : 

        #usr=os.getenv('USER') 
        rootdir = args.outpath+args.outtree.replace(".root","")
        os.system("mkdir -p "+rootdir)

        print "Output will be separate per each input file"
        
        for fi,f in enumerate(files) : 
    
            #ids = re.findall('/(\d+)/(\d+)/',f)[0]
            #os.system("mkdir -p "+rootdir+'/'+str(ids[0]))
            #curdir = rootdir+'/'+'/'.join(ids)
            #os.system("mkdir -p "+curdir)
            ids = re.findall('/(\d+)/',f)[0]
            curdir = rootdir+'/'+str(ids[0])
            os.system("mkdir -p "+curdir)
            
            args.outtree = args.outtree.replace(".root","")
            args.outfile = curdir + "/{name}.root".format(name=args.outtree)
    
            ## Check if already done correctly
            redo = False
            if len(glob(args.outfile)) > 0 :
                print "Output:", args.outfile
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
                    tree = TChain(tname)
                    tree.AddFile(f)
                    trees.append(tree)
    
                loopTrees(trees,worker,cutter=cutter,args=args)
    
                print '\nProcessed {i} / {tot} files'.format(i=fi+1,tot=len(files))
    
            else :
    
                pickle.dump(args,open(curdir+'/opts.pkl','w'))
                runf = open(curdir+'/run.sh','w')
                if args.cuts[0]==None : 
                    runf.write("python "+loc.PROCESSING+"/process_single_file.py -f {filename} -w {worker} {wparam1} {wparam2} -c {cutter}  --opts {options}".format(
                        filename = f, worker = args.worker[0], wparam1 = args.worker[1], wparam2 = args.worker[2] , cutter = args.cuts[0] , options = curdir+'/opts.pkl' ))
                else :
                    runf.write("python "+loc.PROCESSING+"/process_single_file.py -f {filename} -w {worker} {wparam1} {wparam2} -c {cutter} {cparam}  --opts {options}".format(
                        filename = f, worker = args.worker[0], wparam1 = args.worker[1], wparam2 = args.worker[2] , cutter = args.cuts[0], cparam = args.cuts[1] , options = curdir+'/opts.pkl' ))
                runf.close()
                cmd = "bsub -R 'pool>30000' -o {dir}/out -e {dir}/err -q {queue} -J {jname} < {dir}/run.sh ".format(
                    dir = curdir, jname = args.outtree+'_'+'_'.join(ids), queue = args.queue )
                print cmd
                os.system(cmd)

                
