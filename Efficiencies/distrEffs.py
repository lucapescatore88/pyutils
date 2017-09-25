#!/usr/bin/env python
from __future__ import division
from math import sqrt
import pickle, os, math, copy
import array, itertools
import ROOT as r
from root_numpy import tree2array
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import seaborn as sns
from uncertainties import ufloat, umath, unumpy
try:
    from pyUtils import roundPair
    from pyUtils.Efficiencies import Efficiency
    from pyUtils.MultiCanvas import MultiCanvas
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../..'))
    from pyUtils import roundPair
    from pyUtils.Efficiencies import Efficiency
    from pyUtils.MultiCanvas import MultiCanvas


class NTable:
    '''
    n-D histo that can contain the distributions of num_gen, num_sel, effs ...
    '''
    
    def __init__(self, variables, tree = None, nBins=None,
                 ranges=None,
                 weights_var = None, cut=None, edges=None):
        if isinstance(variables, str):
            variables = [variables]
        self.variables = variables
        self.weights_var = weights_var
        self.cut = cut
        if nBins == None:
            dict_bins = {1: 100, 2: 50, 3: 20, 4: 10, 5: 5}
            nBins = dict_bins.get(len(variables), 2)
        if not edges:
            edges = []
            if ranges:
                try:
                    assert len(nBins) == len(ranges)
                except TypeError:
                    nBins = [nBins]*len(ranges)
                for rr, nBin in zip(ranges, nBins):
                    edges.append(np.linspace(rr[0], rr[1], nBin+1))
            else:
                edges = nBins
        else:
            nBins = [len(i)-1 for i in edges]
            edges = [np.array(i) for i in edges]

        if tree:
            self.readTree(tree, edges)
        else:
            self.histo, self.edges = unumpy.uarray(np.zeros(nBins), np.zeros(nBins)), edges

    @property
    def val(self):
        return unumpy.nominal_values(self.histo)

    @property
    def err(self):
        return unumpy.std_devs(self.histo)

    @property
    def rel_err(self):
        return self.err/self.val
            

    def readTree(self, tree, nBins=3, ranges=None, cut=None, weights_var=None, weights_array=None):
        '''
        weights_array is a numpy array with the weights (assumed to be in the same order as in the tree)
        '''
        if cut == None: cut = self.cut
        if weights_var == None: weights_var = self.weights_var
        if weights_var or weights_array:
            rec = tree2array(tree, self.variables+[weights_var], selection=cut).view(np.recarray)
            df = pd.DataFrame(rec)
            if weights_var:
                df['w'] = df[weights_var]
            elif weights_array:
                df['w'] = weights_array
            df['w2'] = df['w']*df['w']
            df2 = df[self.variables]
            hh = np.histogramdd(df2.as_matrix(), bins=nBins, range=ranges, weights=df['w'])
            hh_sumw2 = np.histogramdd(df2.as_matrix(), bins=nBins, range=ranges, weights=df['w2'])
            self.edges = hh[1]
            self.histo = unumpy.uarray(hh[0], np.sqrt(hh_sumw2[0]))
        else:
            rec = tree2array(tree, self.variables, selection=cut).view(np.recarray)
            df = pd.DataFrame(rec)
            hh = np.histogramdd(df.as_matrix(), bins=nBins, range=ranges)
            hist, self.edges = hh
            self.histo = unumpy.uarray(hist[:], np.sqrt(hist))
       

        
    def __repr__(self):
        if not hasattr(self, 'histo'):
            return 'Empty {0}'.format(self.__class__.__name__)
        return '{0} with {1} dimensions'.format(self.__class__.__name__, self.histo.shape)

    
    def __str__(self):
        if not hasattr(self, 'histo'):
            return 'Empty {0}'.format(self.__class__.__name__)
        return '''{0} with {1} dimensions
        
            variables: {2},
        
            edges: {3},
        
            values:
            {4}'''.format(self.__class__.__name__, self.histo.shape, self.variables, self.edges, self.histo)


    def copy(self):
        '''
        deepcopy instance
        '''
        res = NTable()
        res.edges = [i.copy() for i in self.edges]
        res.variables = self.variables[:]
        res.histo = self.histo.copy()
        for coso in self.__dict__:
            if coso not in ['variables', 'edges', 'histo']:
                exec 'res.{0} = copy.deepcopy(self.{0})'.format(coso)
        res.__class__ = self.__class__ # like this I cast the base class to the derived class
        return res
    
    def __add__(self, other):
        assert np.array([(i==j).all() for i, j in zip(self.edges, other.edges)]).all()
        res = self.copy()
        res.histo = self.histo + other.histo
        return res

    def __sub__(self, other):
        assert np.array([(i==j).all() for i, j in zip(self.edges, other.edges)]).all()
        res = self.copy()
        res.histo = self.histo - other.histo
        return res

    def __mul__(self, other):
        res = self.copy()
        if hasattr( other, 'histo'): # Multiply by another nTable
            assert np.array([(i==j).all() for i, j in zip(self.edges, other.edges)]).all()
            res.histo = self.histo * other.histo
        else: # Multiply by a number
            res.histo = self.histo * other
        return res

    __rmul__ = __mul__

    def __div__(self, other):
        res = self.copy()
        if hasattr( other, 'histo'): # Divide by another nTable
            assert np.array([(i==j).all() for i, j in zip(self.edges, other.edges)]).all()
            val = self.val / other.val # np.nan_to_num(self.val / other.val)
            err = abs(val) * np.sqrt( (self.err/self.val)**2 + (other.err/other.val)**2) #np.nan_to_num(val * sqrt( (self.err/self.val)**2 + (other.err/other.val)**2))
            res.histo = unumpy.uarray(val,err)
        else: # Divide by a number
            res.histo = self.histo / other
        res.removeNan(0)
        return res

    def __rdiv__(self, other):
        res = self.copy()
        if hasattr( other, 'histo'): # Divide by another nTable
            assert np.array([(i==j).all() for i, j in zip(self.edges, other.edges)]).all()
            val = other.val / self.val #np.nan_to_num(other.val / self.val)
            err = abs(val) * np.sqrt( (self.err/self.val)**2 + (other.err/other.val)**2) # np.nan_to_num(val * sqrt( (self.err/self.val)**2 + (other.err/other.val)**2))
            res.histo = unumpy.uarray(val,err)
        else: # Divide by a number
            val = other / self.val #np.nan_to_num(other / self.val)
            err = abs(val) * abs(self.err/self.val) #np.nan_to_num(val * abs(self.val/self.err))
            res.histo = unumpy.uarray(val,err)
        res.removeNan(0)
        return res
    
    __truediv__ = __div__
    __rtruediv__ = __rdiv__
    

    def sqrt(self):
        res = self.copy()
        res.edges = self.edges
        res.variables = self.variables
        res.histo = unumpy.sqrt(self.histo)
        return res

    def saveToFile(self, fileName = "nTable.pkl"):
        pickle.dump(self, open( fileName, "wb" ))

    def loadFromFile(self,fileName = "nTable.pkl"):
        return pickle.load( open( fileName, "rb" ) )


    def transpose(self, perm):
        '''
        Change the order of the variables
        perm can either be variables names or numbers
        '''
        perm = list(perm)
        assert len(perm) == len(self.variables)
        for i in range(len(perm)):
            if not unicode(perm[i]).isnumeric():
                perm[i] = self.variables.index(perm[i])
        perm = tuple(perm)
        res = copy.deepcopy(self)
        res.variables=[self.variables[i] for i in perm]
        res.histo = self.histo.transpose(perm)
        res.edges =  [self.edges[i] for i in perm]
        return res

    def removeNan(self, default=None):
        '''
        modify self so that no nan or inf are present.
        default is what has to replace inf and nan
        if it is not given will be 0 for nana and  a big number for inf
        '''
        val = self.val
        err = self.err
        if default == None:
            val = np.nan_to_num(val)
            err = np.nan_to_num(err)
        else:
            val[np.isinf(val) + np.isnan(val)] = default
            err[np.isinf(err) + np.isnan(err)] = default
        self.histo =  unumpy.uarray(val,err)
        return self

    
    def project(self,vars2keep=[]):
        '''
        return a nTable of lower dimension projecting out (i.e. summing over)
        the variables not present in vars2keep
        vars2keep can contain the strings with the name of the variables or the indexes
        '''
        vars2keep = list(vars2keep)
        for i in range(len(vars2keep)):
            if unicode(vars2keep[i]).isnumeric():
                vars2keep[i] = self.variables[int(vars2keep[i])]
        index2sum = tuple([self.variables.index(i) for i in self.variables if i not in vars2keep])
        res = NTable(variables=[i for i in self.variables if i in vars2keep])
        res.histo = self.histo.sum(index2sum)
        res.edges = [self.edges[i] for i in range(len(self.edges)) if self.variables[i] in vars2keep]
        if len(vars2keep) > 1:
            res = res.transpose(vars2keep)
        elif len(vars2keep) == 0:
            res = res.histo
        return res

    def Draw(self, vars2keep=None, opts='', isSumw2=False, **kargs):
        if vars2keep == None:
            vars2keep = self.variables
        if isinstance(vars2keep,str):
            vars2keep = [vars2keep]
        if len(vars2keep) > 3:
            raise ValueError('For now it works only for less than 4 dimensions')
        proj = self.project(vars2keep, **kargs)
        self.h_draw = nTable2histo(proj, isSumw2=isSumw2)
        self.h_draw.Draw(opts)
        return self.h_draw

    def matrixPlot(self, isSumw2=True, **kargs):
        ndim = self.histo.ndim
        drawables = []
        for i in range(ndim):
            drawables.append([])
            for j in range(ndim):
                if i == j:
                    drawables[i].append(self.Draw([i], isSumw2=isSumw2, **kargs))
                else:
                    drawables[i].append((self.Draw([i,j], **kargs), 'colz'+('text e' if isSumw2 else '')))
        return MultiCanvas(drawables)

        

        
def nTable2histo(nTable, title='', name='', latex_names={}, isSumw2=False):
    '''
    Convert nTable to the appropriate THnD depending of the dimension
    useful mainly for plotting porposes
    '''
    if not name:
        name = str(hash(nTable))
    if not title:
        title = 'histo'
        for var in nTable.variables:
            title += ';'+latex_names.get(var, var)
    if nTable.histo.ndim == 1:
        h = r.TH1D(name, title, len(nTable.edges[0])-1, nTable.edges[0])
        for i in range(h.GetNbinsX()):
            h.SetBinContent(i+1, nTable.histo[i].n)
            if isSumw2:
                h.SetBinError(i+1, nTable.histo[i].s)
    elif nTable.histo.ndim == 2:
        h = r.TH2D(name, title, len(nTable.edges[0])-1, nTable.edges[0], len(nTable.edges[1])-1, nTable.edges[1] )
        for i in range(h.GetNbinsX()):
            for j in range(h.GetNbinsY()):
                h.SetBinContent(i+1, j+1, nTable.histo[i,j].n)
                if isSumw2:
                    h.SetBinError(i+1, j+1, nTable.histo[i,j].s)
    elif nTable.histo.ndim == 3:
        h = r.TH3D(name, title, len(nTable.edges[0])-1, nTable.edges[0], len(nTable.edges[1])-1, nTable.edges[1], len(nTable.edges[2])-1, nTable.edges[2] )
        for i in range(h.GetNbinsX()):
            for j in range(h.GetNbinsY()):
                for k in range(h.GetNbinsZ()):
                    h.SetBinContent(i+1, j+1, k+1, nTable.histo[i, j, k].n)
                    if isSumw2:
                        h.SetBinError(i+1,j+1, k+1, nTable.histo[i, j, k].s)
    else:
        
        h = r.THnD(name, title, nTable.histo.ndim,
                   array.array('i', [len(i)-1 for i in nTable.edges]),
                   array.array('d', [i[0] for i in nTable.edges]),
                    array.array('d', [i[-1] for i in nTable.edges])
                    )
        nBins = [h.GetAxis(i).GetNbins() for i in range(h.GetNdimensions())]
        for iters in itertools.product(*[range(i) for i in nBins]):
            h.SetBinContent(array.array('i', [i+1 for i in iters]), nTable.histo[tuple(iters)].n)
            if isSumw2:
                h.SetBinError(array.array('i', [i+1 for i in iters]), nTable.histo[tuple(iters)].s)
    return h

def histo2nTable(histo, variables):
    '''
    Convert a histo (THn with n = 1,2,3) to a nTable, variables is the names of the variables [x, y, z]
    '''
    assert histo.GetDimension() == len(variables) # number of variables must be same dimension of histo
    assert histo.GetDimension() in [1, 2, 3] # nuber of dimension can be 1, 2, 3

    edges = []
    edges.append(np.zeros(histo.GetNbinsX()+1))
    histo.GetXaxis().GetLowEdge(edges[0])
    edges[0][-1] = histo.GetXaxis().GetBinUpEdge(histo.GetNbinsX())
    if histo.GetDimension() > 1:
        edges.append(np.zeros(histo.GetNbinsY()+1))
        histo.GetYaxis().GetLowEdge(edges[1])
        edges[1][-1] = histo.GetYaxis().GetBinUpEdge(histo.GetNbinsY())
    if histo.GetDimension() > 2:
        edges.append(np.zeros(histo.GetNbinsZ()+1))
        histo.GetZaxis().GetLowEdge(edges[2])
        edges[2][-1] = histo.GetZaxis().GetBinUpEdge(histo.GetNbinsZ())
    
    nt = NTable(variables=variables, edges = edges)

    if histo.GetDimension() == 1:
        for i in range(histo.GetNbinsX()):
            nt.histo[i].n = ufloat(histo.GetBinContent(i+1), histo.GetBinError(i+1))
    if histo.GetDimension() == 2:
        for i in range(histo.GetNbinsX()):
            for j in range(histo.GetNbinsY()):
                nt.histo[i][j] = ufloat(histo.GetBinContent(i+1, j+1), histo.GetBinError(i+1, j+1))
    if histo.GetDimension() == 3:
        for i in range(histo.GetNbinsX()):
            for j in range(histo.GetNbinsY()):
                for k in range(histo.GetNbinsZ()):
                    nt.histo[i][j][k] = ufloat(histo.GetBinContent(i+1, j+1, k+1), histo.GetBinError(i+1, j+1, k+1))

    return nt
    

class EffTable(NTable):
    '''
    Class to store and evaluate information about a single efficiency table
    Takes as an input two Ntables with the generated and the selected
    '''

    def __init__(self, gen=None, sel=None):

        if gen!=None and sel!=None:

            assert np.array([(i==j).all() for i, j in zip(gen.edges, sel.edges)]).all()
            
            self.variables = sel.variables
            self.edges = sel.edges
            gen_sumw, gen_sumw2 = unumpy.nominal_values(gen.histo), unumpy.std_devs(gen.histo)**2
            sel_sumw, sel_sumw2 = unumpy.nominal_values(sel.histo), unumpy.std_devs(sel.histo)**2
            eff = sel_sumw / gen_sumw
            s_eff = np.sqrt( ( (1 - 2 * sel_sumw/gen_sumw)*sel_sumw2 + (sel_sumw/gen_sumw)**2 * gen_sumw2 ) / gen_sumw**2 )
            self.histo = unumpy.uarray(eff, s_eff)
            self.removeNan(0)

            
    
    def project(self, vars2keep=[], n_gen=None, n_sel=None, ni_errors=True):
        '''
        return a nTable of lower dimension projecting out (i.e. summing over)
        the variables not present in vars2keep
        vars2keep can contain the strings with the name of the variables or the indexes

        give only one of n_gen and n_sel: they are nTables with number of gen or sel events
        because to compute efficiencies I have to know it

        n_gen xor n_sel can also be True: implies uniform distribution

        if both are None it is assumed "n_gen = True"

        if ni_errors is False put to zero all the errors for n_sel or n_gen. This is useful so if later I multiply again 
        by sum_ni (to get the ) I do not doublecount this error and can separate error coming from yield (stat) 
        from stat error from MC finite statistics (syst)
        '''
        assert n_gen == None or n_sel == None
        if  n_gen == None and n_sel == None:
            n_gen = True

        vars2keep = list(vars2keep)
        for i in range(len(vars2keep)):
            if unicode(vars2keep[i]).isnumeric():
                vars2keep[i] = self.variables[int(vars2keep[i])]
        vars2sum = tuple([i for i in self.variables if i not in vars2keep])
        index2sum = tuple([self.variables.index(i) for i in vars2sum])

        if len(vars2sum) != 0:

            res = EffTable()
            res.variables=[i for i in self.variables if i in vars2keep]
            res.edges = [self.edges[i] for i in range(len(self.edges)) if self.variables[i] in vars2keep]


            if n_gen != None:
                if n_gen == True:
                    n_gen = NTable(variables=vars2sum)
                    n_gen.histo = unumpy.uarray(np.ones([self.histo.shape[i] for i in index2sum]), np.zeros([self.histo.shape[i] for i in index2sum]))
                else:
                    n_gen = n_gen.project(vars2sum)

                if not ni_errors:
                    n_gen.histo = unumpy.uarray(unumpy.nominal_values(n_gen.histo), np.zeros(n_gen.histo.shape))
                n_gen.histo = n_gen.histo / n_gen.histo.sum()
                res.histo = np.tensordot(self.histo, n_gen.histo, axes=(index2sum, range(len(index2sum)))) 

            if n_sel != None:
                if n_sel == True:
                    n_sel = NTable(variables=vars2sum)
                    n_sel.histo = unumpy.uarray(np.ones([self.histo.shape[i] for i in index2sum]), np.zeros([self.histo.shape[i] for i in index2sum]))
                else:
                    n_sel = n_sel.project(vars2sum)

                if not ni_errors:
                    n_sel.histo = unumpy.uarray(unumpy.nominal_values(n_sel.histo), np.zeros(n_sel.histo.shape))    
                n_sel.histo = n_sel.histo / n_sel.histo.sum()
                tmp = 1 / self
                tmp.removeNan(0)
                tmp.histo = np.tensordot(tmp.histo, n_sel.histo, axes=(index2sum, range(len(index2sum))))
                tmp = 1/tmp
                tmp.removeNan(0)
                res.histo = tmp.histo
                #res.histo = 1 / np.tensordot(1/self.histo, n_sel.histo, axes=(index2sum, range(len(index2sum)))) 

        else:
            res = self

        if len(vars2keep) > 1:
            res = res.transpose(vars2keep)
        elif len(vars2keep) == 0:
            try:
                eff = res.histo.item()
            except AttributeError:
                eff = res.histo
            res = Efficiency(eff = eff.n, s_eff = eff.s)

        return res

  


#######################################################################################


