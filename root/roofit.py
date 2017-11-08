
"""
Functions to deal with roofit datasets and others
"""

try:
    import ROOT as r
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


def makeRooDataset(tree, vars, helpingVars, datasetName, datasetDescription, weightsName=None):
    '''
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

    if weightsName:
        dataSet = r.RooDataSet(datasetName, datasetDescription, tree, dataArgSet, '1', weightsName)
    else:
        dataSet = r.RooDataSet(datasetName, datasetDescription, tree, dataArgSet)
    return dataSet


def makeRooMultiDataset(trees, vars, helpingVars, datasetName, datasetDescription, categoryName = 'sample', weightsName=None):
    '''
    trees is a dictionary with {mode: tree}
    vars is a dictionary {varName: (min, max)}
    helpingVars is a list of variables I also want in the dataset but without cuts
    '''

    rooVars = {}
    for var, spread in vars.items():
        rooVars[var] = r.RooRealVar(var, var, spread[0], spread[1])


    for var in helpingVars:
        rooVars[var] = r.RooRealVar(var, var, 0)
        rooVars[var].setConstant(False)

    dataArgSet = makeRooArgSet(rooVars.values())

    sample = r.RooCategory(categoryName, categoryName)
    dataSets = {}
    dataSetImport = {}
    for mode, tree in trees.items():
        sample.defineType(mode)
        dataSets[mode] = r.RooDataSet('{0}_{1}'.format(datasetName, mode), datasetDescription, tree, dataArgSet)
        dataSetImport[mode] = r.RooFit.Import(mode, dataSets[mode])

    for i in dataSets.values(): i.Print()

    combDataSet = r.RooDataSet(datasetName,datasetDescription, dataArgSet, r.RooFit.Index(sample), *dataSetImport.values())
    combDataSet.Print()
    return combDataSet
