#!/usr/bin/env python
from __future__ import division
from math import sqrt
import pickle, os
from uncertainties import ufloat
try:
    from pyutils.nums import roundPair
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'../..'))
    from pyutils.nums import roundPair

class Efficiency:
    '''
    Class to store and evaluate information about a single efficiency
    '''
    def __init__(self, eff=None, s_eff=None, n_gen=None, n_sel=None, s2_n_gen=None, s2_n_sel=None, cov_n_gen_sel=None, sumw2_sel=None, sumw2_gen=None):

        self.eff = 0
        self.s_eff = 0

        if n_gen is not None and n_sel is not None:
            try:
                self.eff = n_sel/n_gen
                if s2_n_gen is not None and s2_n_sel is not None and cov_n_gen_sel is not None:
                    self.s_eff = n_sel/n_gen * sqrt( s2_n_sel/n_sel**2 + s2_n_gen/n_gen**2 - 2*cov_n_gen_sel/(n_sel*n_gen) )
                else: # self.s_eff = sqrt( self.eff * abs(1-self.eff) / n_gen )
                    if sumw2_sel is None: sumw2_sel = n_sel
                    if sumw2_gen is None: sumw2_gen = n_gen
                    self.s_eff = sqrt( ( (1 - 2 * n_sel/n_gen)*sumw2_sel + (n_sel/n_gen)**2 * sumw2_gen ) / n_gen**2 )
            except ZeroDivisionError:
                pass # keep default 0, 0

        if eff is not None: self.eff = eff
        if s_eff is not None: self.s_eff = s_eff

        # Protection against wrong values given by sWeights and similar
        if self.eff < 0: self.eff = 0
        if self.s_eff < 0: self.s_eff = 0
        if self.eff > 1: self.eff = 1
        if self.s_eff > 1: self.s_eff = 1

    @property
    def s_rel_eff(self):
        return self.s_eff/self.eff

    @property
    def ufloat(self):
        return ufloat(self.eff,self.s_eff)

    def __str__(self):
        return 'efficiency = '+str(self.eff)+'\n'+\
            'error = '+str(self.s_eff)+'\n'+\
            'relative error = '+str(self.s_rel_eff)

    def saveToFile(self, fileName = "efficiency.txt"):
        '''
        Use pickle to save to file
        '''
        pickle.dump(self, open( fileName, "wb" ))

    def loadFromFile(self,fileName = "efficiency.txt"):
        '''
        Use pickle to load from to file
        '''
        return pickle.load( open( fileName, "rb" ) )

    def __repr__(self):
        val, err = roundPair(self.eff, self.s_eff)
        return val+' +- '+err

    #def __r

    def __add__(self, other):
        res = Efficiency()
        res.eff = self.eff + other.eff
        res.s_eff = sqrt(self.s_eff**2 + other.s_eff**2)
        return res

    def __sub__(self, other):
        res = Efficiency()
        res.eff = self.eff - other.eff
        res.s_eff = sqrt(self.s_eff**2 + other.s_eff**2)
        return res

    def __mul__(self, other):
        res = Efficiency()
        if hasattr( other, 'eff'): # Multiply by another efficiency
            res.eff = self.eff * other.eff
            try:
                res.s_eff = res.eff * sqrt( (self.s_eff/self.eff)**2 + (other.s_eff/other.eff)**2)
            except ZeroDivisionError:
                res.s_eff = 1
        elif hasattr( other, 'std_dev'): # Multiply by a ufloat
            self_ufloat = ufloat(self.eff, self.s_eff)
            result = self_ufloat*other
            res.eff = result.n
            res.s_eff = result.s
        else: # Multiply by a number
            res.eff = self.eff * other
            res.s_eff = self.s_eff * other
        return res

    def __div__(self, other):
        res = Efficiency()
        if hasattr( other, 'eff'): # Divide by another efficiency
            res.eff = self.eff / other.eff if self.eff else self.eff
            try:
                res.s_eff = res.eff * sqrt( (self.s_eff/self.eff)**2 + (other.s_eff/other.eff)**2)
            except ZeroDivisionError:
                res.s_eff = 1
        elif hasattr( other, 'std_dev'): # Divide by a ufloat
            self_ufloat = ufloat(self.eff, self.s_eff)
            result = self_ufloat / other
            res.eff = result.n
            res.s_eff = result.s
        else: # Divide by a number
            res.eff = self.eff / other
            res.s_eff = self.s_eff / other
        return res

    __truediv__ = __div__



#################################################
# Import submodules
try:
    from distrEffs import *
except ImportError: # When run PID I setup urania and do not have fancy python tools like root_numpy
    print 'Not able to import distrEffs'
    pass
#################################################
