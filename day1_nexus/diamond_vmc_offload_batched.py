#! /usr/bin/env python3

from diamond_setup import system

from nexus import generate_qmcpack,job
from nexus import run_project

from qmcpack_input import vmc

qmcpack_offload_exe = '/your/path/to/offload/qmcpack'

qmc_job = job(cores=12,threads=4,app=qmcpack_offload_exe)

walkers_scan = [   1,   2,   4,   8,  16,  32,
                  64,  96, 128, 180, 256, 300, 
                 360, 436, 512, 600, 720, 864,
                1024,1216,1440]

qmc = generate_qmcpack(
    identifier       = 'vmc_offload_scan',
    path             = './',
    job              = qmc_job,
    input_type       = 'basic',
    system           = system,
    pseudos          = ['C.BFD.xml'],
    orbitals_h5      = './diamond.orbitals.h5',
    jastrows         = './diamond.jastrow.xml',
    corrections      = [],
    driver           = 'batched',
    delay_rank       = 4,
    det_batch        = True,
    calculations     = [
        vmc(walkers_per_rank = walkers_per_rank,
            warmupsteps      =  50,
            blocks           = 800,
            steps            =  10,
            substeps         =   3,
            timestep         = 0.3,
            usedrift         = True,
            #crowds           = , # integer, optional
            ) for walkers_per_rank in walkers_scan
        ]
    )


walkers_selected = None # use scan above to select/set this

qmc = generate_qmcpack(
    block            = walkers_selected is None,
    identifier       = 'vmc_offload_run',
    path             = './',
    job              = qmc_job,
    input_type       = 'basic',
    system           = system,
    pseudos          = ['C.BFD.xml'],
    orbitals_h5      = './diamond.orbitals.h5',
    jastrows         = './diamond.jastrow.xml',
    corrections      = [],
    driver           = 'batched',
    delay_rank       = 4,
    det_batch        = True,
    #crowds           = , # integer, optional
    qmc              = 'vmc',
    walkers_per_rank = walkers_selected,
    warmupsteps      =  50,
    blocks           = 800,
    steps            =  10,
    substeps         =   3,
    timestep         = 0.3,
    usedrift         = True,
    )

run_project()

