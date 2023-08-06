# MD2NMR. Written by TW on Jan 2023, Queen's University Panchenko's Lab
Tools for calculating NMR relaxation observables (R1/R2/NOE/T1/T2/Tau_c) directly from MD trajectories. Initially written for calculations regarding nucleosome simulations but can be extended for other proteins/complexes. This software is subject to MIT license, with some functions imported from other repo, as noted individually in script comment section.

Dependencies:
The required packages are listed in 'requirements.txt'.
To create a new environment using anaconda: (replace myenv as approperiate)
conda create --name myenv --file requirements.txt

Usage:
Before usage one should first check the config.py and make sure the hyperparameters are suitable for the calculation.

for single file mode (basic usage):
python main.py -t $topology_file$ -y $trajectory_file$

for batch mode:
python main.py --batch=True

Note that the batch mode will generate results for all traj/topo under working directory with satisfied prefix.
