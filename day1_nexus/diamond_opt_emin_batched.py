#! /usr/bin/env python3

from diamond_setup import system,qmc_job

from nexus import generate_qmcpack
from nexus import run_project

samples    = 51200
proc_elems = qmc_job.processes*qmc_job.threads
blocks     = 200
steps      = int(round(samples/(blocks*proc_elems)+.5))

opt = generate_qmcpack(
    identifier   = 'opt_emin_batched',
    path         = './',
    job          = qmc_job,
    input_type   = 'basic',
    system       = system,
    pseudos      = ['C.BFD.xml'],
    orbitals_h5  = './diamond.orbitals.h5',
    J2           = True,
    corrections  = [],
    qmc          = 'opt',
    driver       = 'batched',
    minmethod    = 'oneshift',
    init_cycles  = 3,
    cycles       = 6,
    blocks       = blocks,
    steps        = steps,
    )

run_project()
