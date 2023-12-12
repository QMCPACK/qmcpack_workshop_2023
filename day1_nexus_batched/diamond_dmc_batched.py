#! /usr/bin/env python3

from diamond_setup import system,qmc_job

from nexus import generate_qmcpack
from nexus import run_project

qmc = generate_qmcpack(
    identifier       = 'dmc_batched',
    path             = './',
    job              = qmc_job,
    input_type       = 'basic',
    system           = system,
    pseudos          = ['C.BFD.xml'],
    orbitals_h5      = './diamond.orbitals.h5',
    jastrows         = './diamond.jastrow.xml',
    corrections      = [],
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
