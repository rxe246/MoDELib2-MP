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

materialFile="../../Library/Materials/W.txt"
T = 300 # [K]
mat=pyMoDELib.PolycrystallineMaterialBase(materialFile,T) # material object
mob111=pyMoDELib.DislocationMobilityBCC(mat) # mobility object
mob100=pyMoDELib.DislocationMobilityBCC100(mat) # mobility object

m=np.array([1,1,1]) # stress axis
m=m/np.linalg.norm(m); # normalized stress axis
s0=0.01 # stress amplitude [MPa/mu_SI] mat.mu_SI
S=np.outer(m,m)*s0 # stress tensor
b=np.array([1,1,-1]) # burgers vector mat.b_SI
b=b/np.linalg.norm(b)
n=np.array([1,0,1]) # plane normal
n=n/np.linalg.norm(n)

theta1 = range(360+1)
v111 = []
v100 = []

A = 0.02298
B = 0.01454
C = 0.010

for thetaDeg in range(360+1):
    theta=thetaDeg*np.pi/180 # angle between line tangent and burgers vector
    xi=angleAxis(theta,n)@b # rotate b about n to define the line tangent
    tau=n@S@b.transpose() # shear stress
    v=mob111.velocity(S,b,xi,n,T)
    v111.append(v)
    #print(v)

b=np.array([0,0,-1]) # burgers vector mat.b_SI
b=b/np.linalg.norm(b)
n=np.array([1,1,0]) # plane normal
n=n/np.linalg.norm(n)

for thetaDeg in range(360+1):
    theta=thetaDeg*np.pi/180 # angle between line tangent and burgers vector
    xi=angleAxis(theta,n)@b # rotate b about n to define the line tangent
    tau=n@S@b.transpose() # shear stress
    v=mob100.velocity(S,b,xi,n,T)
    v100.append(v)
    #print(v)

x1 = 54.7
x2 = 180 - 54.7

# Plot Velocity v Angle
fig, ax = plt.subplots(figsize=(12, 8))
plt.plot(theta1, v111, 'b', linewidth=4, label='<111> Mobility')
plt.plot(theta1, v100, 'r', linewidth=4, label='<100> Mobility')
#plt.plot(theta1, v100_peaks, 'r', linewidth=4, label='Gaussian V1')
#plt.plot(theta1, v100_gauss, 'g', linewidth=4, linestyle='--', label='Gaussian V2')
#plt.plot(theta1, v100_fourier, 'm-', linewidth=4, label='Fourier Fit (6 Coeffs)')
#plt.plot(theta1, v100_fourier2, 'k-', linewidth=4, label='Fourier Fit (4 Coeffs)')
plt.axvline(x1, color='k', linewidth=2, linestyle='--')
plt.axvline(x2, color='k', linewidth=2, linestyle='--')
plt.xlabel("Character Angle, θ, [Degrees]"); plt.xlim([0,180])
plt.ylabel("Velocity, v/c"); plt.ylim([None,None])
plt.grid(True)
plt.legend(loc='upper left')
plt.tight_layout()

plt.show()