# This script simply plot the total Portugal graph (PTg) with the boarders included,
# for better visualization

import pickle
import json
import numpy as np
from graphcls import node
import matplotlib.pyplot as plt


with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\aEEZ.json", "r") as read_file:
    aEEZ = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\mEEZ.json", "r") as read_file:
    mEEZ = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\cEEZ.json", "r") as read_file:
    cEEZ = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\ECS.json", "r") as read_file:
    ECS = np.asarray(json.load(read_file))

picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\PTg", 'rb')
PTg = pickle.load(picklefile)
picklefile.close()

Edg = []
for node in PTg:
    N = node
    P = node.cord
    while N.next:
        A = [P, N.next.cord]
        Edg.append(A)
        if [N.next.cord, P] not in Edg:
            A = np.asarray(A)
            plt.plot(A[:, 0], A[:, 1], color="blue", linewidth=0.2)
        N = N.next

plt.plot(ECS[:,0],ECS[:,1])
plt.plot(aEEZ[:,0],aEEZ[:,1])
plt.plot(mEEZ[:,0],mEEZ[:,1])
plt.plot(cEEZ[:,0],cEEZ[:,1])
plt.show()
