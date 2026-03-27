#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Modified for use as module
"""
.. note ::

  | **Author      :** Roy Gonzalez Aleman
  | **Contact     :** [roy_gonzalez@fq.uh.cu, roy.gonzalez.aleman@gmail.com]
"""
import sys
import argparse
import numpy as np
import numpy.ma as ma
import pickle as cPickle
import bz2
import mdtraj as md

# =============================================================================
# Preprocessing
# =============================================================================


# Calculates Matrix from file
def load_matrix_from_traj(
    traj_file,
    top_file=None,
    selection="all",
    first_frame=0,
    last_frame=-1,
    frame_stride=1,
):
    # ---- Load trajectory --------------------------------------------------------

    if top_file != None:
        trajectory = md.load(traj_file)
    else:
        trajectory = md.load(traj_file, top=top_file)

    # Reduce RAM consumption by loading selected atoms only -------------------
    if selection != "all":
        try:
            sel_indx = trajectory.topology.select(selection)
        except ValueError:
            print("Specified selection is invalid")
            sys.exit()
        if sel_indx.size == 0:
            print("Specified selection in your system corresponds to no atoms")
            sys.exit()
        trajectory = trajectory.atom_slice(sel_indx)[
            first_frame:last_frame:frame_stride
        ]
    else:
        trajectory = trajectory[first_frame:last_frame:frame_stride]

    # Center coordinates of loaded trajectory ---------------------------------
    trajectory.center_coordinates()

    N = trajectory.n_frames

    # ---- Calculate matrix pairwise distances ------------------------------------
    matrix = np.ndarray((N, N), dtype=np.float16)
    for i in range(N):
        rmsd_ = md.rmsd(trajectory, trajectory, i, precentered=True) * 10
        matrix[i] = rmsd_
    print(">>> Calculation of the RMSD matrix completed <<<")
    return matrix


#  Returns matrix from file
def load_matrix(matrix_file):
    # ---- ADDED MANUALLY: Load precomputed distance matrix (eRMSD) ---------------
    def load_bz2_pkl(inp):
        data = bz2.BZ2File(inp, "rb")
        data = cPickle.load(data)
        return data

    print("Precalculated distance matrix provided.\nLoading matrix...")
    matrix = load_bz2_pkl(matrix_file)
    return matrix


# clusters using given RMSD matrix
def qt_cluster(matrix, cutoff=1, minsize=2):

    N = matrix.shape[0]
    print(f"Matrix Size {N}")

    # ---- Delete unuseful values from matrix (diagonal &  x>threshold) -----------
    matrix[matrix > cutoff] = np.inf
    matrix[matrix == 0] = np.inf
    degrees = (matrix < np.inf).sum(axis=0)

    # =============================================================================
    # QT algotithm
    # =============================================================================

    clusters_arr = np.ndarray(N, dtype=np.int64)
    clusters_arr.fill(-1)
    max_precluster = []
    max_node = None
    ncluster = 0
    while True:
        # This while executes for every cluster in trajectory ---------------------
        len_precluster = 0
        while True:
            # This while executes for every potential cluster analyzed ------------
            biggest_node = degrees.argmax()
            precluster = []
            precluster.append(biggest_node)
            candidates = np.where(matrix[biggest_node] < np.inf)[0]
            next_ = biggest_node
            distances = matrix[next_][candidates]
            while True:
                # This while executes for every node of a potential cluster -------
                next_ = candidates[distances.argmin()]
                precluster.append(next_)
                post_distances = matrix[next_][candidates]
                mask = post_distances > distances
                distances[mask] = post_distances[mask]
                if (distances == np.inf).all():
                    break
            degrees[biggest_node] = 0
            # This section saves the maximum cluster found so far -----------------
            if len(precluster) > len_precluster:
                len_precluster = len(precluster)
                max_precluster = precluster
                max_node = biggest_node
                degrees = ma.masked_less(degrees, len_precluster)
            if not degrees.max():
                break
        # General break if minsize is reached -------------------------------------
        if len(max_precluster) < minsize:
            break

        # ---- Store cluster frames -----------------------------------------------
        clusters_arr[max_precluster] = ncluster
        ncluster += 1
        print(
            ">>> Cluster # {} found with {} frames at center {} <<<".format(
                ncluster, len_precluster, max_node
            )
        )

        # ---- Update matrix & degrees (discard found clusters) -------------------
        matrix[max_precluster, :] = np.inf
        matrix[:, max_precluster] = np.inf

        degrees = (matrix < np.inf).sum(axis=0)
        if (degrees == 0).all():
            break

    return clusters_arr
    # ---- Write clustering results to disk ---------------------------------------

    # simple format
    # np.savetxt(f"QT_Clusters.txt", clusters_arr, fmt="%i")

    # # NMRcluster format. VMD interface
    # with open("QT_Visualization.log", "wt") as clq:
    #     for numcluster in np.unique(clusters_arr):
    #         clq.write("{}:\n".format(numcluster))
    #         members = " ".join(
    #             [str(x) for x in np.where(clusters_arr == numcluster)[0]]
    #         )
    #         clq.write("Members: " + members + "\n\n")
