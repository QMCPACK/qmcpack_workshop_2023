#!/usr/bin/env python3

# Morse 3p:
#
#   3-parameter problem in the abstract parameter space
#
#   This example simulates characteristics of the surrogate hessian parallel 
#   line-search method using a lightweight artificial Morse PES.
#
#   This example is light enough to operate interactively on a laptop.



base_dir = 'morse_3p/'

#===========================#
# Representation of the PES #
#===========================#
#   Artificial/specific to this example.
#   In an ab-initio calculation setting, calls to this function
#   are replaced by DFT and QMC total energy calculations.
#
#   This example: three coupled 1D Morse oscillators  
#   c:     coupling constant of parameters through auxiliary morse potentials
#   d:     eqm displacements
#   sigma: added stochastic noise

print('\n'+70*'=')
print('Define PES (only for non-ab-initio)')
print(70*'=')

def pes(structure, sigma = None, c = 1.0, d = 0.0):
    from numpy import array, exp, random
    morse = lambda p,r: p[2]*((1-exp(-(r-p[0])/p[1]))**2-1)+p[3]
    p0, p1, p2 = structure.params
    # define Morse potentials for each individual parameter
    # when c = 0, these are the solutions for p_eqm and the Hessian
    #  (eqm value, stiffness, well depth, E_inf)
    m0 = array([1.0 + d, 3.0, 0.5, 0.0])
    m1 = array([2.0 + d, 2.0, 0.5, 0.0])
    m2 = array([3.0 + d, 1.0, 0.5, 0.0])
    E = 0.0
    E += morse(m0, p0)
    E += morse(m1, p1)
    E += morse(m2, p2)
    # non-zero (c > 0) couplings between the parameters set off the equilibrium point
    m01 = array([4.0, 6.0, 0.5, 0.0])
    m02 = array([5.0, 5.0, 0.5, 0.0])
    m12 = array([6.0, 4.0, 0.5, 0.0])
    E += c * morse(m01, p0 + p1)
    E += c * morse(m02, p0 + p2)
    E += c * morse(m12, p1 + p2)
    if not sigma is None:
        E += sigma * random.randn(1)[0]  # add random noise
    #end if
    return E, sigma
#end def



#======================================================================#
# Obtain surrogate hessian and relaxed parameters of the surrogate PES #
#======================================================================#
#   In an ab-initio calculation, these steps are performed with DFT.
#   In this model setting we define a surrogate PES.

print('\n'+70*'=')
print('Surrogate PES: obtain relaxed geometry and surrogate Hessian ("DFT")')
print(70*'=')

# Parameters defining the surrogate PES
c_surr = 1.0  # define the surrogate PES with c = 1.0
d_surr = 0.0  # and d = 0.0

# Initial guess structure
from surrogate_classes import ParameterSet
p_init = ParameterSet([1.0, 2.0, 3.0])

# Find the optimal parameters (relaxed strucuture) of the surrogate PES
#   (in ab initio: this step would be perfomed with DFT structural relaxation)
from scipy.optimize import minimize
def pes_min(params):
    return pes(ParameterSet(params), c = c_surr, d = d_surr)[0]
#end def
res = minimize(pes_min, p_init.params) # "DFT" structural relaxation
p_relax = ParameterSet(res.x)
print('Minimum-energy parameters (surrogate):')
print(p_relax.params)

# Obtain the surrogate Hessian via finite differences
#  (in ab initio: this step would be perfomed with DFT-SCF calculations)
from surrogate_macros import compute_fdiff_hessian
hessian = compute_fdiff_hessian(structure = p_relax, func = pes, mode = 'pes')
print('\nSurrogate Hessian:')
print(hessian)



#=======================================================================#
# Tune parallel line search approach based on the surrogate PES/Hessian #
#=======================================================================#
#  Based on user-provided parameter tolerances, determine line search 
#  extents along conjugate directions and target stochastic uncertainties 
#  on the energy values computed along each conjugate direction.
#
#  This step aims to minimize statistical cost in the following DMC
#  line search, while remaining within user defined parameter tolerances.
#
#  In the ab-initio setting, this step involves no QMC calculations.

print('\n'+70*'=')
print('Tune/design parallel line search process (minimize cost)')
print(70*'=')

# User-specified accuracy tolerances on structural parameters
#                   p1    p2    p3
param_tolerances = [0.01, 0.02, 0.03]

# Create a surrogate ParallelLineSearch object
from surrogate_macros import generate_surrogate
surrogate = generate_surrogate(
    path        = base_dir + 'surrogate',
    fname       = 'surrogate.p', 
    structure   = p_relax,
    hessian     = hessian,
    pes_func    = pes,
    pes_args    = {'c': c_surr, 'd': d_surr},
    mode        = 'pes',
    window_frac = 0.5,  # max displacement relative to PES stiffness of each direction
    M           = 25,   # number of points to evaluate surrogate PES along directions
    )

# Optimize the line-search to tolerances via correlated sampling
if not surrogate.optimized:
    surrogate.optimize(
        epsilon_p  = param_tolerances,  # parameter tolerances
        fit_kind   = 'pf3',
        noise_frac = 0.01,  # (initial) maximum resampled noise relative to the maximum window
        M          = 7,
        N          = 500,  #  correlated resampling of the error
        )
    surrogate.write_to_disk('surrogate.p')
#end if


#==============================#
# Perform parallel line search #
#==============================#
#  The actual parallel line search along the surrogate conjugate directions.
#
#  In the ab-initio setting, this step contains all QMC calculations.  

print('\n'+70*'=')
print('Perform parallel line search ("DMC")')
print(70*'=')

# (non-ab-initio only) define the actual/target/"DMC" PES
c_actual = 1.0
d_actual = 0.3

# Run line-search iteration with the alternative PES 
from surrogate_classes import LineSearchIteration
lsi = LineSearchIteration(
    path      = base_dir + 'lsi',
    surrogate = surrogate,
    pes_func  = pes,
    pes_args  = {'c': c_actual, 'd': d_actual},
    mode      = 'pes',
    )

# Perform L parallel iterations of line search
L = 4
for i in range(L):
    lsi.propagate(i, add_sigma = True)
#end for


from surrogate_macros import linesearch_diagnostics
linesearch_diagnostics(lsi)




# Compute reference minimum
print('\n'+70*'=')
print('Minimum-energy parameters (actual/reference):')
print(70*'=')
def pes_min_actual(params):
    return pes(ParameterSet(params), c = c_actual, d = d_actual)[0]
#end def
res = minimize(pes_min_actual, p_init.params)
p_relax = ParameterSet(res.x)
print(p_relax.params)
print('param tolerances:',param_tolerances)



import matplotlib.pyplot as plt
plt.show()


