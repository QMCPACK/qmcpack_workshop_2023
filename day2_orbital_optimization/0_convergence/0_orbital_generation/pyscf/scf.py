from pyscf import scf

# Nexus expands this with Mole info

### generated system text ###
from pyscf import gto as gto_loc
mol = gto_loc.Mole()
mol.atom     = '''
               C    0.00000000   0.00000000   0.00000000
               C    0.00000000   0.00000000   1.24300000
               '''
mol.basis    = 'ccecpccpvqz'
mol.unit     = 'A'
mol.ecp      = 'ccecp'
mol.charge   = 0
mol.spin     = 0
mol.verbose     = 6
mol.symmetry = True
mol.build()
### end generated system text ###



mf = scf.UHF(mol)
mf.kernel()

### generated conversion text ###
from PyscfToQmcpack import savetoqmcpack
savetoqmcpack(mol,mf,'scf_lcao')
### end generated conversion text ###


