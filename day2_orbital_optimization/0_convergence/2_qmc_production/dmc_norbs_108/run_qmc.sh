#!/usr/bin/env bash
set -o pipefail
set -o errexit
set -o nounset

# Number of threads per MPI task
export OMP_NUM_THREADS=8

# qmcpack executable
export QMCPACK="${HOME}/qmcpack/3.17.1/build-production-real/bin/qmcpack"

# Get the ecp and orbs
if [[ ! -e "C.ccECP.xml" ]]; then
    ln -s "../../../C.ccECP.xml" .
fi
if [[ ! -e "c4q.orbs.h5" ]]; then
    ln -s "../../0_orbital_generation/blessed_output/c4q.orbs.h5" .
fi
if [[ ! -e "opt.s048.vp.h5" ]]; then
    ln -s "../../1_qmc_opt/norbs_108/opt.s048.vp.h5" .
fi

# Run the problem
${QMCPACK} dmc.in.xml > dmc.out

exit 0
