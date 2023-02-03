Each file here has a description at the top and subsequent comentary. Here nonetheless we present the description of each file.

## Border_Data_Cleaning.py
This script cleans the data pertaining to the coordinates of the Exclusive Economic Zones (EEZ) and Extended
Continental Shelf (ECS). The EEZ data contains not only the boarder of the EEZ but also land masses within
it, as such these are separated into two arrays. At the end all arrays are stored in json files.

## Land_Data_Cleaning.py
This script redefines the coordinates of land masses, making a new boarder for these obstacles
of a simpler shape and away from land, so that this boarder can be traversed by the USV without hitting land.
This also greatly reduces the number of vertices\coordinates required to define these land masses. Attention
was paid to assure that vertices dedicated to ports in several land masses are present, so that the USV can
navigate to cole proximity of a port to then enter it (using other navigation systems). Once this is done we
convert this information into graphs. At the end we store all data, either in a json file or pickle file.

## graphcls.py
This contains simply the class that defines a graph object.

## ECS_graph.py
Here we built the graph inside the ECS zone. This graph is built by choosing a poit at random
inside the ECS and from there move in particular direction and distance and see if that endpoint
is also in the ECS, if so that point is added to the graph and edges in both direction are added as well.
Here we search in 6 direction from a starting point (multiples of 60 degrees), at a distance of 2 (this 2
can be seen as dimensionless here, but it represents a movement of 2 degrees (latitude\longitude) on the
face of the earth). We run an optimization routine on the chosen initial point to see if a small perturbation of
that point can increase the number of vertices in the ECS graph. The optimization algorithm used here is completely
informal and should be reviewed to improve outcomes.

## EEZ_graphs.py
Here we built all the EEZ visibility graphs and the final complete graph over all zones of the Portuguese
maritime territory. Special attention had to be taken to several special cases and caveat. We build first the
graphs inside each EEZ independently and then connect them all to the ECS graph, thus producing the final complete graph.
Regarding the Visibility Graphs we choose two vertices in the corresponding graph (we're working with) and see if the edge 
connecting them is not within an obstacle, then we check if it doesn't intersect any other obstacle's edge, 
if not then those vertices are "visible" and can be connected (in both ways). We also memoize the 
already processed pairs to avoid reprocessing them again.

## Ray_method.py
Here we have several function required to build the ECS graph and EEZ visibility graphs. For the ECS graph we
simply need a subroutine to check if a point is within a given region. To do this we implement a ray method
algorithm for the point-in-region problem.
For the EEZ visibility graph we need to check if a given edge intersect some other edge (edges of obstacles).
To do this we implement a variation of the ray method with a few extra steps. More information in the comments 
within the file.

## PTg_plot.py
This script simply plot the total graph (PTgraph) with the boarders included,
for better visualization.
