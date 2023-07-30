import json
import pandas as pd
import numpy as np
from sklearn import utils
import os

def trj2np(f_lattice, f_positions, f_energy, f_forces, n_atoms, n_frames, n_CO2, shuffle=True):
    # Lattice
    Lattice_init = pd.read_csv(f_lattice, sep="\s+")
    Lattice_all = Lattice_init.drop(columns=['Step', 'Time[fs]', 'Volume[Angstrom^3]'])[:n_frames].to_numpy()
    Lattice_all = Lattice_all.reshape(n_frames, 3, 3)
    # Positions and AtomTypes
    with open(f_positions) as f_read:
        Positions_all = np.array([])
        AtomTypes = []
        for I in range(n_frames):
            if I % 10000 == 0:
                print(I)
            Positions = np.array([])
            f_read.readline()
            f_read.readline()
            for i in range(n_atoms):  
                z = f_read.readline().split()
#                 if z[0] == "Mg":
#                     z[0] = "1"
#                 elif z[0] == "O":
#                     z[0] = "2"
#                 elif z[0] == "C":
#                     z[0] = "3"
#                 else:
#                     z[0] = "4"
                Positions = np.append(Positions, np.array([float(zz) for zz in z[1:]]))
                if I == 0:
                    AtomTypes.append(z[0])
            Positions_all = np.append(Positions_all, Positions)
    Positions_all = Positions_all.reshape(n_frames, n_atoms, 3)
    # AtomTypes for CO2
    for n in range(n_CO2):
        AtomTypes[-1 + 3 * n] = "CC" # "5" #
        AtomTypes[-2 + 3 * n] = "OO" #"6" #
        AtomTypes[-3 + 3 * n] = "OO" #"6" #
    # Energy
    Energy_init = pd.read_csv(f_energy, sep="\s+")
    Energy_all = Energy_init["Pot.[a.u.]"].to_numpy()[:n_frames]
    Energy_all *= 27.211
    # Forces
    with open(f_forces) as f_read:
        Forces_all = np.array([])
        for I in range(n_frames):
            if I % 10000 == 0:
                print(I)
            Forces = np.array([])
            f_read.readline()
            f_read.readline()
            for i in range(n_atoms):  
                z = f_read.readline().split()[1:]

                Forces = np.append(Forces, np.array([float(zz) for zz in z]))
            Forces_all = np.append(Forces_all, Forces)
    Forces_all = Forces_all.reshape(n_frames, n_atoms, 3)
    Forces_all *= 51.42
    if shuffle:
        Lattice_all, Positions_all, Energy_all, Forces_all = utils.shuffle(Lattice_all, Positions_all, Energy_all, Forces_all)
    return Lattice_all, Positions_all, Energy_all, Forces_all, AtomTypes