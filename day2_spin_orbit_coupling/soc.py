#! /usr/bin/env python3

# Run with SOC
withSOC = True

from nexus import settings,job,run_project,obj
from nexus import generate_physical_system
from nexus import generate_pwscf
from nexus import generate_pw2qmcpack
from nexus import generate_qmcpack
from nexus import generate_convertpw4qmc
from nexus import loop, linear, vmc, dmc

settings(
    pseudo_dir = 'pseudopotentials',
    results    = '',
    sleep      = 3,
    machine    = 'YOUR MACHINE HERE', 
    account    = 'YOUR ACCOUNT HERE'
    )

#add your modules here
qmc_modules='''
module purge
module load gnu/12.1.1
module load intel/23.2.0
module load mkl/23.2.0
module load openmpi-gnu/4.1
module load cmake/3.25.2
module list

export  HDF5_ROOT=/projects/lsgroup/hdf5/1.14.0/hdf5
export BOOST_ROOT=/projects/lsgroup/boost/1.78.0
'''

#path to binaries
pwscf   = "pw.x"
pw2qmc  = "pw2qmcpack.x"
cpw4qmc = "convertpw4qmc"
qmccomplex = "qmcpack_complex"
qmcjob = job(nodes=12, processes_per_node=2, threads=56, hours=4, app=qmccomplex, presub=qmc_modules, queue='short')

system = generate_physical_system(
    units    = 'A',
    axes     = '''
        0.0000000000         3.2456000031         3.2456000031
        3.2456000031         0.0000000000         3.2456000031
        3.2456000031         3.2456000031         0.0000000000
        ''',
    elem_pos = '''
     Sn  0.000000000         0.000000000         0.000000000
     Sn  1.622799993         1.622799993         1.622799993
               ''',
    kgrid    = (1,1,1),
    Sn       = 4,
    )


# Here, we are specifying the common pwscf arguments between the no SOC and with SOC 
# calculations.
pwscf_common_arguments = obj(
    identifier  = 'scf',
    input_type  = 'generic',
    job         = job(cores=8, app=pwscf),
    calculation = 'scf',
    ecutwfc     = 200,
    conv_thr    = 1e-08,
    system      = system,
    kgrid       = (4,4,4),
    kshift      = (1,1,1),
)
# Here, these are the specialized input flags for the pwscf without SOC. Note the
# use of a (A)veraged (R)elativistic (E)ffective Core (P)otential (AREP)
# this includes up to scalar relativistic effects, i.e., no SOC
pwscf_woSOC_arguments = obj(
    path    = 'scf/woSOC',
    pseudos = ['Sn.ccECP.AREP.upf'],
)
# Here, these are the specialized input flags for the pwscf with SOC. Note the 
# use of a (S)pin (O)rbit (R)elativistic (E)ffective Core (P)otential (SOREP)
# this includes the terms in the AREP, but also has spin-orbit coupling
# We also set the pwscf noncolin and lspinorb flags to true
pwscf_wSOC_arguments = obj(
    path     = 'scf/wSOC',
    pseudos  = ['Sn.ccECP.SOREP.upf'],
    noncolin = True,
    lspinorb = True,
)
# Choose with arguments to include depending on if we are running with SOC or not
if withSOC:
    pwscf_args = obj(**pwscf_common_arguments, **pwscf_wSOC_arguments)
else:
    pwscf_args = obj(**pwscf_common_arguments, **pwscf_woSOC_arguments)
scf = generate_pwscf(**pwscf_args)


# using different kpoints from the converged density
# for demonstration
nscf_common_arguments = obj(
    identifier   = 'nscf',
    job          = job(cores=8,app=pwscf),
    input_type   = 'generic',
    calculation  = 'nscf',
    input_dft    = 'pbe',
    system       = system,
    conv_thr     = 1e-8,
    ecutwfc      = 200,
    nosym        = True,
    kgrid        = (1,1,1),
    kshift       = (1,1,1),
    dependencies = (scf, 'charge_density'),
)
nscf_woSOC_arguments = obj(
    path    = 'nscf/woSOC',
    pseudos = ['Sn.ccECP.AREP.upf'],
)
nscf_wSOC_arguments = obj(
    path     = 'nscf/wSOC',
    pseudos  = ['Sn.ccECP.SOREP.upf'],
    noncolin = True,
    lspinorb = True,
)
if withSOC:
    nscf_arguments = obj(**nscf_common_arguments, **nscf_wSOC_arguments)
else:
    nscf_arguments = obj(**nscf_common_arguments, **nscf_woSOC_arguments)
nscf = generate_pwscf(**nscf_arguments)


# Currently, we have two separate converters depending on whether or not SOC is included
# For normal calculations, we go through the standard path using pw2qmcpack.x
# Spinor conversion is only supported through a qmcpack converter called convertpw4qmc
# and nexus support is limited. 
# this will change in the future when we incorporate spinors into 
if withSOC:
  conv = generate_convertpw4qmc(
        identifier = 'conv',
        path       = 'nscf/wSOC',
        job        = job(cores=1, app=cpw4qmc),
        dependencies = (nscf,'orbitals'),
    )
else:
  conv = generate_pw2qmcpack(
      identifier   = 'conv',
      path         = 'nscf/woSOC',
      job          = job(cores=8,app=pw2qmc),
      write_psir   = False,
      dependencies = (nscf,'orbitals'),
      )

#linear method optimization 
linear_arguments = obj(steps            = 10,
                       blocks           = 100,
                       walkers_per_rank = 56,
                       MinMethod        = 'OneShiftOnly',
                       usedrift         = False,
                      )
loop_arguments = obj(max = 10, qmc = linear(**linear_arguments))
opt_common_arguments = obj(
     identifier       = 'opt',
     job              = qmcjob,
     input_type       = 'basic',
     system           = system,
     J1               = True,
     J2               = True,
     driver           = 'batched',
     dependencies     = (conv,'orbitals'),
     calculations     = [loop(**loop_arguments)],
)
opt_woSOC_arguments = obj(
     path    = 'optJ2_batched/woSOC',
     pseudos = ['Sn.ccECP.AREP.xml'],
)
opt_wSOC_arguments = obj(
     path    = 'optJ2_batched/wSOC',
     pseudos = ['Sn.ccECP.SOREP.xml'],
     spinor  = 'yes',
)
if withSOC:
    opt_arguments = obj(**opt_common_arguments, **opt_wSOC_arguments)
else:
    opt_arguments = obj(**opt_common_arguments, **opt_woSOC_arguments)
opt = generate_qmcpack(**opt_arguments)
 
# An important step when doing dynamic spin DMC is that there is an additional parameter, namely the 
# spin mass which determines the rate of spin sampling relative to the spatial degrees of freedom. 
# Here, we will do a 2D scan of timesteps and spin masses to investigate the impact of spin mass

def createSpinorQMC(spinmass):
  #for VMC, just using default spinmass so not setting it
  vmc_input = obj(walkers_per_rank = 56, 
                  steps            = 50,
                  blocks           = 30,
                  usedrift         = True,
                  timestep         = 0.75
                 )
  dmc_input = obj(nonlocalmoves    = False,
                  blocks           = 30,
                  walkers_per_rank = 56,
                  spin_mass        = spinmass
                 )
  qmc_arguments = obj(
      path             = 'qmc_batched/wSOC/spinmass_{}'.format(spinmass),
      identifier       = 'qmc',
      job              = qmcjob,
      input_type       = 'basic',
      system           = system,
      J2               = True,
      qmc              = 'vmc',
      driver           = 'batched',
      spinor           = 'yes', 
      dependencies     = [(conv,'orbitals'),
                          (opt,'jastrow')],
      pseudos          = ['Sn.ccECP.SOREP.xml'],
      calculations     = [vmc(**vmc_input),
                          dmc(timestep = 0.1600, steps = 100, **dmc_input),
                          dmc(timestep = 0.0400, steps = 25,  **dmc_input),
                          dmc(timestep = 0.0100, steps = 100, **dmc_input),
                          dmc(timestep = 0.0025, steps = 400, **dmc_input)]
  )
  return generate_qmcpack(**qmc_arguments)

def createQMC():
  #for VMC
  vmc_input = obj(walkers_per_rank = 56, 
                  steps            = 50,
                  blocks           = 20,
                  usedrift         = True,
                  timestep         = 0.75
                 )
  dmc_input = obj(nonlocalmoves    = False,
                  blocks           = 30,
                  walkers_per_rank = 56,
                 )
  qmc_arguments = obj(
      path             = 'qmc_batched/woSOC',
      identifier       = 'qmc',
      job              = qmcjob,
      input_type       = 'basic',
      system           = system,
      J2               = True,
      qmc              = 'vmc',
      driver           = 'batched',
      dependencies     = [(conv,'orbitals'),
                          (opt,'jastrow')],
      pseudos          = ['Sn.ccECP.AREP.xml'],
      calculations     = [vmc(**vmc_input),
                          dmc(timestep = 0.1600, steps = 25, **dmc_input), # this is a warmup  with a large timestep
                          dmc(timestep = 0.0400, steps = 25,  **dmc_input), #all other timesteps are setup with each block being one unit of imaginary time
                          dmc(timestep = 0.0100, steps = 100, **dmc_input),
                          dmc(timestep = 0.0025, steps = 400, **dmc_input)]
  )
  return generate_qmcpack(**qmc_arguments)

if withSOC:
    for spinmass in [1e-04, 1e-02, 1e00, 1e02, 1e04, 1e06]:
        qmc = createSpinorQMC(spinmass)
else:
    qmc = createQMC()

run_project()
