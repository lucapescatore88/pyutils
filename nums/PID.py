class PIDinfo :

  def __init__(self, decay, matching, IDs, divIDs = None, files = [], tree = "DecayTree") :
    self.decay    = decay
    self.matching = matching
    #self.files    = db[decay].tup
    self.IDs      = IDs
    self.divIDs   = divIDs
    self.files    = files 
    self.tree     = tree


