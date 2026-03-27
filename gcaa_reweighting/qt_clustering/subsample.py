import mdtraj as md
import numpy as np
import sys
import os

bme_dir = os.getcwd().split("notebook")[0]
data_dir_1 = os.getcwd().split("BME-main")[0]
data_dir_2 = f"{data_dir_1}/GCAA_python_analysis"
data_dir_3 = os.getcwd().split("analysis")[0]
sys.path.append(bme_dir)

# choose two sets of experimental data like RDC, CCR, NOE or 3J and define run number
data1 = "rdcall_CCR"
data2 = "3J"

# define a folder for saving the output,
out_weights = f"weights"
out_crossval = f"crossval"

traj_file = f"{data_dir_2}/gcaa_simulations/concat_traj_nopbc.xtc"
top_file = f"{data_dir_2}/gcaa_simulations/initial_nopbc_mdtraj.pdb"
pdb_file_out = f"qt_clustering_200/md_plus_exp_subsampled.pdb"
weights = np.load(f"{out_weights}/{data1}_{data2}_weights_55.6_final.npy")
n_frames_out = 100

frames = np.random.choice(
    np.arange(0, len(weights)), size=n_frames_out, replace=True, p=weights
)
np.save("qt_clustering_200/subsampled_frames.npy", frames)
traj = md.load(traj_file, top=top_file)
traj_subsampled = traj[frames]
traj_subsampled.save_pdb(pdb_file_out)
