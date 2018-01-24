
"""
Functions to deal with root trees and others
"""

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


def makeGraph(values, errors=None, x_values=None, errors_x = None):
    import numpy as np
    x = np.array([float(i) for i in range(len(values))]) if x_values is None else np.array([float(i) for i in x_values])
    ex = np.array([0 for i in range(len(x))]) if errors_x is None else np.array([float(i) for i in errors_x])
    y = np.array([float(i) for i in values])
    ey = np.array([0 for i in range(len(x))]) if errors is None else np.array([float(i) for i in errors])
    return r.TGraphErrors(len(x),x, y, ex, ey)


def makeHisto(name, values, title = None, range = [None, None], nBins = 100):
    if range[0] == None: range[0] = min(values)
    if range[1] == None: range[1] = max(values)+1
    if title == None: title = name
    h = r.TH1D(name, title, nBins, *range)
    for i in values:
        h.Fill(i)
    return h


def makeGraphHisto(name, title, values, errors=None):
    '''
    Take values and errors and make TH1D that contains graph
    '''
    h = r.TH1D(name, title, len(values),0,len(values))
    for i in range(len(values)):
        h.SetBinContent(i+1, values[i])
        if errors:
            h.SetBinError(i+1, errors[i])
        else:
            h.SetBinError(i+1, 0)
    return h.Clone()



# Import functions from roofit
from roofit import *
