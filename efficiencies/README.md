# Efficiencies utilities

This submodule defines the following utilities classes. All the relevant methods
should have clear docstrings so

## Efficiency
Can be used to compute an efficiency given the number of events before and after a cut_converter

By default compute the binomial error sqrt((epsilon * (1-epsilon)/N) but can also
give the variance of generated and selected events and their covariance and
simple error propagation will be applied. Another option is to give the sum of
squared weights for generated and selected events.

```python
eff = Efficiency(n_gen=100, n_sel=50)

eff.eff # efficiency
eff.s_eff # error
eff.ufloat # efficiency as ufloat
```

The four basic operations and sqrt are defined along with two funtions that use `pickle`
to write to and read from a file

## NTable
Essentially a n-dimentional histogram to store yields that can be later used to make
n-dimentional histograms of efficiencies.

Can be constructed starting from a ROOT histogram or from
a ROOT tree (or pandas DataFrame or numpy recarray) and accepts also weights.
Possible to store also sum of square weights to have error propagation.
The four basic operations and sqrt are defined along with two funtions that use `pickle`
to write to and read from a file.

Some examples:

```python
nt = NTable(variables = ['x', 'y'], tree = my_tree, nBins = (20, 40),
            ranges = [(-100, 100), (0, 1)],
            cut = 'z > 0.5', weights_var = 'w')

# List of variables
nt.variables

# Bin edges
nt.edges

# numpy array with bin contents
nt.histo

# numpy array with only bin contents values (no errors)
nt.val

# numpy array with only errors
nt.err

# numpy array with relative errors
nt.rel_err

# Plot ROOT histogram
nt.Draw(opts='colz')

# Change order of variables
new_nt = nt.transpose(['y', 'x'])

# Sum over variable 'y'
new_nt = nt.project(vars2keep = ['x'])

# Keep only first bin in y
new_nt = nt.keepOnlyBin(var='y', bin=0)

# return numpy array with weights
weights = getWeights(my_tree)
```

## EffTable
derives from NTable and can be constructed from two NTables for
 generated and selected events
 ```python
eff = EffTable(gen=nt_gen, sel=nt_sel)
 ```

 The method `project` takes as input also an NTable with the generated or the
 selected events
