#!/usr/bin/env python
# calculate RDCs using Pales. A lof of hardcoded stuff, so make sure to check everything!

import mdtraj as md
import subprocess
import os
import pandas as pd
import sys
import platform

# i = int(sys.argv[1])
# stride = int(sys.argv[2])


# calculate RDCs using Pales.
def run_calc(sim_folder, exp_folder):
    folder = sim_folder
    exp = exp_folder
    pales = "bin/pales-win" if platform.system() == "Windows" else "bin/pales-linux"

    # print(f'Calculating RDCs for gcaa_{i}. Stride {stride}.')

    di_df = pd.DataFrame()
    d_df = pd.DataFrame()

    traj_file = f"{folder}/concat_traj_nopbc.xtc"
    top_file = f"{folder}/initial_nopbc_mdtraj.pdb"
    traj = md.load_xtc(traj_file, top=top_file, stride=1)  # stride=stride
    for k, f in enumerate(traj):
        pdb_tmp = f"{folder}/frame_{k}.pdb"
        outd_tmp = f"{folder}/rdc_tmp_pf1_{k}.tbl"
        outd_tmp_2 = f"{outd_tmp}_red"
        # Save tmp pdb for current frame:
        f.save_pdb(
            pdb_tmp,
        )
        # Calculate RDCs:
        process = f"{pales} -inD {exp}/exp_rdc_pales.tab -pdb {pdb_tmp} -outD {outd_tmp} -pf1 -H -wv 0.05"
        p = subprocess.Popen(
            process,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        p.wait()
        os.remove(pdb_tmp)
        # Remove all uneccesary lines:
        process = f"sed 0,/^FORMAT/d {outd_tmp} > {outd_tmp_2}"
        p = subprocess.Popen(
            process,
            shell=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True,
        )
        p.wait()
        # Read outfile:
        df_tmp = pd.read_csv(
            outd_tmp_2,
            delim_whitespace=True,
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
        )
        names = [
            f"{r[1]['RESNAME_I'][0]}{r[1]['RESID_I']}_{r[1]['ATOMNAME_I']}-{r[1]['ATOMNAME_J']}"
            for r in df_tmp.iterrows()
        ]
        di_tmp = [float(v) for v in df_tmp["DI"]]
        d_tmp = [float(v) for v in df_tmp["D"]]
        # Add Di values to one df:
        dic_di = dict(zip(names, di_tmp))
        di_intermediate_df = pd.DataFrame.from_dict(
            dic_di, orient="index", columns=[f"{k}"]
        )
        di_df = pd.concat([di_df, di_intermediate_df], axis=1)
        # Add D valuesto another df:
        dic_d = dict(zip(names, d_tmp))
        d_intermediate_df = pd.DataFrame.from_dict(
            dic_d, orient="index", columns=[f"{k}"]
        )
        d_df = pd.concat([d_df, d_intermediate_df], axis=1)
        os.remove(outd_tmp)
        os.remove(outd_tmp_2)
    return di_df, d_df


if __name__ == "__main__":
    di_df, d_df = run_calc(sys.argv[1], sys.argv[2])
    di_df.to_pickle(f"{sys.argv[1]}/di_df_pf1.pkl")
    d_df.to_pickle(f"{sys.argv[1]}/d_df_pf1.pkl")
    print(di_df)
    print(d_df)
    print(f"{d_df.shape[1]} Di & D for {d_df.shape[0]} frames saved as pickle.")
