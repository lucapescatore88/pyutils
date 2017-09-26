import sys, string
from ROOT import *

def getPartLV(name, event) :

    px = getattr(event,name+"_PX")
    py = getattr(event,name+"_PY")
    pz = getattr(event,name+"_PZ")
    m  = getattr(event,name+"_M")

    res = TLorentzVector()
    res.SetXYZM(px,pz,pz,m)

    return res

def loopTrees(tree_list,worker = None,cutter = None,args=None) :

    newfile   = TFile(args.outfile,"RECREATE")
    print "Writing to: ", newfile.GetName()

    for tree in tree_list :
        
        newtree = loopTree(tree,worker,cutter,args)
        newfile.cd()
        newtree.Write()

    newfile.Close()

def loopTree(tree,worker=None,cutter=None,args=None) :

    if worker is not None :
        if not hasattr(worker,'variables') or not hasattr(worker,'addVariables') :
            print "Attention: worker module doesn't have 'variables' and 'addVariables' attributes! Aborting..."
            sys.exit()
    #if cutter is not None :
    #    if not hasattr(cutter,'cutEvents') :
    #        print "Attention: cutter module doesn't habe cutEvents! Aborting..."
    #        sys.exit()

    print "Processing", tree.GetName(), "..."
    outTname = tree.GetName().replace("/DecayTree","")
    if args.outtree is not None : outTname += '_'+args.outtree
    newtree   = TTree(outTname,outTname)
    if args.clone : newtree = tree.CloneTree(0)
    newtree.SetName(outTname)
    
    if worker is not None :
        for name,arr in worker.variables.iteritems() :
            newtree.Branch( name, arr, name+"/D")

    nevts = 0
    nmax = args.maxev
    if args.maxev > 1.e13 : nmax = tree.GetEntries() 
    for ie,ev in enumerate(tree) :

        args.extra['nevts'] = nevts
        
        if cutter is not None :
            if not cutter(tree,ev,ie,args.extra) : continue
        if worker is not None :
            worker.addVariables(tree,ev,ie,worker.variables,args.extra)
       
        newtree.Fill()
        nevts+=1
        if ie%20==0 : print "\rNumber of events saved: ", ie, " / ", nmax,
        if ie >= nmax : break

    print
    return newtree
    




