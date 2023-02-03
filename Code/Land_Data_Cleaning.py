# this script redefines the coordinates of land masses, making a new boarder for these obstacles
# of a simpler shape and away from land, so that this boarder can be traversed by the USV without hitting land.
# This also greatly reduces the number of vertices\coordinates required to define these land masses. Attention
# was pain to assure that vertices dedicated to ports in several land masses are present, so that the USV can
# navigate to cole proximity of a port to then enter it (using other navigation systems). Once this is done we
# convert this information into graphs. At the end we store all data, either in a json file or pickle file.

import json
import pickle
from graphcls import node
import numpy as np
import matplotlib.pyplot as plt



# Import land masses data
with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\Mad.json", "r") as read_file:
    Mad = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\Azo.json", "r") as read_file:
    Azo = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\cEEZ.json", "r") as read_file:
    cEEZ = np.asarray(json.load(read_file))


# Redefine each land mass ans store in an "object" list (by zone)

# Azores

A1 = [[-31.1462, -31.1274, -31.1107, -31.0704, -31.0692, -31.1462], [39.739, 39.659, 39.6700, 39.675, 39.743, 39.739]]
# A1[2] is port

A2 = [[-31.2228, -31.2959, -31.2734, -31.1650, -31.1650, -31.1335, -31.1077, -31.1435, -31.2228],
      [39.5599, 39.4823, 39.3532, 39.3612, 39.3793, 39.3888, 39.4729, 39.5317, 39.5599]]
# A2[4] is port

A3 = [[-28.0374, -28.0945, -28.0417, -27.9228, -27.9369, -27.9646, -27.9864, -28.0374],
      [39.1205, 39.0653, 39.0070, 38.9948, 39.0381, 39.0530, 39.1031, 39.1205]]
# A3[5] is port

A4 = [[-27.96, -27.95105, -27.94857, -27.95371, -27.96],
      [39.05839, 39.0625, 39.0588, 39.0498, 39.05839]]
# A4 has no port

A5 = [[-27.4266, -27.3356, -27.0258, -27.0437, -27.0180, -27.0860, -27.3306, -27.4266],
      [38.7627, 38.6048, 38.6184, 38.7242, 38.7520, 38.8261, 38.8380, 38.7627]]
# A5[3] is port

A6 = [[-28.3637, -28.2432, -28.2033, -28.1962, -27.7903, -27.6969, -28.0132, -28.3340, -28.3637],
      [38.7429, 38.6664, 38.6730, 38.6486, 38.5101, 38.5602, 38.7151, 38.7877, 38.7429]]
# A6[2] is port

A7 = [[-28.8567, -28.7774, -28.6033, -28.6169, -28.5918, -28.5789, -28.7199, -28.8567],
      [38.6062, 38.5015, 38.5047, 38.5369, 38.5425, 38.6133, 38.6716, 38.6062]]
# A7[3] is port

A8 = [[-28.5613, -28.5513, -28.2199, -27.9859, -28.0432, -28.2663, -28.315, -28.316, -28.3993, -28.5204, -28.5613],
      [38.544, 38.435, 38.362, 38.398, 38.472, 38.534, 38.5291, 38.5539, 38.585, 38.575, 38.544]]
# A8[6] is port

A9 = [[-25.895, -25.692, -25.656, -25.506, -25.113, -25.120, -25.814, -25.895],
      [37.843, 37.710, 37.733, 37.679, 37.713, 37.899, 37.952, 37.843]]
# A9[2] is port

A10 = [[-24.78346,-24.78311, -24.77806, -24.77928, -24.78346],
       [37.27785, 37.26727, 37.27021, 37.27852, 37.27785]]
# A10 has no port

A11 = [[-25.2131, -25.1776, -25.1475, -25.1404, -25.0727, -24.9924, -24.9984, -25.0535, -25.2131],
       [37.0129, 36.9294, 36.9405, 36.9317, 36.9156, 36.9201, 36.9797, 37.0383, 37.0129]]
# A11[2] is port

aObj = [np.ndarray.tolist(np.asarray(A1).T), np.ndarray.tolist(np.asarray(A2).T),
        np.ndarray.tolist(np.asarray(A3).T), np.ndarray.tolist(np.asarray(A4).T),
        np.ndarray.tolist(np.asarray(A5).T), np.ndarray.tolist(np.asarray(A6).T),
        np.ndarray.tolist(np.asarray(A7).T), np.ndarray.tolist(np.asarray(A8).T),
        np.ndarray.tolist(np.asarray(A9).T), np.ndarray.tolist(np.asarray(A10).T),
        np.ndarray.tolist(np.asarray(A11).T)]

plt.plot(Azo[:, 0], Azo[:, 1])
plt.plot(A1[0], A1[1])
plt.plot(A2[0], A2[1])
plt.plot(A3[0], A3[1])
plt.plot(A4[0], A4[1])
plt.plot(A5[0], A5[1])
plt.plot(A6[0], A6[1])
plt.plot(A7[0], A7[1])
plt.plot(A8[0], A8[1])
plt.plot(A9[0], A9[1])
plt.plot(A10[0], A10[1])
plt.plot(A11[0], A11[1])


# Madeira

M1 = [[-16.4221, -16.3837, -16.3151, -16.2704, -16.2755, -16.3759, -16.4221],
      [33.035, 32.965, 33.058, 33.030, 33.154, 33.130, 33.035]]
# M1[2] is port

M2 = [[-16.42196, -16.42136, -16.41785, -16.41847, -16.42196],
      [32.84151, 32.83641, 32.83951, 32.84415, 32.84151]]
# M2 has no port

M3 = [[-17.2943, -17.1965, -16.9473, -16.9022, -16.8068, -16.6282, -16.8797, -17.2112, -17.2943],
      [32.815, 32.653, 32.593, 32.641, 32.598, 32.728, 32.904, 32.940, 32.815]]
# M3[3] is port

M4 = [[-16.5628, -16.5315, -16.4485, -16.5057, -16.5628],
      [32.609, 32.4, 32.378, 32.629, 32.609]]
# M4 has no port

mObj = [np.ndarray.tolist(np.asarray(M1).T), np.ndarray.tolist(np.asarray(M2).T),
        np.ndarray.tolist(np.asarray(M3).T), np.ndarray.tolist(np.asarray(M4).T)]

plt.plot(Mad[:, 0], Mad[:, 1])
plt.plot(M1[0], M1[1])
plt.plot(M2[0], M2[1])
plt.plot(M3[0], M3[1])
plt.plot(M4[0], M4[1])


# Continent
# special case where first node should connect to last to make an object but this edge can't be in graph

C1 = [[-8.678, -9.469, -9.594, -9.279, -9.308, -9, -8.612, -8.678],
      [41.11, 39.36, 38.66, 38.56, 38.21, 36.78, 37.09, 41.11]]
# C1[0], C1[3], C1[6] are ports

cObj = [np.ndarray.tolist(np.asarray(C1).T)]

plt.plot(cEEZ[:, 0], cEEZ[:, 1])
plt.plot(C1[0], C1[1])


# Obstacle graphs by zone

# Azores
aLg = []
for obj in aObj:
    for i in range(len(obj)-1):
        N = node(obj[i])
        aLg.append(N)
        N.next = node(obj[i+1])
        if i != 0:
            N.next.next = node(obj[i-1])
    aLg[-len(obj)+1].next.next = node(obj[len(obj)-2])


# Madeira
mLg = []
for obj in mObj:
    for i in range(len(obj)-1):
        N = node(obj[i])
        mLg.append(N)
        N.next = node(obj[i+1])
        if i != 0:
            N.next.next = node(obj[i-1])
    mLg[-len(obj)+1].next.next = node(obj[len(obj)-2])


# Continent
cLg = []
for obj in cObj:
    for i in range(len(obj)-1):
        N = node(obj[i])
        cLg.append(N)
        if i != len(obj)-2:
            N.next = node(obj[i+1])
        else:
            N.next = node(obj[i - 1])
        if i != 0 and i != len(obj)-2:
            N.next.next = node(obj[i-1])


# Check graphs

# Azores

Edg = []
for node in aLg:
    N = node
    P = node.cord
    while N.next:
        A = [P, N.next.cord]
        Edg.append(A)
        if [N.next.cord, P] not in Edg:
            A = np.asarray(A)
            plt.plot(A[:, 0], A[:, 1], color="blue")
        N = N.next
plt.show()

# Madeira

Edg = []
for node in mLg:
    N = node
    P = node.cord
    while N.next:
        A = [P, N.next.cord]
        Edg.append(A)
        if [N.next.cord, P] not in Edg:
            A = np.asarray(A)
            plt.plot(A[:, 0], A[:, 1], color="blue")
        N = N.next
plt.show()

# Continent

Edg = []
for node in cLg:
    N = node
    P = node.cord
    while N.next:
        A = [P, N.next.cord]
        Edg.append(A)
        if [N.next.cord, P] not in Edg:
            A = np.asarray(A)
            plt.plot(A[:, 0], A[:, 1], color="blue")
        N = N.next
plt.show()


# store all data

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\aObj.json", "w") as outfile:
    json.dump(aObj, outfile)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\mObj.json", "w") as outfile:
    json.dump(mObj, outfile)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\cObj.json", "w") as outfile:
    json.dump(cObj, outfile)

picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\aLg", 'wb')
pickle.dump(aLg, picklefile)
picklefile.close()

picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\mLg", 'wb')
pickle.dump(mLg, picklefile)
picklefile.close()

picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\cLg", 'wb')
pickle.dump(cLg, picklefile)
picklefile.close()
