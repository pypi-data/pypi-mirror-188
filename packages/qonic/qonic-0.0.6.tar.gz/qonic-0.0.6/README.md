[![Python application](https://github.com/Qonic-Team/qonic/actions/workflows/python-app.yml/badge.svg)](https://github.com/Qonic-Team/qonic/actions/workflows/python-app.yml)
[![CodeQL](https://github.com/Qonic-Team/qonic/actions/workflows/codeql.yml/badge.svg)](https://github.com/Qonic-Team/qonic/actions/workflows/codeql.yml)
<sup>[`Snyk Vulnerability Report`](https://snyk.io/test/github/Qonic-Team/qonic?targetFile=source_dir/requirements.txt)</sup>

# qonic
The Qonic project is an open source, expandable framework for solving problems using hybrid quantum computing solutions.  The base library includes tools for defining optimization problems to be run on gate quantum computers on a variety of backends or simulators, as well as on simulated or physical quantum annealers.

**To install:** `pip3 install qonic`

## QProgram

## ConstraintSatisfaction
Constraint satisfaction is the process of finding a configuration of variables that satisfy a set of constraints imposed on those variables.  The `ConstraintSatisfactionProblem` class allows for mapping constraints from a CSP onto a binary quadratic model (BQM).  Once formulated as a BQM, a valid configuration can be searched for by using simulated or quantum annealing algorithms.
### _`class`_`ConstraintSatisfactionProblem`
**Methods**  
* `fromStr(constraint, binary, real, complx)`
  **Description:**
  This function adds a constraint to the current CSP object from a string.  The constraint string can be made up of:
  * variables
    * these can be binary bits, or 16 bit real floats, or 32 bit complex floats.  Note that the float variables are are not technically represented with floats, but rather approximations constructed from binary polynomial sentences.  This is done so that the variables can be broken up and converted into a BQM
    * ⚠️ NOTE: variables can have any name that does not contain spaces or special characters (eg ! - / etc), with the exception of names of the form `f[number]` or `j[number]` (eg `'f12'`, `'j51.34'`) as these are special names reserved for use by the constraint parser
  * binary operations `and`, `or`, `not` applied to binary variables and relational operators `==` and `!=` for requiring two terms to be equal or not equal respectively
  * polynomial expressions constructed from variables 
    * terms can be combined with `+` and `-` operations
    * coefficients can be combined with `*` and `/` operations
    * terms can be raised to a given (integer) power using `**`
    * terms can be grouped using parentheses 
    * relational operators `==`, `!=`, `<`, `<=`, `>`, `>=` can be used to require one expression to be equal to, not equal to, less than, less than or equal to, greater than, or greater than or equal to another expression.

  **Parameters:**
  * `constraint <type 'string'>`: a single string storing a constraint expression (see above description for formatting)
  * `binary <type 'list'>`: a list of the binary variables used in the constraint (variable names stored in strings)
  * `real <type 'list'>`: a list of the real 16 bit float variables used in the constraint (variable names stored in strings)
  * `complx <type 'list'>`: a list of the complex 32 bit float variables used in the constraint (variable names stored in strings)

  **Example:**
  ```python
  >>> CSP = qonic.ConstraintSatisfactionProblem()
  >>> # add a new constraint on binary variable 'd', 16 bit floats 'a' and 'b', and 32 bit complex float 'c'
  >>> CSP.fromStr('a * b > c**2 or d', ['d'], ['a', 'b'], ['c'])
  ```

* `fromFile(filename)`
  **Description:**
  This function adds constraint(s) to the current CSP object from a yaml file.  The yaml file should have the following structure:
  * `constraint0`: the first constraint stored in a string
  * `constraint1`: the second constraint stored in a string
   ⋮
  * `constraintN`: the (N-1)th constraint stored in a string.  Note that the constraints can use any key within the file as long as `constraint` is contained within it
  * `binary`: a list of the binary variables used in the constraint (variable names stored in strings)
  * `real`: a list of the real 16 bit float variables used in the constraint (variable names stored in strings)
  * `complx`: a list of the complex 32 bit float variables used in the constraint (variable names stored in strings)

  **Parameters:**
  * `filename <type 'string'>`: the path to the file location of the yaml file storing the constraints

  **Example:**
  * example `constraints.yaml` file:
    ```yaml
    # first the constraints
    constraint0: "a * b > c**2 or d"
    my_constraint: "a**3 > 1 and e"
    another_constraint: "d == e"

    # now specify the variables
    binary: ["d", "e"]
    real: ["a", "b"]
    complx: ["c"]
    ```
  * example python script:
    ```python
    >>> CSP = qonic.ConstraintSatisfactionProblem()
    >>> # add a new constraint from a yaml file
    >>> CSP.fromFile('constraints.yaml')
    ```

* `toQUBO()`
  **Description:**
  This function returns the constraints in the form of a quadratic unconstrained binary optimization problem (or QUBO)

  **Returns:**
  * `({(vars): biases}, offset) <type 'tuple'>`: a tuple containing the biases between variables as a dictionary, and the offset of the QUBO

  **Example:**
   ```python
  >>> self.toQUBO()
  ({('b0', 'b1'): -3.9999999991051727, ('b0', 'b0'): 1.999999998686436, ('b1', 'b1'): 1.9999999986863806}, 8.661749095750793e-10)
  ```

* `checkConfiguration(configuration, err=0.0)`
  **Description:**
  This function takes a dictionary of values of variables and returns the number of constraints satisfied by the configuration (within a margin of error specified in err)

  **Parameters:**
  * `configuration <type 'dict'>`: the configuration of variables stored in a dictionary of the form `{'variable': value}`
  * `err <type 'float'>`: the margin of error when checking constraints with relational operators `==`, `!=`, `<`, `<=`, `>`, `>=`

  **Returns:**
  * `constraintsMet <type 'int'>`: the number of constraints within the CSP that are satisfied by the passed configuration

  **Example:**
  ```python
  >>> self.fromString('(a or b) and c', ['a', 'b', 'c'], [], [])
  >>> self.checkConfiguration({'a': 1, 'b': 0, 'c': 1}, 0.1) # should return that 1 constraint is satisfied by this configuration
  1
  ```

**Attributes**
* `__b <type 'dict'>`: a dictionary storing a list of binary variables and the corresponding names
* `__f <type 'dict'>`: a dictionary storing the binary polynomial expressions approximating 16 bit real floats (stored as strings) and the corresponding float variable names
* `__j <type 'dict'>` a dictionary storing the binary polynomial expressions approximating 32 bit complex floats (stored as strings) and the corresponding float variable names