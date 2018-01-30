import subprocess as sb
import sys, re, os

xrootd = 'root://eoslhcb.cern.ch/'

def remotels_simple_py3(location,pattern = '',opt='') :
    out = sb.check_output("xrdfs "+xrootd+" ls "+location, shell=True).decode("utf-8") 
    out = out.split('\n')
    out = [ x.replace(xrootd,'') for x in out if len(x) > 0 ]
    out = [ x for x in out if len(re.findall(pattern,x)) > 0 or pattern=='' ]
    if 'noxrd' not in opt : out = [ xrootd+x for x in out ]
    return out

def remotels_simple(location,pattern = '',opt='') :
    out = sb.check_output("xrdfs "+xrootd+" ls "+location, shell=True)
    out = out.split('\n')
    out = [ x.replace(xrootd,'') for x in out if len(x) > 0 ]
    out = [ x for x in out if len(re.findall(pattern,x)) > 0 or pattern=='' ]
    if 'noxrd' not in opt : out = [ xrootd+x for x in out ]
    return out

def remotels_allpy(location,pattern='',opt='') :

    import sys
    if sys.version_info.major > 2 : return remotels_simple_py3(location,pattern,opt)
    else : return remotels_simple(location,pattern,opt)

def remotels(locations,pattern='',levels=0) :
 
    folders = []
    lev = 0
    tmpfolders = locations
    while lev < levels :
        newfolders = []
        for tmp in tmpfolders :
            try : newfolders.extend(remotels_allpy(tmp,opt='noxrd'))
            except : continue
        tmpfolders = newfolders
        lev += 1
    
    files = [] 
    for tmp in tmpfolders :
        try : files.extend(remotels_allpy(tmp,pattern))
        except : continue

    return files

def remote_ls_fromids(dataids) :
    
    base = dataids[0]
    ids  = dataids[1]
    locs = [ base + str(i) for i in ids ]
    return remotels(locs,levels=1,pattern='(.root)')

if __name__ == '__main__' :

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path",default = None)
    args = parser.parse_args()

    remote_ls(path)


