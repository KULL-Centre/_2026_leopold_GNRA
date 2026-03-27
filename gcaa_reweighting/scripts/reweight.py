import os
import numpy as np

# add parent folder to import bme scripts
import sys

sys.path.append("..")

import BME

import matplotlib as mpl

mpl.rcParams["hatch.linewidth"] = 5


BME_FOLDER = "../bme_reweight"

import glob
import shutil


class Reweighter:
    def __init__(self, tag, datatags):
        self.rew = BME.Reweight(tag)
        self.tag = tag

        # load the experimental and calculated datasets
        for datatag in datatags:
            self.rew.load(
                f"{BME_FOLDER}/exp_{datatag['tag']}.dat",
                f"{BME_FOLDER}/calc_{datatag['tag']}.dat",
                fit=datatag["fit"],
            )

    def move_logs(self):
        log_dir = f"{BME_FOLDER}/crossvals/crossval_{self.tag}/logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        for file in glob.glob(f"crossval_{self.tag}*.log"):
            shutil.copy(file, log_dir)

    def reweight(self):
        print(f"Starting to reweight #{self.tag}")
        self.thetas = np.geomspace(
            0.2, 20000, 30
        )  # Start: 0.2 (change if calculation fails at lower range) Stop: 20000, num: 30
        self.rew.theta_scan(thetas=self.thetas, nfold=5)
        return self.thetas

    def fit_and_save(self):
        print("Fitting")
        chi2 = []
        phis = []
        weights = []

        for theta in self.thetas:
            chi2_before, chi2_after, phi = self.rew.fit(
                theta=theta
            )  # What does fit do?
            phis.append(phi)
            chi2.append(chi2_after / chi2_before)
            w_0 = self.rew.get_w0()
            w_new = self.rew.get_weights()
            weights.append(w_new)
        out_dir = f"{BME_FOLDER}/crossvals/crossval_{self.tag}"
        print("Saving new weights at {outdir}")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        else:
            print("For this data a result directory already exists, overwriting...")
        np.save(f"{out_dir}/chi2_results.npy", chi2)
        np.save(f"{out_dir}/phi_results.npy", phis)
        np.save(f"{out_dir}/weights_results.npy", weights)


# Tag corresponds to exp and calc file
dt = {
    "ccr": {"tag": "ccr_loop_bme", "fit": "no"},
    "rdc": {"tag": "rdc_bme", "fit": "scale"},
    "j3": {"tag": "j3_bme", "fit": "no"},
    "noe": {"tag": "noe_loop_bme", "fit": "no"},
}

combinations = [
    # ["ccr", "rdc", "j3"],
    ["noe", "rdc", "j3"],
    ["ccr", "noe", "j3"],
    ["ccr", "rdc", "noe"],
]

for c in combinations:
    tag = "_".join(c)
    print(f"Looking at combination: {tag}")
    r = Reweighter(tag, [dt[typ] for typ in c])
    r.reweight()
    r.fit_and_save()
    r.move_logs()
