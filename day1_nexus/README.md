# Driving the Batched Code with Nexus

## General details

* Diamond primitive cell (diamond.poscar)
* BFD pseudopotential (C.BFD.xml)
* DFT planewave/B-spline orbitals (diamond.orbitals.h5)
* Two body Jastrow (diamond.jastrow.xml)

## Examples

* Variational Monte Carlo (diamond_vmc_batched.py)
* Optimization: Variance Minimization (diamond_opt_vmin_batched.py)
* Optimization: Energy Minimization (diamond_opt_emin_batched.py)
* Diffusion Monte Carlo (diamond_dmc_batched.py)
* DMC with Physical Observables (diamond_dmc_est_batched.py)
* VMC on GPU's with OpenMP Offload (diamond_vmc_offload_batched.py)

## Other files

* Legacy versions of Nexus examples above (legacy_nexus_files)
* QMCPACK inputs and outputs for all examples (example_inputs_outputs)

## Running the Examples

* Have working installs of QMCPACK and Nexus
* Update your path to QMCPACK (CPU real build) in diamond_setup.py
* (if necessary) update workstation/job core counts in diamond_setup.py
* Execute any desired example scripts (e.g. ./diamond_vmc_batched.py)
* Note: the GPU offload example (diamond_vmc_offload_batched.py) is intended to be run with the GPU/offload real build of QMCPACK.  Build this version of the code (and have an available GPU) for representative results.

