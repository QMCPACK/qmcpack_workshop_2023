#! /usr/bin/env python3

from diamond_setup import system,qmc_job

from nexus import generate_qmcpack
from nexus import run_project

qmc = generate_qmcpack(
    identifier   = 'vmc_batched',
    path         = './',
    job          = qmc_job,
    input_type   = 'basic',
    system       = system,
    pseudos      = ['C.BFD.xml'],
    orbitals_h5  = './diamond.orbitals.h5',
    jastrows     = './diamond.jastrow.xml',
    corrections  = [],
    qmc          = 'vmc',
    driver       = 'batched',
    warmupsteps  =  50,
    blocks       = 800,
    steps        =  10,
    substeps     =   3,
    timestep     = 0.3,
    usedrift     = True,
    )

run_project()
