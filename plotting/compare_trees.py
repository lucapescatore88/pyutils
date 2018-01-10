#!/usr/bin/env python

import ROOT as r
from random import random
import array
import collections
from multi_plot import MultiPlot

def getHisto(tree, name, expr=None, region=None, nBins = None, cut='', title = None, opts= '', tree_cut='', tree_weight='',evtMax=1000000000, bins_limits=None, removeErrors=False):
    '''
    Function to return a histogram from a variable in a tree using
    TTree.Draw()
    For having norm put opts = "norm"
    bins_limits can be used to give directly the bins limits if they are not all the same, it works. It should be a list (1-D) or a list of 2 lists [[list x], [list y]] (2-D)
    '''
    if not expr: expr = name
    tmpAddName = str(random)
    cuts = []
    if cut != '': cuts.append(cut)
    if tree_cut != '': cuts.append(tree_cut)
    region_str = ''

    if len(expr.split(':'))==2:
        if region and len(region) == 4: # avoid coming here if region is set to min or max in CompareTreeVars
            expr_y, expr_x = expr.split(':')
            cuts += [expr_x+'>'+str(region[0]), expr_x+'<'+str(region[1]),expr_y+'>'+str(region[2]), expr_y+'<'+str(region[3])]
            region_str = '({0}, '+str(region[0])+', '+str(region[1])+', {1}, '+str(region[2])+', '+str(region[3])+')'
        else: region_str = '({0}, {1})'
        if nBins!=None: bin_str = region_str.format(*nBins)
        else: bin_str = region_str.format(100,100)
    else:
        if region:
            cuts += [expr+'>'+str(region[0]), expr+'<'+str(region[1])]
            region_str = '({0}, '+str(region[0])+', '+str(region[1])+')'
        else: region_str = '({0})'
        bin_str = region_str.format(nBins if nBins != None else 100)

    cut_string = ' && '.join(cuts)
    if tree_weight != '':
        cut_string = '('+cut_string+')*'+str(tree_weight) if cut_string else str(tree_weight)
    #print name+':', cut_string
    if bins_limits:
        if len(expr.split(':'))==2:
            x_bins = array.array('f', bins_limits[0])
            y_bins = array.array('f', bins_limits[1])
            h = r.TH2D(name+tmpAddName, '', len(x_bins)-1, x_bins, len(x_bins)-1, x_bins)
        else:
            x_bins = array.array('f', bins_limits)
            h = r.TH1D(name+tmpAddName, '', len(x_bins)-1, x_bins)
        tree.Draw(expr+'>>'+name+tmpAddName, cut_string, opts,evtMax)
    else:
        tree.Draw(expr+'>>'+name+tmpAddName+bin_str, cut_string, opts,evtMax)
        h = r.gDirectory.Get(name+tmpAddName)
    r.gROOT.cd()
    try:
        histo = h.Clone(name)
    except ReferenceError: #attempt to access a null-pointer
        raise ReferenceError(name+' '+expr+' does not work')
    if title is None:
        if len(expr.split(':'))==2:
            histo.SetTitle(';{1};{0}'.format(*expr.split(':')))
        else:
            histo.SetTitle(';{0};A.U.'.format(expr))
    else:
        histo.SetTitle(title)

    if removeErrors:
        histo.Sumw2(False)

    return histo



def _getHistoRegion(*args, **kargs):
    '''
    Return the range of an histograms by plotting it and getting the position of the first and the last bin;
    all the arguments are passed to getHisto
    '''
    hh = getHisto(*args, **kargs)
    if hh.GetDimension() == 1:
        return [hh.GetBinLowEdge(1), hh.GetBinLowEdge(hh.GetNbinsX())+hh.GetBinWidth(hh.GetNbinsX())]
    elif hh.GetDimension() == 2:
        return None #[hh.GetBinLowEdge(1), hh.GetBinLowEdge(hh.GetNbinsX())+hh.GetBinWidth(hh.GetNbinsX())]



class CompareTreeVars:


    def __init__(self, trees={}, names=None, exprs={}, regions={}, cuts={}, titles={}, trees_cuts={}, trees_weights={}, opts={}, common_cut='', normalise=True, maxEvts={}, default_region='max'):
        """

        trees is a dictionary of trees with {label: tree}

        names is list of names of histos to plot, a name can also be directly name of variable in tree

        exprs, regions, cuts, titles, opts are dictionary with informations of the histograms, they use as key the general name of the histogram

        common_cut is a cut to apply to all histograms

        normalise tells if the histos from different trees should be normalised, N.B. normalisation does not work if a region is not specified

        trees_cuts is a dictionary with {label : cut}
        the weights will be apply to the different trees so that I can use the same tree with different weights

        trees_weights is a dictionary with {label : weight}
        the cuts will be apply to the different trees so that I can use the same tree with different cuts

        maxEvts  is a dictionary with {label : evtMax}
        evtMax is the maximum number of events per tree which it analyze
        addOpts is a dictionary of dictionaries with other options to pass to Multiplot's Add

        default_region is to set automatically the default region for all the plots for which one is not specified (and get the normalisation right),
        special choices are 'min' and 'max' to get the intersection or the union of the histograms' regions
        """

        self.trees = collections.OrderedDict()
        self.trees_cuts = {}
        self.trees_weights = {}
        self.trees_maxEvts = {}
        self.removeErrors = {}
        self.addOpts = {}
        self.default_region = default_region

        for label in trees:
            self.addTree(
                label = label,
                tree = trees[label],
                tree_cut = trees_cuts.get(label,''),
                tree_weight = trees_weights.get(label,''),
                evtMax = maxEvts.get(label,1000000000),
                **self.addOpts.get(label,{}))

        self.common_cut = common_cut
        self.normalise = normalise
        self.histos_info = collections.OrderedDict()

        if names:
            for name in names:
                self.addVariable(
                    name = name,
                    expr = exprs.get(name),
                    region = regions.get(name, default_region),
                    cut = cuts.get(name,''),
                    title = titles.get(name),
                    opts = opts.get(name,''),
                    )


    def addTree(self, label, tree, tree_cut='', tree_weight='',evtMax = 1000000000, removeErrors=False, **add_opts):
        '''
        in add_opts I can put options for the constructor of MultiPlot
        removeErrors allow to plot histogram without errors (e.g. with fills) also when weights are present
        '''
        self.trees[label] = tree
        if tree_weight != '': self.trees_weights[label] = tree_weight
        if tree_cut != '': self.trees_cuts[label] = tree_cut
        self.trees_maxEvts[label] = evtMax
        self.addOpts[label] = add_opts
        self.removeErrors[label] = removeErrors



    def addVariable(self, name, expr=None, region='default', nBins = None, cut='', title=None, bins_limits=None, opts=''):
        if cut == '' or self.common_cut == '':
            cut += self.common_cut
        else:
            cut += ' && '+ self.common_cut
        if title == None: title = '{0};{0};A.U.'.format(name)
        if expr == None: expr = name
        if self.normalise: opts = 'norm ' + opts
        self.histos_info[name] = dict(
            expr = expr,
            region = self.default_region if region == 'default' else region,
            nBins = nBins,
            cut = cut,
            title = title,
            bins_limits=bins_limits,
            opts = opts,
            )


    def getMultiPlots(self, **kargv):
        '''
        Return dictionary of MultiPlot
        kargv get passed directly to constructor of multiplot, can be useful for example
        to pass directives on legend drawing
        '''
        MultiPlots = collections.OrderedDict()

        for name, infos in self.histos_info.items():
            MultiPlots[name] = MultiPlot(name, infos['title'],'h', **kargv)

            if str(infos['region']).lower() in ['min', 'max']:
                _region = str(infos['region']).lower()
                infos['region'] = None
                mins, maxs = [], []
                for label, tree in self.trees.items():
                    tree_cut = self.trees_cuts.get(label,'')
                    tree_weight = self.trees_weights.get(label,'')
                    tree_evtMax = self.trees_maxEvts.get(label, 1000000000)
                    region = _getHistoRegion(tree, name = label+'_'+name, tree_cut=tree_cut, tree_weight=tree_weight, evtMax = tree_evtMax, removeErrors= self.removeErrors[label], **infos)
                    mins.append(region[0])
                    maxs.append(region[1])
                if _region == 'min':
                    infos['region'] = [max(mins), min(maxs)]
                else:
                    infos['region'] = [min(mins), max(maxs)]


            for label, tree in self.trees.items():
                tree_cut = self.trees_cuts.get(label,'')
                tree_weight = self.trees_weights.get(label,'')
                tree_evtMax = self.trees_maxEvts.get(label, 1000000000)
                if len(infos['expr'].split(':'))==2 and 'prof' not in infos['opts']: # If is 2D-histo markers must be little dots, moreover normalization messes things up
                    infos['opts'] = infos['opts'].replace('norm ','')
                    if not self.addOpts[label].has_key('markerStyle'): self.addOpts[label]['markerStyle']=1
                else:
                    if not self.addOpts[label].has_key('markerStyle'): self.addOpts[label]['markerStyle']=None #keep default
                histo = getHisto(tree, name = label+'_'+name, tree_cut=tree_cut, tree_weight=tree_weight, evtMax = tree_evtMax, removeErrors= self.removeErrors[label], **infos)
                #if len(infos['expr'].split(':'))==2: histo.Scale(0.0000001/histo.Integral())
                if not self.addOpts[label].has_key('legMarker'): self.addOpts[label]['legMarker']= 'p'
                MultiPlots[name].Add(histo, label = label, **self.addOpts[label])

        return MultiPlots
