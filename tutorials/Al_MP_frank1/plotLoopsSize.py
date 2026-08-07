import sys, os
import matplotlib.pyplot as plt
import numpy as np

# Adjust path if needed
sys.path.insert(0, '../../python')
try:
    from modlibUtils import *
except ImportError:
    print("Warning: modlibUtils not found, but we can bypass it for this specific plot!")

font = {'family' : 'normal', 'size' : 16}
plt.rc('font', **font)

def getAverageRadiusFromDensity(folderName):
    # Read the main data file
    F = np.loadtxt(folderName + '/F/F_0.txt')
    
    t_sim = F[:, 1] # Simulation time
    
    # Based on your F_labels.txt, the last 4 columns are the densities:
    # glissile, sessile, boundary, grain boundary.
    # We sum glissile and sessile for total loop density.
    total_density = F[:, -4] + F[:, -3] 
    
    # Calculate radius based on the decay of the initial density
    initial_density = total_density[0]
    
    # If initial density is 0 (no loops spawned), avoid division by zero
    if initial_density == 0:
        return t_sim, np.zeros_like(t_sim)
        
    # R_avg(t) = 330 * (Density(t) / Density(0))
    radius_A = 330.0 * (total_density / initial_density)
    
    return t_sim, radius_A

# --- Main Code ---
# Try to get the time conversion factor if modlibUtils is available
try:
    materialFile = 'inputFiles/' + getStringInFile('inputFiles/polycrystal.txt', 'materialFile')
    mu_SI = getValueInFile(materialFile, 'mu0_SI')    
    rho_SI = getValueInFile(materialFile, 'rho_SI')   
    b_SI = getValueInFile(materialFile, 'b_SI')       
    v_dd2SI = np.sqrt(mu_SI / rho_SI)
    t_dd2SI = b_SI / v_dd2SI
except:
    print("Using fallback time conversion...")
    t_dd2SI = 1e-9 # Fallback if material file parsing fails

# Get the data
t_sim, radius_A = getAverageRadiusFromDensity('.')
time_sec = t_sim * t_dd2SI

# --- Plotting ---
fig1 = plt.figure()
ax1 = plt.subplot(1, 1, 1)

ax1.plot(time_sec, radius_A, color='b', linewidth=2, label='10 grains') # Update label as needed

ax1.grid(linestyle='--', alpha=0.7)
ax1.set_xlim(left=0)
ax1.set_ylim(bottom=0, top=350) # Lock the Y-axis to easily see the 330 start

ax1.set_xlabel('Time [sec]')
ax1.set_ylabel(r'Average radius [$\AA$]')
ax1.legend(loc='lower left', frameon=False)

fig1.autofmt_xdate()
plt.show()
fig1.savefig("fig1_mean_radius.pdf", bbox_inches='tight')