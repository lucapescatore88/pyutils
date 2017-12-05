
"""
Functions to deal with roofit datasets and others
"""

try:
    import ROOT as r
    from root_numpy import tree2array, array2tree
except ImportError:
    print "ROOT not found, funtions to deal with RooFit not available"


def makeRooArgSet(ll, isArgList=False):
    '''
    take as input a list an return a RooArgSet,
    useful because RooArgSet constructor does not work for lists
    longer than 12
    If isArgList is True return an ArgList instead of an ArgSet
    '''
    def chunks(l, n):
        return [l[i:i+n] for i in range(0, len(l), n)]
    vars_slices = chunks(ll, 6)
    if isArgList:
        returnArgSet = r.RooArgList(*vars_slices[0])
    else:
        returnArgSet = r.RooArgSet(*vars_slices[0])
    for var_slice in vars_slices[1:]:
        returnArgSet.add(r.RooArgSet(*var_slice))
    return returnArgSet


def makeRooDataset(tree, vars, helpingVars, datasetName, datasetDescription, weightsName=None, cut=''):
    '''
    vars is a dictionary {varName: (min, max)}
    helpingVars is a list of variables I also want in the dataset but without cuts
    '''

    rooVars = {}
    for var, spread in vars.items():
        rooVars[var] = r.RooRealVar(var, var, spread[0], spread[1])
        #cut += '&& {0} > {1} && {0} < {2}'.format(var, *spread)

    cuts_vars = ' && '.join(['{0} > {1} && {0} < {2}'.format(var, *spread) for var, spread in vars.items()])
    cut = cut+' && '+cuts_vars if cut != '' and cuts_vars != '' else cut+cuts_vars

    if weightsName:
        helpingVars.append(weightsName)
    for var in helpingVars:
        rooVars[var] = r.RooRealVar(var, var, 0)
        rooVars[var].setConstant(False)

    dataArgSet = makeRooArgSet(rooVars.values())

    arr = tree2array(tree, branches = vars.keys()+helpingVars, selection=cut)
    tree = array2tree(arr)

    if weightsName:
        dataSet = r.RooDataSet(datasetName, datasetDescription, tree, dataArgSet, '1', weightsName)
    else:
        dataSet = r.RooDataSet(datasetName, datasetDescription, tree, dataArgSet)
    return dataSet



def makeRooMultiDataset(trees, vars, helpingVars, datasetName, datasetDescription, categoryName = 'sample', weightsName=None, cut=''):
    '''
    trees is a dictionary with {mode: tree}
    vars is a dictionary {varName: (min, max)}
    helpingVars is a list of variables I also want in the dataset but without cuts
    '''

    rooVars = {}
    for var, spread in vars.items():
        rooVars[var] = r.RooRealVar(var, var, spread[0], spread[1])

    if weightsName:
        helpingVars.append(weightsName)
    for var in helpingVars:
        rooVars[var] = r.RooRealVar(var, var, 0)
        rooVars[var].setConstant(False)

    dataArgSet = makeRooArgSet(rooVars.values())

    _trees = {}
    for mode, tree in trees.items():
        arr = tree2array(tree, branches = vars.keys()+helpingVars, selection=cut)
        _trees[mode] = array2tree(arr)

    sample = r.RooCategory(categoryName, categoryName)
    dataSets = {}
    dataSetImport = {}
    for mode, tree in _trees.items():
        sample.defineType(mode)
        dataSets[mode] = r.RooDataSet('{0}_{1}'.format(datasetName, mode), datasetDescription, tree, dataArgSet)
        dataSetImport[mode] = r.RooFit.Import(mode, dataSets[mode])

    for i in dataSets.values(): i.Print()

    combDataSet = r.RooDataSet(datasetName,datasetDescription, dataArgSet, r.RooFit.Index(sample), *dataSetImport.values())
    combDataSet.Print()
    return combDataSet
