# this script cleans the data pertaining to the coordinates of the Exclusive Economic Zones (EEZ) and Extended
# Continental Shelf (ECS). The EEZ data contains not only the boarder of the EEZ but also land masses within
# it, as such these are separated into two arrays. At the end all arrays are stored in json files

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import data
with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\
EEZ and ECS coordinates\Data Sources\Madeira_EEZ_json.txt", "r") as read_file:
    Mad = json.load(read_file)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\
EEZ and ECS coordinates\Data Sources\Azores_EEZ_json.txt", "r") as read_file:
    Azo = json.load(read_file)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\
EEZ and ECS coordinates\Data Sources\Portugal_EEZ_json.txt", "r") as read_file:
    Cont = json.load(read_file)

portECS = pd.read_excel(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\
EEZ and ECS coordinates\Data Sources\Portugal_ECS.xlsx")


# data selection and conversion to numpy arrays
mEEZ = np.array([element for sublist in Mad["features"][0]["geometry"]["coordinates"][0] for element in sublist]).T
aEEZ = np.array([element for sublist in Azo["features"][0]["geometry"]["coordinates"][0] for element in sublist]).T
cEEZ = np.array([element for sublist in Cont["features"][0]["geometry"]["coordinates"][0] for element in sublist]).T
ECS = np.array(portECS[["Longitude (W)", "Latitude (N)"]].values.tolist()).T


# Data cleaning and plots
for i in range(len(ECS[0])):
    ECS[0][i] = -ECS[0][i]

plt.plot(aEEZ[0], aEEZ[1], "o")
plt.plot(mEEZ[0], mEEZ[1], "o")
plt.plot(cEEZ[0], cEEZ[1], "o")
plt.plot(ECS[0], ECS[1], "o")
plt.show()

ECS = np.ndarray.tolist(np.vstack((cEEZ[:, 5649].T, ECS[:, 0:1938+1].T, mEEZ[:, 77:2814+1].T,
                                   ECS[:, 1939:1940+1].T, cEEZ[:, 4613:5649].T)))

Mad = np.ndarray.tolist(mEEZ[:, 2815:].T)

Azo = np.ndarray.tolist(aEEZ[:, 8172:].T)

mEEZ = np.ndarray.tolist(mEEZ[:, 0:2815].T)

aEEZ = np.ndarray.tolist(aEEZ[:, 0:8171].T)

cEEZ = np.ndarray.tolist(cEEZ.T)

plt.plot(aEEZ[:,0], aEEZ[:,1], "o")
plt.plot(mEEZ[:,0], mEEZ[:,1], "o")
plt.plot(cEEZ[:,0], cEEZ[:,1], "o")
plt.plot(ECS[:,0], ECS[:,1], "o")
plt.plot(Mad[:,0], Mad[:,1], "o")
plt.plot(Azo[:,0], Azo[:,1], "o")

# Store Data to files
with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\ECS.json", "w") as outfile:
    json.dump(ECS, outfile)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\Mad.json", "w") as outfile:
    json.dump(Mad, outfile)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\Azo.json", "w") as outfile:
    json.dump(Azo, outfile)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\mEEZ.json", "w") as outfile:
    json.dump(mEEZ, outfile)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\aEEZ.json", "w") as outfile:
    json.dump(aEEZ, outfile)

with open(r"C:\Users\Jorge Pereira\Desktop\Project SeaNet\Data\EEZ and ECS coordinates\cEEZ.json", "w") as outfile:
    json.dump(cEEZ, outfile)
