""" Functions for calculating Root Means Sqaured Error of experimental and calculated data"""

import numpy as np
import barnaba as bb


def calc_chi_ensemble(exp, calc, sample_weights, noe=False):
    calc_avg = np.sum(calc * sample_weights[:, np.newaxis], axis=0)
    if noe == True:
        calc_avg = np.power(
            np.average(np.power(calc, -6), weights=sample_weights, axis=0), -1.0 / 6
        )
    diff = calc_avg - exp[:, 0]

    return np.average((diff / exp[:, 1]) ** 2)


def calc_chi_bundle(exp, calc, noe=False):
    calc_avg = calc
    if noe == True:
        calc_avg = calc
    diff = calc_avg - exp[:, 0]

    return np.average((diff / exp[:, 1]) ** 2, axis=-1)


def calc_RMSE_ensemble(exp, calc, sample_weights, noe=False):
    calc_avg = np.sum(calc * sample_weights[:, np.newaxis], axis=0)
    if noe == True:
        calc_avg = np.power(
            np.average(np.power(calc, -6), weights=sample_weights, axis=0), -1.0 / 6
        )
    # test of modification
    if len(exp) > 2:
        diff = calc_avg - exp[:, 0]
    else:
        diff = calc_avg - exp
    # end of modification
    #diff = calc_avg - exp[:, 0]

    return np.sqrt(np.average(diff**2))


def calc_RMSE_bundle(exp, calc):
    diff = calc - exp[:, 0]
    return np.sqrt(np.average(diff**2, axis=-1))


def calc_RMSRE_ensemble(exp, calc, sample_weights, noe=False):
    calc_avg = np.sum(calc * sample_weights[:, np.newaxis], axis=0)
    if noe == True:
        calc_avg = np.power(
            np.average(np.power(calc, -6), weights=sample_weights, axis=0), -1.0 / 6
        )
    rel_diff = (calc_avg - exp[:, 0]) / exp[:, 0]

    return np.sqrt(np.average(rel_diff**2))


def calc_RMSRE_bundle(exp, calc):
    rel_diff = (calc - exp[:, 0]) / exp[:, 0]
    return np.sqrt(np.average(rel_diff**2, axis=-1))


def get_angles_bundle(
    bundle_pdb,
    angles_list,
    res_list=["C_5_0", "G_6_0", "C_7_0", "A_8_0", "A_9_0", "G_10_0"],
):
    angles_, res_ = bb.backbone_angles(
        bundle_pdb, residues=res_list, angles=angles_list
    )
    res_ = [i.split("_")[0] + i.split("_")[1] for i in res_]
    print(angles_.shape)
    #     aa_ = np.copy(angles_)
    #     aa_ *= 180.0/np.pi

    return angles_
