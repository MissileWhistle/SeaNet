# Here we'll build the graph inside the ECS zone. This graph is built by choosing a poit at random
# inside the ECS and from there move in particular direction and distance and see if that endpoint
# is also in the ECS, if so that point is added to the graph and edges in both direction are added as well.
# Here we search in 6 direction from a starting point (multiples of 60 degrees), at a distance of 2 (this 2
# can be seen as dimensionless here, but it represents a movement of 2 degrees (latitude\longitude) on the
# face of the earth). We run an optimization routine on the chosen initial point to see if a small perturbation of
# that point can increase the number of vertices in the ECS graph. The optimization algorithm used here is completely
# informal and should be reviewed to improve outcomes.

import json
import pickle
import Ray_method as ray
from graphcls import node
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt


# import data
with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\ECS.json", "r") as read_file:
    ECS = np.asarray(json.load(read_file))

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\aEEZ.json", "r") as read_file:
    aEEZ = np.asarray(json.load(read_file))

# set of possible direction one can go from a particular point in space
dir = [[np.cos(np.pi/6+0*np.pi/3), np.sin(np.pi/6+0*np.pi/3)], [0,1],
       [-np.cos(np.pi/6+0*np.pi/3), np.sin(np.pi/6+0*np.pi/3)],
       [-np.cos(np.pi/6+0*np.pi/3), -np.sin(np.pi/6+0*np.pi/3)], [0,-1],
       [np.cos(np.pi/6+0*np.pi/3), -np.sin(np.pi/6+0*np.pi/3)]]


# graph building function, from a particular point and edge length. This function runs a point-in-region
# algorithm to know if a certain point is in the ECS (refer to Ray_method.py file, function point_inr()).
def ECSgraph(p, d, ECSg=None, Grc=None):
    if ECSg is None and Grc is None:
        ECSg = []
        Grc = []
    if ray.point_inr(ECS,aEEZ,p) and p not in Grc:
        P = node(p)
        ECSg.append(P)
        Grc.append(p)
        for i in range(6):
            q = [p[0] + d*dir[i][0], p[1] + d*dir[i][1]]
            if ray.point_inr(ECS,aEEZ,q):
                P.next = node(q)
                P = P.next
                ECSgraph(q,d,ECSg,Grc)
    return ECSg, Grc


# function to optimize; ECSgraph function depending only on the parameter to be optimized (initial
# point to build graph)
def ECSgf(p):
    graph, nodes = ECSgraph(np.ndarray.tolist(p), 2)
    return -len(nodes)


# optimization routine
x0 = np.asarray([-35, 35])
res = minimize(ECSgf, x0)
p = res.x
print(p)

# build graph with optimized parameter
ECSg, Grc = ECSgraph(np.ndarray.tolist(p), 2)

# plot graph
plt.plot(ECS[:,0], ECS[:,1])
plt.plot(aEEZ[:,0], aEEZ[:,1])
plt.plot(np.asarray(Grc)[:,0], np.asarray(Grc)[:,1], 'o')
plt.show()

# Save graph to file (pickle)
picklefile = open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\ECSg", 'wb')
pickle.dump(ECSg, picklefile)
picklefile.close()
