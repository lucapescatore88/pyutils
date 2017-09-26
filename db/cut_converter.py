import os, re
from ROOT import TCut

class CutConverter :

    name = ""
    cuts = {}
    __orig_cuts = {}
    __keys = []

    def __init__(self, namefile = '/src/cuts.hpp') :

        if not os.path.exists(namefile) : return
        
        lines = open(namefile).readlines()

        for l in lines :

            if "TCut" not in l or "//" in l or "#" in l:
                continue
            
            #print l
            poseq = l.index("=")+1
            cut = l[poseq:]
            cut = cut.replace(";","").replace("\n","")
	    cut = cut.replace("&&"," && ").replace("||"," || ")

            split = l.split()
            namepos = split.index("TCut") + 1
            name = split[namepos]

            self.__keys.append(name)
            self.__orig_cuts[name] = cut

            cut = cut.replace("\"","")
            parts = cut.split()
            for istr,str in enumerate(parts) :
                sstr = str.replace("!","").replace("(","").replace(")","")
                if sstr in self.cuts.keys() :
                    cut = cut.replace(sstr,"(" + self.cuts[sstr] + ")")
                    #parts[istr] = "(" + self.cuts[sstr] + ")"
                    #if istr > 0 :
                    #    if parts[istr - 1] == "+" :
                    #        parts[istr - 1] = "&&"
                    #if istr < len(parts)-1 :
                    #    if parts[istr + 1] == "+" :
                    #        parts[istr + 1] = "&&"
            #cut = ' '.join(parts)

            #globals()[name] = TCut(cut)
            self.__dict__[name] = TCut(name,cut)
            self.cuts[name] = cut
            
    def Print(self) :

        for k,v in self.cuts.iteritems() :
            print k, " ---> ", v, "\n"

    def List(self) :

        print self.cuts.keys()

    def SaveToFile(self, namefile = "cuts.hpp", type = "Extended" ) :

        if type == "Reduced" :
            cuts, keys = self.GetReducedCuts()
        elif type == "Original" :
            cuts = self.__orig_cuts
            keys = self.__keys
        else :
            cuts = self.cuts
            keys = self.cuts.keys()

        f = open(namefile,'w')
        f.write("#ifndef CUTS_HPP\n#define CUTS_HPP\n\n#include \"TCut.h\"\n\n")
        f.write("namespace DefCuts\n{\n")
        for c in keys :
            if type != "Extended" :
                f.write("\tTCut " + c + " = " + cuts[c] + ";\n\n")
            else :
                f.write("\tTCut " + c + " = \"" + cuts[c] + "\";\n\n")
        f.write("}\n\n#endif")

    def GetReducedCuts(self) :

        ordkeys = sorted(self.cuts, key=lambda k: len(self.cuts[k]), reverse=True)
        cuts_copy = self.cuts.copy()
        
        for k in ordkeys :
            cuts_copy[k] = cuts_copy[k].replace(" ","").replace("\t","")
        
        red_cuts = cuts_copy.copy()

        sort_keys = {}
        for k,kk in enumerate(ordkeys):
            ntimes = 0
            
            for j,kj in enumerate(ordkeys[k+1:]) :
    
                if cuts_copy[kj] in cuts_copy[kk] and cuts_copy[kj] != "1" :
                    ntimes += 1
                    red_cuts[kk] = red_cuts[kk].replace(cuts_copy[kj]," "+kj+" ")    

            cstr = [] 
            for str in red_cuts[kk].split() :
                if str == "&&" or str == "||" :
                    cstr.append(str)
                    continue

                if "&&" not in str or "||" not in str :
                    if str in cuts_copy.keys() :
                        cstr.append(str)
                    else :
                        cstr.append("\""+str+"\"")
                    continue

                if str in cuts_copy.keys() :
                        cstr.append(str)
                else :
                    cstr.append("\""+str+"\"")

            red_cuts[kk] = " ".join(cstr)
            red_cuts[kk] = red_cuts[kk].replace("!\"","\" !")
            red_cuts[kk] = red_cuts[kk].replace("\"||"," || \"")
            red_cuts[kk] = red_cuts[kk].replace("\"&&"," && \"")
            red_cuts[kk] = red_cuts[kk].replace("&&\"","\" && ")
            red_cuts[kk] = red_cuts[kk].replace("||\"","\" || ")
            red_cuts[kk] = red_cuts[kk].replace("&&"," && ")
            red_cuts[kk] = red_cuts[kk].replace("||"," || ")
            red_cuts[kk] = red_cuts[kk].replace("!="," != ")
            red_cuts[kk] = red_cuts[kk].replace("=="," == ")
            red_cuts[kk] = red_cuts[kk].replace("<"," < ")
            red_cuts[kk] = red_cuts[kk].replace("<="," <= ")
            red_cuts[kk] = red_cuts[kk].replace(">"," > ")
            red_cuts[kk] = red_cuts[kk].replace(">="," >= ")
            sort_keys[kk]  = ntimes
                
        ordkeys = sorted(sort_keys, key=sort_keys.get)
        
        return red_cuts, ordkeys


CutsDef = CutConverter()
