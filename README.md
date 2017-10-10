# What is this repository

Module with various useful python functions and classes to deal with ROOT and friends
in a physics analysis.

_Authors: G. Dujany (giulio.dujany@cern.ch), L. Pescatore (luca.pescatore@cern.ch)_

# Structure

Where awailable you can find readme files into each folder.

- db :
    * ```particle_DB``` (Luca): Implements a database accssible in python containing particles properties as defined in LHCb
    * ```cut_converter``` (Luca): Converts a C++ file with TCuts into a python object
- editing :
    * ```formatter``` (Luca): Extends the python format() function to handle missing values
    * ```latex_builder``` (Luca): Allows to easyly build and compile latex documents automatically.
- efficiencies :
    * ```distrEffs``` (Giulio): 
- editing :
    * ```addPID``` (Luca): Given PID tables and MC files it adds the weight to the MC
    * ```value``` (Luca): Extends python number formatting to allow to chose the power to display
- efficiencies :
    * ```compare_trees``` (Giulio): Compares variables from two trees
    * ```multi_plot``` (Giulio): 
    * ```multi_canvas``` (Giulio): 
- processing :
    * ```submit``` (Luca): Script to easily submit jobs in local or lxplus batch
    * ```process_data``` (Luca): Run an action (add variables or cut) on several trees
    * ```multi_process``` (Giulio): Run more actions in parallel