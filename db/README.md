#### Particles DB

The LHCb text file LHCb/ParticleTable.txt contains all the properties of particles
as defined by LHCB. This will be parsed and made available to you as a python object.

Here an example
```
from utils.particles_DB import db
db['e-']
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

from utils.particles_DB import db, pdgid_db, mass_db
pdg_db['p+']
pdgid_db['p+']
2212
mass_db['p+']
0.93827205
```
