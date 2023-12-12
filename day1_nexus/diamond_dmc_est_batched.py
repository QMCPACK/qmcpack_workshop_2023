#! /usr/bin/env python3

from diamond_setup import system,qmc_job

from nexus import generate_qmcpack
from nexus import run_project

from qmcpack_input import spindensity
from qmcpack_input import momentumdistribution
from qmcpack_input import onebodydensitymatrices,sposet

estimators = [
    spindensity(
        dr         = (0.3,0.3,0.3)
        ),
    momentumdistribution(
        kmax       = 4,
        samples    = 20,
        ),
    onebodydensitymatrices(
        basis      = sposet(type='bspline',size=8),
        reuse      = True,
        integrator = 'uniform_grid',
        points     = 4,
        center     = (0,0,0),
        ),
    ]

qmc = generate_qmcpack(
    identifier       = 'dmc_est_batched',
    path             = './',
    job              = qmc_job,
    input_type       = 'basic',
    system           = system,
    pseudos          = ['C.BFD.xml'],
    orbitals_h5      = './diamond.orbitals.h5',
    jastrows         = './diamond.jastrow.xml',
    corrections      = ['mpc'],
    estimators       = estimators,
    qmc              = 'dmc',
    driver           = 'batched',
    # vmc
    vmc_warmupsteps  =  50,
    vmc_blocks       = 100,
    vmc_steps        =   5,
    vmc_substeps     =   3,
    vmc_timestep     = 0.3,
    vmc_usedrift     = True,
    # dmc equilibration
    eq_dmc           = True,
    eq_warmupsteps   = 20,
    eq_blocks        = 20,
    eq_steps         =  5,
    eq_timestep      = 0.02,
    # main dmc
    total_walkers    = 1024,
    warmupsteps      = 20,
    blocks           = 200,
    steps            =  10,
    timestep         = 0.01,
    nonlocalmoves    = True,
    )

run_project()
