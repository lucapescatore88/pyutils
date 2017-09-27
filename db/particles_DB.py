import os, sys

dbfile = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ParticleTable.txt')
lines = open(dbfile).readlines()

class Particle :

    '''
    The LHCb text file LHCb/ParticleTable.txt contains all the properties of particles
    as defined by LHCB. This will be parsed and made available to you as a python object.

    Here an example

    from utils.particles_DB import db
    db['e-']    # Print properties
    --------------------------------
    Name     : e-
    PDG ID   : 11
    Charge   : -1.0
    Mass     : 0.000511
    Lifetime : 1e+16
    Width    : 0.0
    -------------------------------
    db['p+'].mass
    0.93827205
    db['pi+'].mass
    0.13957018
    db['K+'].tau
    1.237939e-08
    db['Z0'].width
    10.0
    db['W+'].pdgid
    24

    ## You can also get dictionaries by keys e.g. PDGID or mass given particle name
    from utils.particles_DB import db, pdgid_db, mass_db
    pdg_db['p+']
    pdgid_db['p+']
    2212
    mass_db['p+']
    0.93827205
    '''

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


