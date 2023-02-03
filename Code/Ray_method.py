# Here we have several function required to build the ECS graph and EEZ visibility graphs. For the ECS graph we
# simply need a subroutine to check if a point is within a given region. To do this we implement a ray method
# algorithm for the point-in-region problem.
# For the EEZ visibility graph we need to check if a given edge intersect some other edge (edges of obstacles).
# To do this we implement a variation of the ray method with a few extra steps


import numpy as np

# Ray method for ECS graph (point-in-region problem)


# This function is a subroutine of the point-in-region method presented in the next function (point_inr).
# Here we verify if the horizontal line extending to the right of a given point "p" intersects a given edge "e".
# To do this we simply check if the y-coordinate of the point is within the vertical bound of the edge "e"
# and if the point is to the left of the edge (by simply computing the angle orientation of the edge "e"
# with an edge that goes from the upper vertex of the edge "e" to the point "p").
def rline_intersect(p,e):
    if e[1,1]-e[0,1]<0:
        A = e[1,:]-e[0,:]
        B = p-e[0,:]
    else:
        A = e[0,:]-e[1,:]
        B = p-e[1,:]
    det = A[0]*B[1]-A[1]*B[0]
    if (e[0,1]<=p[1]<e[1,1] or e[0,1]>=p[1]>e[1,1]) and det<=0:
        return True

# This function checks if a given point is within a region "P" that has a single hole in it "Q" (inside the ECS but
# outside the EEZ of Azores which is inside the ECS). If "Q" is empty then the function runs as if the region has
# no hole in it. This is a simple variation of the ray method algorithm for point-in-region problems.
def point_inr(P, Q, p):
    cntp = 0
    cntq = 0
    for i in range(max(len(P), len(Q))-1):
        if i < len(P)-1:
            if rline_intersect(p,P[i:i+2,:]):
                cntp += 1
        if i < len(Q)-1:
            if rline_intersect(p,Q[i:i+2,:]):
                cntq += 1
    if (cntp+cntq) % 2 == 1:
        return True


# ray method for EEZ graphs

# This function is a subroutine of the point-in-region method presented in the next function (nvisible_edge).
# This is simply a variation of the function rline_intersect() above. Given the two edges "i","e" we apply a
# transformation to the plane so that the edge "i" is rooted at the origin of the plane and is now horizontal
# (so a translation and a rotation). If "i" intersects "e" then the y-coordinated of both vertices of "i"
# are within the vertical bounds of "e" and one of the vertices of "i" iz to the left of "e" and the other to the
# right
def edge_intersect(i,e):
    if i[1,1]<i[0,1]:
        E = i[1,:]-i[0,:]
        orgin=0
    else:
        E = i[0, :] - i[1, :]
        orgin=1
    theta = np.arccos(E[0]/(np.sqrt(E[0]*E[0]+E[1]*E[1])))
    M = np.asarray([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    it = (M @ (i-i[orgin,:]).T).T
    et = (M @ (e-i[orgin,:]).T).T
    if (et[0,1]<=it[0,1]<=et[1,1] or et[0,1]>=it[0,1]>=et[1,1]) and (et[0,1]<=it[1,1]<=et[1,1] or et[0,1]>=it[1,1]>=et[1,1]):
        if et[1,1]<et[0,1]:
            A = et[1,:]-et[0,:]
            B = it[0,:]-et[0,:]
            C = it[1,:]-et[0,:]
        else:
            A = et[0,:]-et[1,:]
            B = it[0,:]-et[1,:]
            C = it[1,:]-et[1,:]
        det1 = A[0] * B[1] - A[1] * B[0]
        det2 = A[0] * C[1] - A[1] * C[0]
        if (det1<0 and det2>0) or (det2<0 and det1>0):
            return True

# this function checks if a given edge "e" intersect any of the edges in a set "P"
def nvisible_edge(P, e):
    for i in range(len(P)):
        if not (e[0]==P[i][0] or e[0]==P[i][1] or e[1]==P[i][0] or e[1]==P[i][1]):
            if edge_intersect(np.asarray(e), np.asarray(P[i])):
                return True
