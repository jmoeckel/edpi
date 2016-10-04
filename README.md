# Extended Dymola-Python-Interface
An extended version of the Python interface provided by Dymola

### Content
Dymola provides a Python (2.7) interface. Unfortunately, the included `simulateModel` function only returns a success-boolean but not the actual simulation results. These have to be re-imported (using the API of the interface of some other .mat reader). 

The dpi-module extends the Dymola-Python interface by one module `simulateModelwithResults` which provides the possibility to simulate a model with given simulation settings AND automatically use the simulated values, which are provided as an output in form of a dictionary. 

### Except from the `simulateModelwithResults()`-documentation (Sphinx-syntax)
````Sphinx
:param trajectoryNames: The possibility, to choose, which simulated
  parameters should be included in the output 'data'. If not set, all
  results are returned.
:type trajectoryNames: list (of strings)

:returns: A dictionary, that contains simulated values. This dictionary
  structure is: {'param name':[param values]}
:rtype: dict

:raises: DymolaException, if the simulation fails

..note: 
    Besides the additional input argument 'trajectoryNames' and the
    output parameter, this module provides the exact the same API as
    'simulateModel'. So for more informations regarding different
    input-arguments, see the documentation for 'simulateModel'
````
### Requirements
- Dymola 2015 or newer
- Python 2.x (as the interface itsself does not support Python 3.x)

### Usage
```` Python
import dpi
dymola = dpi.DymolaInterface

# From here on, use the Interface described as in the documentation provided by
# Dymola.
````

### Note
The path to Dymola is gained by evaluating Windows environmental variables. If 
your Dymola installation is not registered, add the path to the interface 
manually by `sys.path.append([YOUR PATH])` before invoking `dpi.DymolaInterface()`.
