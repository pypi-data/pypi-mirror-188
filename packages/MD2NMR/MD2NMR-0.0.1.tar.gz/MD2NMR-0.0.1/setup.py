from setuptools import setup, find_packages

setup(
    name="MD2NMR",
    version="0.0.1",
    author="Tiejun Wei",
    description="Tools for calculating NMR relaxation observables (R1/R2/NOE/T1/T2/Tau_c) directly from MD trajectories. Initially written for calculations regarding nucleosome simulations but can be extended for other proteins/complexes.",
    url="https://github.com/DerienFe/MD2NMR",
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=["numpy == 1.23.4",
                      "pandas == 1.5.1",
                      "python == 3.10.6",
                      "scikit-learn == 1.1.3",
                      "scipy == 1.9.3",
                      "mdtraj ==1.9.7",
                      'setuptools == 65.5.0'],
)