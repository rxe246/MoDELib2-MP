# /opt/local/bin/python3.13 test.py
import sys, string, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

sys.path.append("../../python")
from modlibUtils import *
sys.path.append("../../build/tools/pyMoDELib")
import pyMoDELib

# Set global font to Times New Roman
plt.rcParams.update({
    'font.family': 'Times New Roman',
    'font.size': 20, #12,       # default font size
    'axes.labelsize': 30, #12,
    'axes.titlesize': 20, #14,
    'legend.fontsize': 20, #10,
    'xtick.labelsize': 20, #10,
    'ytick.labelsize': 20, #10
})

materialFile="../../Library/Materials/W_100.txt"
T = 300 # [K]
mat=pyMoDELib.PolycrystallineMaterialBase(materialFile,T) # material object
mob111=pyMoDELib.DislocationMobilityBCC(mat) # mobility object

m=np.array([-1,1,1]) # stress axis
m=m/np.linalg.norm(m); # normalized stress axis
s0=0.01 # stress amplitude [MPa/mu_SI] mat.mu_SI
S=np.outer(m,m)*s0 # stress tensor
b=np.array([1,1,1]) # burgers vector mat.b_SI
b=b/np.linalg.norm(b)
n=np.array([-1,0,1]) # plane normal
n=n/np.linalg.norm(n)

theta1 = range(360+1)
v111 = []
v100 = []

for thetaDeg in range(360+1):
    theta=thetaDeg*np.pi/180 # angle between line tangent and burgers vector
    xi=angleAxis(theta,n)@b # rotate b about n to define the line tangent
    tau=n@S@b.transpose() # shear stress
    v=mob111.velocity(S,b,xi,n,T)
    v111.append(v)
    print(v)

theta_o = 26.84137634
A = 0.01747818671
for thetaDeg in range(360+1):
    v = A * np.exp(-(thetaDeg/theta_o)**2) + A * np.exp(-((thetaDeg-180)/theta_o)**2)
    v100.append(v)

#print('max = ', np.max(v100))
#print('min = ', np.min(v100))


# Plot Velocity v Angle
fig, ax = plt.subplots(figsize=(12, 8))
plt.plot(theta1, v111, 'b', linewidth=4)
plt.plot(theta1, v100, 'r', linewidth=4)
plt.xlabel("Character Angle, θ, [Degrees]"); plt.xlim([0,180])
plt.ylabel("Velocity, v/c"); #plt.ylim([None,None])
plt.grid(True)
plt.legend(['<111>','<100>'], loc='upper left')
plt.tight_layout()

# theta = np.deg2rad(90)
# xi = angleAxis(theta, n) @ b

# s0_values = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])/161
# # Temperature sweep: 0 K to 1500 K in 1 K steps
# T_range = range(0, 6001, 1)
# # Write to file
# with open("T_C9T_Edge.txt", "w") as f:
#     # Header
#     header = "T " + " ".join([f"v_s0={s0:.4f}" for s0 in s0_values]) + "\n"
#     f.write(header)

#     # Loop over temperature
#     for T in T_range:
#         row = [f"{T}"]
#         mat = pyMoDELib.PolycrystallineMaterialBase(materialFile, T)
#         mob111 = pyMoDELib.DislocationMobilityBCC(mat)

#         # Loop over stress amplitudes
#         for s0 in s0_values:
#             S = np.outer(m, m) * s0
#             v = mob111.velocity(S, b, xi, n, T)
#             row.append(f"{v:.6e}")
#         f.write(" ".join(row) + "\n")

# s0_values = np.linspace(0.0, 6.0, 1000)/161
# # Temperatures
# temps = [0, 300, 600, 900, 1200, 1500]
# # Prepare output
# with open("T_C9S_Edge.txt", "w") as f:
#     f.write("s0 " + " ".join([f"v_T{T}" for T in temps]) + "\n")
#     for s0 in s0_values:
#         S = np.outer(m, m) * s0
#         row = [f"{s0:.6f}"]
#         for T in temps:
#             mat = pyMoDELib.PolycrystallineMaterialBase(materialFile, T)
#             mob111 = pyMoDELib.DislocationMobilityBCC(mat)
#             v = mob111.velocity(S, b, xi, n, T)
#             row.append(f"{v:.6e}")
#         f.write(" ".join(row) + "\n")

# with open("alt1_C001HT.txt", "w") as f:
#     f.write("Velocity Theta(deg)\n")
#     for thetaDeg in range(360+1):
#         theta=thetaDeg*np.pi/180 # angle between line tangent and burgers vector
#         xi=angleAxis(theta,n)@b # rotate b about n to define the line tangent
#         tau=n@S@b.transpose() # shear stress
#         v=mob111.velocity(S,b,xi,n,T)
#         f.write(f"{v} {thetaDeg}\n")
#         print(v) 

plt.show()