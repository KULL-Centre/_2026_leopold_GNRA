import numpy as np

### HELPER FUNCTIONS TO CALCULATE NOE DISTANCES ###

# helper functions, subsititute strings. This is because the name of hydrogens is a mess
# alt = {"H2'":"1H2'","H5''":"2H5'","H5'":"1H5'","HO2'":"2HO'","H5\"":"2H5'","H5'2":"2H5'","H5'1":"1H5'"}
alt = {"H2'": "H2'1", "H5''": "H5'2", "H5'": "H5'1", "HO2'": "HO'2"}


def sub(ss):
    at = "H" + ss.split("H")[1]
    if at in alt:
        at = alt[at]
    return ss.split("H")[0] + at


# read experimental datafile and returns a list of labels and experimental values
def read_exp(f_exp):
    labels = []
    vals = []
    with open(f_exp) as fh:
        for line in fh:
            if "#" not in line:
                r1 = line.split()[0].split("-")[0]
                print(r1)
                r2 = line.split()[0].split("-")[1]
                print(r2)
                v1 = np.sort([r1, r2])
                print(v1)
                qq = v1[0] + "/" + v1[1]

                if qq in labels:
                    print("# DUPLICATE. Skipping data.."),
                    print(qq, vals[labels.index(qq)], line),
                else:
                    vals.append([float(line.split()[1]), float(line.split()[2])])
                    labels.append(qq)
    return labels, vals


# get labels from df column (Assignment)
def get_labels(df, col):
    labels = []
    for asm in df.iloc[:, col]:
        r1 = asm.split()[0].split("-")[0]
        r2 = asm.split()[0].split("-")[1]
        v1 = np.sort([r1, r2])
        qq = v1[0] + "/" + v1[1]
        labels.append(qq)
    return labels


# find indeces in topology corresponding to labels in experimental datafile
def get_idxs(labels, top):

    atoms = []
    for atom in top.atoms:
        aa = str(atom).split("-")[1]
        if aa in alt:
            aa = alt[aa]
        # print((str(atom).split("-")[0], aa))
        atoms.append("%s%s" % (str(atom).split("-")[0], aa))
    pairs = []
    for el in labels:
        ss = el.split("/")
        at1 = sub(ss[0])
        at2 = sub(ss[1])
        if at1 in atoms and at2 in atoms:
            pairs.append([atoms.index(at1), atoms.index(at2)])
        else:
            print("# Warning: Either %s or %s are missing" % (at1, at2))
            return 0
    if len(pairs) != len(labels):
        print("# Found only %d pairs out of %d" % (len(pairs), len(labels)))
    return np.array(pairs)


def group_by_heading(some_source):
    buffer = []
    for line in some_source:
        if line.startswith(" ASSI"):
            if buffer:
                yield buffer
            buffer = [line.strip().strip(")")]
        else:
            buffer.append(line.strip().strip(")"))
    yield buffer
