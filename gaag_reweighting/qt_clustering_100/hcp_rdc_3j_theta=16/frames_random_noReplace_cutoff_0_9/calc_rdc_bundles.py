#!/usr/bin/python
# calculate RDCs using Pales. A lof of hardcoded stuff, so make sure to check everything! Also, test with a single frame to make sure this works with your version of PALES.

import mdtraj as md
import subprocess
import os
import pandas as pd
import sys

#### Modify this accordingly ####
i = str(sys.argv[1])  # bundle name
#i = "cluster_0"    #for testing with a single bundle
#inout_dir = "qt_clustering_100/hcp_rdc_3j_theta=16/frames_random_cutoff_0_9"  # directory to the bundle pdb structures
inout_dir = str(sys.argv[2])
pales_exec = f"pales-win" #put the exe file in the home folder, not the 
exp_rdc = f"exp_data/exp_rdc_pales.tab"
#################################

di_df = pd.DataFrame()
d_df = pd.DataFrame()
traj_f = f"{inout_dir}/{i}.pdb"
top_f = f"{inout_dir}/{i}.pdb"
traj = md.load_pdb(traj_f)


for k, f in enumerate(traj):
    pdb_tmp = f"{inout_dir}/frame_{k}.pdb"
    out_dir_tmp = f"{inout_dir}/rdc_tmp_pf1_{k}.tbl"
    # Save tmp pdb for current frame:
    f.save_pdb(pdb_tmp)
    # Calculate RDCs:
    #    process = f'{pales_exec} -inD {exp_rdc} -pdb {pdb_tmp} -bestFit -outD {out_dir_tmp} -wv 50 -H' # fitting the alignment tensor
    process = f"{pales_exec} -inD {exp_rdc} -pdb {pdb_tmp} -outD {out_dir_tmp} -pf1 -H -wv 0.05"  # predciting the alignment tensor
    p = subprocess.Popen(
        process,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
    )
    p.wait()
    os.remove(pdb_tmp)
    #    # Remove all unneccesary lines:
    #    process = f"sed -i '0,/^FORMAT/d' {out_dir_tmp}"
    #    p       = subprocess.Popen(process, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
    #    p.wait()
    # Read outfile:
    df_tmp = pd.read_csv(
        out_dir_tmp,
        delim_whitespace=True,
        skiprows=81,
        names=[
            "RESID_I",
            "RESNAME_I",
            "ATOMNAME_I",
            "RESID_J",
            "RESNAME_J",
            "ATOMNAME_J",
            "DI",
            "D_OBS",
            "D",
            "D_DIFF",
            "DD",
            "W",
        ],
    )  # skiprows=81,
    names = [
        f"{r[1]['RESNAME_I'][0]}{r[1]['RESID_I']}_{r[1]['ATOMNAME_I']}-{r[1]['ATOMNAME_J']}"
        for r in df_tmp.iterrows()
    ]
    di_tmp = [float(v) for v in df_tmp["DI"]]
    d_tmp = [float(v) for v in df_tmp["D"]]

    dic_di = dict(zip(names, di_tmp))
    di_intermediate_df = pd.DataFrame.from_dict(
        dic_di, orient="index", columns=[f"{k}"]
    )
    di_df = pd.concat([di_df, di_intermediate_df], axis=1)
    dic_d = dict(zip(names, d_tmp))
    d_intermediate_df = pd.DataFrame.from_dict(dic_d, orient="index", columns=[f"{k}"])
    d_df = pd.concat([d_df, d_intermediate_df], axis=1)
    os.remove(out_dir_tmp)

di_df = di_df.T
d_df = d_df.T

"""    # Add Di values to one df:
    di_df = di_df.append(dict(zip(names,di_tmp)), ignore_index=True)    # curse the omnissiah for deletion of pd.DataFrame.append, so this humble serveant is forced to commit techheresy by coding like a noob 
    # Add D values to another df:
    d_df = d_df.append(dict(zip(names,d_tmp)), ignore_index=True)
"""

di_df.to_pickle(f"{inout_dir}/nmrbundle_{i}_di_df_pf1.pkl")
d_df.to_pickle(f"{inout_dir}/nmrbundle_{i}_d_df_pf1.pkl")
print(f"{d_df.shape[1]} Di & D for {d_df.shape[0]} frames saved as pickle.")
