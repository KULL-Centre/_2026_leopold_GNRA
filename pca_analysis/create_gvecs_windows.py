import sys
import glob
import barnaba as bb
import numpy as np
import barnaba.cluster as cc
import pickle
import os

fdir = os.listdir(sys.argv[1])
flist = []
for f in fdir:
    f2 = f"{sys.argv[1]}/"+f
    flist.append(f2)

#flist = sys.argv[1:]
if(len(flist)==0):
    print("No files")
    exit()
print(flist)

# calculate G-VECTORS  for all files
gvecs = []
structure_names = []
n_frames = 0
for f in flist:
    gvec,seq = bb.dump_gvec(f)
    if len(seq)==8:
        gvecs.extend(gvec)
        structure_names.append(f)
        n_frames += 1
    else:
        print('Skipping')

gvecs = np.array(gvecs)
print(gvecs.shape)
gvecs = gvecs.reshape(n_frames,-1)
print(gvecs.shape)

# calculate PCA
v,w = cc.pca(gvecs,nevecs=3)
print("# Cumulative explained variance of component: 1=%5.1f 2:=%5.1f 3=%5.1f" % (v[0]*100,v[1]*100,v[2]*100))

# Open a file and use dump()
with open('pca_results.pkl', 'wb') as file:

    # A new file will be created
    pickle.dump({'v':v, 'w':w, 'gvecs':gvecs, 'names':structure_names}, file)



