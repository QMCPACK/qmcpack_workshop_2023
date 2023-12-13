
# Surrogate Hessian Structure Optimization on an Artificial PES


## Example description

Artificial model involving three coupled Morse oscillators.

Surrogate and actual PES's represented by different (but related) 
coupled Morse oscialltor systems.

Deterministic structural relaxation along the surrogate PES performed 
with numerical methods in scipy rather than DFT.

The full surrogate hessian parallel line search algorithm is performed 
on the actual PES (different from the surrogate) with added statistical 
noise to represent DMC.


## Installation requirements

* Standard Python libraries needed: numpy, dill, scipy, matplotlib

  pip3 install numpy
  pip3 install dill
  pip3 install scipy
  pip3 install matplotlib

* Nexus

  git clone https://github.com/QMCPACK/qmcpack.git
  export PYTHONPATH=/your/path/to/qmcpack/nexus/lib/:$PYTHONPATH
  
* Surrogate Hessian Relax

  git clone https://github.com/QMCPACK/surrogate_hessian_relax.git
  export PYTHONPATH=/your/path/to/surrogate_hessian_relax:$PYTHONPATH


## Running the example

./morse_3p.py


## What to look for

* Minimum energy parameters of the surrogate PES ("DFT" structure)

* Details of the surrogate hessian (note degree of coupling)

* User defined parameter tolerances (requested parameter accuracy)

* Convergence of parameters with parallel iteration count (also note error bars on/statistical uncertainty of the parameters

* (analytic/reference) minimum energy parameters of the actual PES ("DMC" structure), and how they compare with the parameters found via line search (including statistical uncertainty)

