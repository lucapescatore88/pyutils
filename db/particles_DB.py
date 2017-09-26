import os, sys
from Lb2LemuEnv import loc

dbfile = loc.LHCB+"/ParticleTable.txt"
lines = open(dbfile).readlines()

class Particle :

    def __init__(self,name,pdgid,charge,mass,tau,width) :
        self.name   = name
        self.pdgid  = int(pdgid)
        self.charge = float(charge)
        self.mass   = float(mass)
        self.tau    = float(tau)
        self.width  = float(width)

    def __repr__(self) :
        return self.__str__()

    def __str__(self) :
        out =  "--------------------------------\n"
        out += "Name     : " + self.name + "\n"
        out += "PDG ID   : " + str(self.pdgid) + "\n"
        out += "Charge   : " + str(self.charge) + "\n"
        out += "Mass     : " + str(self.mass) + "\n"
        out += "Lifetime : " + str(self.tau) + "\n"
        #print "Descriptor : ", self.name
        out += "Width    : " + str(self.width) + "\n"
        out += "-------------------------------\n"
        return out

class ParticleDB :

    db = {}

    def get_dict(self,var="pdgid"):
        out = {}
        for pn,p in db.iteritems() :
            out[pn] = getattr(p,var)
        return out


## Start filling dictionary

pdb = ParticleDB()
db = pdb.db

keep = False
for l in lines :

    if "gamma" in l : keep = True

    toks = l.split()
    if not keep or len(toks) != 9 : continue
        
    db[toks[0]] = Particle( name       = toks[0],
                            pdgid      = toks[2],
                            charge     = toks[3],
                            mass       = toks[4],
                            tau        = toks[5],
                            #descriptor = toks[6],
                            width      = toks[8] )


pdgid_db = pdb.get_dict()
mass_db = pdb.get_dict("mass")
tau_db = pdb.get_dict("tau")
width_db = pdb.get_dict("width")
charge_db = pdb.get_dict("charge")


