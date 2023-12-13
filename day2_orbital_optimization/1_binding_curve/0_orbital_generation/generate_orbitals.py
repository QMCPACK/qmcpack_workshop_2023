from pyscf import scf
import numpy as np
import sys
sys.path.append('/Users/aedumi/software/all_qmcpack/oo_nexus/nexus/lib/')
sys.path.append('/Users/aedumi/software/all_qmcpack/oo_nexus/src/QMCTools/')
from PyscfToQmcpack import savetoqmcpack

# Nexus expands this with Mole info
### generated system text ###
from pyscf import gto as gto_loc
mol = gto_loc.Mole()
bd = np.append(np.arange(.8,2.0,.1),np.arange(2.0,5.0,1))


with open('scf_summary.txt','w') as f:
    f.write('bond distance (a)       Energy (Ha)\n')
with open('lda_summary.txt','w') as f:
    f.write('bond distance (a)       Energy (Ha)\n')
with open('pbe_summary.txt','w') as f:
    f.write('bond distance (a)       Energy (Ha)\n')
    
    
for b in bd:
    mol.atom     = f'''
                   C    0.00000000   0.00000000   0.00000000
                   C    0.00000000   0.00000000   {b}
                   '''
    mol.basis    = 'ccecpccpvqz'
    mol.unit     = 'A'
    mol.ecp      = 'ccecp'
    mol.charge   = 0
    mol.spin     = 0
    mol.verbose     = 2
    mol.symmetry = True
    mol.build()
    ### end generated system text ###



    mf = scf.UHF(mol)
    e_scf=mf.kernel()
    with open('scf_summary.txt','a') as f:
        f.write(f'{b:17.2f} {e_scf:17.5f}\n')
    savetoqmcpack(mol,mf,f'hf_orbs/scf_lcao_bd_{b:.1f}')

        
    mf = scf.RKS(mol)
    mf.xc='lda'
    e_dft=mf.kernel()
    with open('lda_summary.txt','a') as f:
        f.write(f'{b:17.2f} {e_dft:17.5f}\n')
    savetoqmcpack(mol,mf,f'lda_orbs/lda_lcao_bd_{b:.1f}')

    mf = scf.RKS(mol)
    mf.xc='pbe'
    e_dft=mf.kernel()
    with open('pbe_summary.txt','a') as f:
        f.write(f'{b:17.2f} {e_dft:17.5f}\n')
    from PyscfToQmcpack import savetoqmcpack
    savetoqmcpack(mol,mf,f'pbe_orbs/pbe_lcao_bd_{b:.1f}')



