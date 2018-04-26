# What is this repository

Module with various useful python functions and classes to deal common tasks in a LHCb analysis.

_Authors: G. Dujany (giulio.dujany@cern.ch), L. Pescatore (luca.pescatore@cern.ch)_

# Structure

Where available you can find readme files into each folder.

- db :
    * ```particle_DB``` (Luca): Implements a database accssible in python containing particles properties as defined in LHCb
    * ```cut_converter``` (Luca): Converts a C++ file with TCuts into a python object
- editing :
    * ```formatter``` (Luca): Extends the python format() function to handle missing values
    * ```latex_builder``` (Luca): Allows to easyly build and compile latex documents automatically.
    * ```nums_formatters``` (Luca): Allows to nicely format values e.g. detects significant digits.
- efficiencies :
    * ```distrEffs``` (Giulio): Classes to calulate efficiencies with errors in more dimensions.
- plotting :
    * ```compare_trees``` (Giulio): Compares variables from two trees
    * ```multi_plot``` (Giulio): 
    * ```multi_canvas``` (Giulio): 
- processing :
    * ```multi_process``` (Giulio): Run more actions in parallel
- scripts : 
  This folder contains scripts that are intended to be run interactively but often can also be imported.
    * ```submit``` (Luca): Script to easily submit jobs in local, LSF (lxplus batch) or SLURM
    * ```check_jobs``` (Luca): Script to check jobs status on LSF
    * ```remotels``` (Luca): Script to ls EOS from wherever XRootD is installed. Even your laptop.
    