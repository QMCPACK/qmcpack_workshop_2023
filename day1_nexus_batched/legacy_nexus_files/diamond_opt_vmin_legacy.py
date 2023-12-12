#! /usr/bin/env python3

from diamond_setup import system,qmc_job

from nexus import generate_qmcpack
from nexus import run_project

opt = generate_qmcpack(
    identifier   = 'opt_vmin_legacy',
    path         = './',
    job          = qmc_job,
    input_type   = 'basic',
    system       = system,
    pseudos      = ['C.BFD.xml'],
    orbitals_h5  = './diamond.orbitals.h5',
    corrections  = [],
    J2           = True,
    qmc          = 'opt',
    cycles       = 6,
    samples      = 51200,
    )

run_project()
