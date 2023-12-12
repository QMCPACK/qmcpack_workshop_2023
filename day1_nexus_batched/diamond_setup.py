from nexus import settings,job
from nexus import generate_physical_system

settings(
    pseudo_dir = './pseudopotentials',
    results    = '',
    sleep      = 3,
    machine    = 'ws16',
    )


system = generate_physical_system(
    structure = './diamond.poscar',
    kgrid     = (1,1,1),
    kshift    = (0,0,0),
    C         = 4,
    )


qmc_exe = '/your/path/to/qmcpack'

qmc_job = job(cores=12,threads=4,app=qmc_exe)


