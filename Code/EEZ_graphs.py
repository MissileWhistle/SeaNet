# Here we build all the EEZ visibility graphs and the final complete graph over all zones of the Portuguese
# maritime territory.

import json
import pickle
import numpy as np
import Ray_method as ray
from graphcls import node
import matplotlib.pyplot as plt



# import data
with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\aEEZ.json", "r") as read_file:
    aEEZ = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\mEEZ.json", "r") as read_file:
    mEEZ = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\cEEZ.json", "r") as read_file:
    cEEZ = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\aObj.json", "r") as read_file:
    aObj = [np.asarray(item) for item in json.load(read_file)]

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\mObj.json", "r") as read_file:
    mObj = [np.asarray(item) for item in json.load(read_file)]

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\cObj.json", "r") as read_file:
    cObj = [np.asarray(item) for item in json.load(read_file)]

picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\aLg", 'rb')
aLg = pickle.load(picklefile)
picklefile.close()

picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\mLg", 'rb')
mLg = pickle.load(picklefile)
picklefile.close()

picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\cLg", 'rb')
cLg = pickle.load(picklefile)
picklefile.close()

picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\ECSg", 'rb')
ECSg = pickle.load(picklefile)
picklefile.close()

d=2


# cEEZ land boarder cleaning (ray method for point in region has problems in the EZZ of the continent of portugal
# because this array inadvertently defined more that a region sharing same boarder, making the ray-method not
# applicable)
cEEZ = np.vstack((cEEZ[4579:5668, :],cEEZ[4579, :]))


# possible direction from a node in ECS
dir = [[np.cos(np.pi/6+0*np.pi/3), np.sin(np.pi/6+0*np.pi/3)], [0,1],
       [-np.cos(np.pi/6+0*np.pi/3), np.sin(np.pi/6+0*np.pi/3)],
       [-np.cos(np.pi/6+0*np.pi/3), -np.sin(np.pi/6+0*np.pi/3)], [0,-1],
       [np.cos(np.pi/6+0*np.pi/3), -np.sin(np.pi/6+0*np.pi/3)]]


# graphs with nodes in ECS that boarder with EEZs (one graph for each EEZ)
aBg = []
mBg = []
cBg = []
for nod in ECSg:
    p = nod.cord
    InZonea = [None] * 6
    InZonem = [None] * 6
    InZonec = [None] * 6
    for i in range(6):
        q = [p[0] + d*dir[i][0], p[1] + d*dir[i][1]]
        InZonea[i] = ray.point_inr(aEEZ, [], q)
        InZonem[i] = ray.point_inr(mEEZ, [], q)
        InZonec[i] = ray.point_inr(cEEZ, [], q)
    if True in InZonea:
        aBg.append(nod)
    if True in InZonem:
        mBg.append(nod)
    if True in InZonec:
        cBg.append(nod)


# concatenate previous graphs with respective imported obstacle graphs. These are the graph to compute
# visibility among vertices
aVg = aBg + aLg
mVg = mBg + mLg
cVg = cBg + cLg


# List of edges in graphs. These are required for the visibility graphs computation

# Azores
aEdges = []
for nod in aVg:
    N = nod
    C = N.cord
    while N.next:
        E = [C, N.next.cord]
        if [N.next.cord, C] not in aEdges:
            aEdges.append(E)
        N = N.next

# Madeira
mEdges = []
for nod in mVg:
    N = nod
    C = N.cord
    while N.next:
        E = [C, N.next.cord]
        if [N.next.cord, C] not in mEdges:
            mEdges.append(E)
        N = N.next

# Continent
# Continent has special case where there is an additional edge that closes the continent landmass but can't
# be present in the graph for it's not a valid path for the USV (this edge is on land)
cEdges = []
for nod in cVg:
    N = nod
    C = N.cord
    while N.next:
        E = [C, N.next.cord]
        if [N.next.cord, C] not in cEdges:
            cEdges.append(E)
        N = N.next
cEdges.append([np.ndarray.tolist(cObj[0][-2]), np.ndarray.tolist(cObj[0][-1])])


# Visibility graphs
# here we choose two vertices in the corresponding graph and see if the edge connecting them is not within an
# obstacle, then we check if it doesn't intersect any other obstacle edge, if not the case then those vertices
# are "visible" and can be connected (in both ways). We also memoize the already processed pairs to avoid
# reprocessing them again (we process combinations not permutations)

# Azores
Ed = []
i = 0
for nodei in aVg:
    p = nodei.cord
    j = 0
    for nodej in aVg:
        q = nodej.cord
        Ed.append([i, j])
        if (not p == q) and ([j, i] not in Ed) and ([p, q] not in aEdges) and ([q, p] not in aEdges):
            inreg = None
            for obj in aObj:
                inreg = ray.point_inr(obj, [], [(p[0]+q[0])/2, (p[1]+q[1])/2])
                if inreg:
                    break
            if not inreg and not ray.nvisible_edge(aEdges, [p, q]):
                x = nodei
                while x.next:
                    x = x.next
                x.next = node(q)
                while nodej.next:
                    nodej = nodej.next
                nodej.next = node(p)
        j += 1
    i += 1


# Madeira
Ed = []
i = 0
for nodei in mVg:
    p = nodei.cord
    j = 0
    for nodej in mVg:
        q = nodej.cord
        Ed.append([i, j])
        if (not p == q) and ([j, i] not in Ed) and ([p, q] not in mEdges) and ([q, p] not in mEdges):
            inreg = None
            for obj in mObj:
                inreg = ray.point_inr(obj, [], [(p[0]+q[0])/2, (p[1]+q[1])/2])
                if inreg:
                    break
            if not inreg and not ray.nvisible_edge(mEdges, [p, q]):
                x = nodei
                while x.next:
                    x = x.next
                x.next = node(q)
                while nodej.next:
                    nodej = nodej.next
                nodej.next = node(p)
        j += 1
    i += 1


# Continent
Ed = []
i = 0
for nodei in cVg:
    p = nodei.cord
    j = 0
    for nodej in cVg:
        q = nodej.cord
        Ed.append([i, j])
        if (not p == q) and ([j, i] not in Ed) and ([p, q] not in cEdges) and ([q, p] not in cEdges):
            inreg = None
            for obj in cObj:
                inreg = ray.point_inr(obj, [], [(p[0]+q[0])/2, (p[1]+q[1])/2])
                if inreg:
                    break
            if (not inreg) and (not ray.nvisible_edge(cEdges, [p, q])):
                x = nodei
                while x.next:
                    x = x.next
                x.next = node(q)
                while nodej.next:
                    nodej = nodej.next
                nodej.next = node(p)
        j += 1
    i += 1


# Plot Graphs

# Azores
Edg = []
for node in aVg:
    N = node
    P = node.cord
    while N.next:
        A = [P, N.next.cord]
        Edg.append(A)
        if [N.next.cord, P] not in Edg:
            A = np.asarray(A)
            plt.plot(A[:, 0], A[:, 1], color="blue", linewidth=0.5)
        N = N.next
plt.show()

# Madeira
Edg = []
for node in mVg:
    N = node
    P = node.cord
    while N.next:
        A = [P, N.next.cord]
        Edg.append(A)
        if [N.next.cord, P] not in Edg:
            A = np.asarray(A)
            plt.plot(A[:, 0], A[:, 1], color="blue", linewidth=0.5)
        N = N.next
plt.show()

# Continent
Edg = []
for node in cVg:
    N = node
    P = node.cord
    while N.next:
        A = [P, N.next.cord]
        Edg.append(A)
        if [N.next.cord, P] not in Edg:
            A = np.asarray(A)
            plt.plot(A[:, 0], A[:, 1], color="blue", linewidth=0.5)
        N = N.next
plt.show()


# Full Portugal graph (ECS + EEZs)
PTg = ECSg + aLg + mLg + cLg

Edg = []
for node in PTg:
    N = node
    P = node.cord
    while N.next:
        A = [P, N.next.cord]
        Edg.append(A)
        if [N.next.cord, P] not in Edg:
            A = np.asarray(A)
            plt.plot(A[:, 0], A[:, 1], color="blue", linewidth=0.5)
        N = N.next
plt.show()


# Store PTg graph
picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\PTg", 'wb')
pickle.dump(PTg, picklefile)
picklefile.close()
