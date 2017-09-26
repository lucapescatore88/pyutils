#!/usr/bin/env python

from __future__ import division
import pickle, math
import re, fnmatch


# Functions to round numbers

def _getCFR(err, sig='PDG'):
    '''
    Get position where to round number based on number of significant digits required
    '''
    if sig == 'PDG':
        sig = 2 if round(err*10**_getCFR(err, sig=3)) < 354 else 1
    try:
        cfr = sig-int(math.floor(math.log10(err)))-1
    except ValueError:
        cfr = 2 
    return cfr

def round_sigDig(val, sig='PDG'):
    cfr = _getCFR(err, sig)
    try:
        return ('{:.'+str(cfr)+'f}').format(val)
    except ValueError:
        if cfr > 0:
            return str(round(val, cfr))
        else:
            return str(int(round(val, cfr)))


def roundPair(val, err, sig='PDG'):
    cfr = _getCFR(err, sig)
    try:
        return ('{:.'+str(cfr)+'f}').format(val), ('{:.'+str(cfr)+'f}').format(err)
    except ValueError:
        if cfr > 0:
            return str(round(val, cfr)), str(round(err, cfr))
        else:
            return str(int(round(val, cfr))), str(int(round(err, cfr)))
    
def roundList(ll, sig='PDG', cfr_fixed=None):
    cfr_list = sorted([_getCFR(err, sig) for err in ll if err !=0.])
    cfr = cfr_list[-1]
    if cfr_fixed: cfr = cfr_fixed
    return [('{:.'+str(cfr)+'f}').format(val) for val in ll]

def roundDict(dd, sig='PDG', cfr_fixed=None):
    cfr_list = sorted([_getCFR(err, sig) for err in ll if err !=0.])
    #cfr_list = sorted([sig-int(math.floor(math.log10(abs(err))))-1 for err in dd.values() if err !=0.])
    cfr = cfr_list[-1]
    if cfr_fixed: cfr = cfr_fixed
    return dict([(key,('{:.'+str(cfr)+'f}').format(val)) for key,val in dd.items()])

# Functions to deal with root trees

try:
    import ROOT as r
except ImportError:
    print "ROOT not found, funtions to deal with trees not available"

def getBranches(tree):
    return [i.GetName() for i in tree.GetListOfBranches()]

def getIntegral(histo, region=[None,None]):
    minBin = histo.FindBin(region[0]) if region[0] else 0
    maxBin = histo.FindBin(region[1]) if region[1] else histo.GetNbinsX()
    return histo.Integral(minBin, maxBin)

def sumWeights(tree, weights_name, cut=None):
    cut = '{0}*({1})'.format(weights_name, cut) if cut else weights_name
    tree.Draw('{0}>>htmp(1)'.format(weights_name), cut)
    h = r.gDirectory.Get('htmp')
    return h.GetBinContent(1)


def numEntries(tree, cut = None, weights_name = None):
    '''
    Return number of entries of a tree or sum of weights
    if a variable (or function of variables) is given as weight.
    Possible also to give a cut.
    '''
    if weights_name == None:
        return tree.GetEntries() if cut==None else tree.GetEntries(cut)
    else:
        return sumWeights(tree, weights_name=weights_name, cut=cut)


# Functions to deal with ufloats

try:
    from uncertainties import ufloat
except ImportError:
    print "uncertainties not found, funtions to deal with ufloats not available"

def dictErrors(num, pattern=None, regex=None):
    '''
    take a ufloat and return a dictionary with the various components of the errors
    a shell-like pattern or a regular espression can be given to reduce the components to select
    '''
    dd = {}
    for key, value in num.error_components().items():
        key = key.tag
        if dd.has_key(key):
            dd[key] = sqrt(dd[key]**2+value**2)
        else:
            dd[key] = value
    if pattern:
        dd = {key : value for key, value in dd.items() if fnmatch.fnmatch(key, pattern)}
    if regex:
        dd = {key : value for key, value in dd.items() if re.match(regex, key)}
    return dd

def dictRelErrors(num, pattern=None, regex=None):
    '''
    take a ufloat and return a dictionary with the various components of the erros (relative to the value)
    a shell-like pattern or a regular espression can be given to reduce the components to select
    '''
    return {key: val/num.n for key, val in dictErrors(num=num, pattern=pattern, regex=regex).items()}


def getError(num, pattern=None, regex=None):
    '''
    take a ufloat and return the total error
    a shell-like pattern or a regular espression can be given to reduce the components to select
    '''
    return sqrt(sum([i**2 for i in dictErrors(num=num, pattern=pattern, regex=regex).values()]))


# Seems impossible to code what I want
# def setError(num, value, name=None):
#     '''
#     assign error to a ufloat
#     if the name is specified assign a new tag or averwite the error
#     '''
#     if name == 0:
#         num.s = value
#     else:
#         if name in dictErrors(num).keys():
                        

def getRelError(num, pattern=None, regex=None):
     '''
     take a ufloat and return the total relative error
     a shell-like pattern or a regular espression can be given to reduce the components to select
     '''
     return getError(num=num, pattern=pattern, regex=regex)/num.n
