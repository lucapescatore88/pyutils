import os, sys, array, random
from argparse import ArgumentParser
from uncertainties import ufloat
import importlib
from ROOT import *

#c = TCanvas()
#gStyle.SetPalette(1)

parser = ArgumentParser()
parser.add_argument("-t","--pidtabs",default=".",)
parser.add_argument("-O","--outdir", default="PerfHists")
parser.add_argument("-m","--pidmtabs", default="PerfHistsMuon")
parser.add_argument("-c","--config", default="config_PID")
parser.add_argument("-s","--scale", type=float, default=1.)
args = parser.parse_args()

sys.path.append(os.getenv('PWD'))
config = importlib.import_module(args.config)
if 'cuts' not in dir(config) :
    print "Attention you need to define the PID cuts applied"
    sys.exit()
if 'decays' not in dir(config) :
    print "Attention you need to define a list of decays to apply the PID to"
    sys.exit()

pidcuts = config.cuts
decays  = config.decays 

def findEff(orig,reco,p,pt,magpol) :

    mag = "Down"
    if magpol > 0 : mag = "Up"

    ## Get correct PIDCalib table
    pidbase = args.pidtabs
    if reco == 'Mu' : pidbase = args.pidmtabs
    f = TFile.Open(pidbase+"PerfHists_{part}_Strip21_Mag{mag}_ricci_binning_P_PT.root".format(part=orig,mag=mag))
    cut = pidcuts[reco]

    h = f.Get(orig+"_"+cut+"_All")
    thebin = h.FindBin(p*args.scale,pt*args.scale)
   
    return ufloat(h.GetBinContent(thebin),h.GetBinError(thebin))

def loop_IDs(IDs,t) :

    w = ufloat(-1,0)
    for curid, parts in IDs.iteritems() :
            
        ww = ufloat(1,0)
        formula = TTreeFormula("cutid",curid, t);
        t.GetEntry(i)
   
        found = False
        if formula.EvalInstance() :
            for part,swap in parts.iteritems() :
                
                if swap == "" : continue
                orig_part = swap.split()[0]
                reco_part = swap.split()[2]
                
                pt = t.GetLeaf(part+"_PT").GetValue()
                p = t.GetLeaf(part+"_P").GetValue()
                magbr = t.GetLeaf("Polarity")
                
                if '0x(nil)' in magbr.__str__() :
                    magpol = random.choice([-1,1])
                else :
                    magpol = t.GetLeaf("Polarity").GetValue()

                temp_ww = findEff(orig_part,reco_part,p,pt,magpol)
                if (temp_ww.get_val()>0.): ww *= temp_ww
                else : ww *= ufloat(0., temp_ww.err) ## IF otherwise the error calculation breaks 

            w = ww
            break

    # Uncomment to have an idea of what does not mach any ID
    #if w.val==-1 : 
    #    print "\nEplus (id, momid): ", t.GetLeaf("eplus_TRUEID").GetValue(), t.GetLeaf("eplus_MC_MOTHER_ID").GetValue(),
    #    print "Muminus (id,momid) : ", t.GetLeaf("muminus_TRUEID").GetValue(), t.GetLeaf("muminus_MC_MOTHER_ID").GetValue()
    
    return w


for pid in decays:
    
    print "Analysing", pid.decay, "......."
    print "Files:", pid.files 
    print "Cut: ", pid.matching

    t = TChain(pid.tree)
    for f in pid.files : t.AddFile(f)
     
    nevts = t.GetEntries()
    
    pidw = array.array("d", [0.0])
    pidw_err = array.array("d", [0.0])

    newfile = TFile(args.outdir+"/"+pid.decay+"_pid.root","RECREATE")
    newtree = t.CloneTree(0)
    newBranch = newtree.Branch( "PIDw" , pidw, "PIDw/D" )
    newBranch = newtree.Branch( "PIDw_err" , pidw_err, "PIDw_err/D" )
    
    uavg, uerravg, n  = 0, 0, 0
    match = TTreeFormula("matching",pid.matching, t)
    print "Entries: ", nevts
    for i in range(nevts):
        
        t.GetEntry(i)
        if not match.EvalInstance() : continue
        print "\rProgress... ", i, "/", nevts,
        w = loop_IDs(pid,t)
        
        pidw[0] = 0.
        pidw_err[0] = 0.
        if w.get_err() < 0.15 :
            pidw[0] = w.get_val()
            pidw_err[0] = w.get_err()
        else:
            print "Setting to zero (", w, ")" 

        ## Make the average on the fly just to check plausibility
        if w.get_val() >= 0. :
            if w.get_err() < 0.15 :
                uavg += w.get_val()
                uerravg += w.get_err()
            n +=1
        
        newtree.Fill()

    ## Print on the fly average for quick validation
    if n > 0 :
        print
        print "Cut eff : ", n / float(nevts)
        print "PID eff : ", uavg / n, " +- ", uerravg / n, "(", uerravg / uavg * 100, "%)"
        print
    else : print "n = 0"
    
    newfile.cd()
    newtree.Write()




