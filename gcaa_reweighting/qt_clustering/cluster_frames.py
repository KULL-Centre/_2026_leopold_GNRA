import mdtraj as md
import numpy as np
import os

data_dir_1 = os.getcwd().split("BME-main")[0]
data_dir_2 = f"{data_dir_1}/GCAA_python_analysis"
traj_file = f'{data_dir_2}/gcaa_simulations/concat_traj_nopbc.xtc'
top_file = f'{data_dir_2}/gcaa_simulations/initial_nopbc_mdtraj.pdb'
frames = np.load("qt_clustering_top/subsampled_frames.npy")
cluster_ids = [[ 5,  7, 14, 16, 19, 33, 43, 51, 60, 63, 66, 83],
               [ 0,  2,  3, 10, 12, 28, 29, 32, 46, 58],
               [ 8, 15, 23, 25, 67, 79, 80, 81],
               [ 9, 24, 34, 72, 77, 97],
               [ 4, 45, 53, 62, 78],
               [59, 69, 70, 74, 82],
               [37, 50, 71, 86, 98],
               [ 1,  6, 11, 13, 17, 18, 20, 21, 22, 26, 27, 30, 31, 35, 36, 38, 39,
        40, 41, 42, 44, 47, 48, 49, 52, 54, 55, 56, 57, 61, 64, 65, 68, 73,
        75, 76, 84, 85, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 99]
]
traj = md.load(traj_file, top=top_file)

for i in range(len(cluster_ids)):
   id = cluster_ids[i]
   pdb_file_out = f'qt_clustering_top/Cluster_{i}_size_{len(id)}.pdb'
   cluster = traj[frames[id]]
   cluster.save_pdb(pdb_file_out)


   