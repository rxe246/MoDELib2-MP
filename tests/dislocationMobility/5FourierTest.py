import numpy as np
import matplotlib.pyplot as plt

# --- 1. PHYSICS PARAMETERS ---
# Constants
kB_eV = 8.617333262e-5
T = 300.0  # Kelvin
bNorm = 2.72e-10 
tau = 1.0e9 # 1 GPa Stress

# Mobility Parameters (From your W.txt)
Bs = 9.8e-4 
Be = 4.26e-04
dH0_vals = np.array([1.24, 0.71, 7.29, 1.91]) # eV (Literature)

# --- 2. CALCULATE TARGET POINTS ---
# Calculate V0, V35, V54, V90
v_targ = np.zeros(4)
for i in range(4):
    dG = (dH0_vals[i]) 
    if i == 3:
        pre_factor = (abs(tau) * bNorm) / Be
    else:
        pre_factor = (abs(tau) * bNorm) / Bs
    v_targ[i] = pre_factor * np.exp(-dG / (2.0 * kB_eV * T))

print("Target Velocities (m/s):")
print(f"  0 deg: {v_targ[0]:.4e}")
print(f" 35 deg: {v_targ[1]:.4e}")
print(f" 54 deg: {v_targ[2]:.4e}")
print(f" 90 deg: {v_targ[3]:.4e}")

# --- 3. SOLVE 5x5 SYSTEM ---
# Model: v(th) = c0 + c1*cos(2th) + c2*cos(4th) + c3*cos(6th) + c4*cos(8th)
angles_deg = np.array([0.0, 35.3, 54.7, 90.0])
angles_rad = angles_deg * np.pi / 180.0

A = np.zeros((5, 5))
b_vec = np.zeros(5)

# Rows 0-3: Fit the 4 points
for i in range(4):
    b_vec[i] = v_targ[i]
    for n in range(5):
        A[i, n] = np.cos(2 * n * angles_rad[i])

# Row 4: Slope Constraint at 54.7 deg (Minima)
# d/dtheta [ cos(2n*theta) ] = -2n * sin(2n*theta)
th_min = angles_rad[2] # 54.7 deg
b_vec[4] = 0.0
A[4, 0] = 0.0
for n in range(1, 5):
    A[4, n] = -2.0 * n * np.sin(2.0 * n * th_min)

# Solve
coeffs = np.linalg.solve(A, b_vec)
print("\n5-Coeff Coefficients:", coeffs)

# --- 4. PLOT ---
theta_plot = np.linspace(0, 360, 360) * np.pi / 180.0
v_plot = np.zeros_like(theta_plot)

for n in range(5):
    v_plot += coeffs[n] * np.cos(2 * n * theta_plot)

# Clamp for visualization (simulate C++ safety)
v_plot_clamped = np.maximum(v_plot, 0.0)

plt.figure(figsize=(10, 6))
plt.plot(np.degrees(theta_plot), v_plot, 'r--', label='5-Coeff (Raw)')
plt.plot(np.degrees(theta_plot), v_plot_clamped, 'r-', linewidth=2, label='5-Coeff (Clamped)')

# Plot Target Points
plt.plot(angles_deg, v_targ, 'bo', markersize=8, label='Target Points')
# Plot Mirror Points for visual check
plt.plot(180-angles_deg, v_targ, 'bo')
plt.plot(180+angles_deg, v_targ, 'bo')
plt.plot(360-angles_deg, v_targ, 'bo')

plt.axhline(0, color='k', linewidth=1)
plt.axvline(54.7, color='k', linestyle=':', alpha=0.5, label='Minima Constraint')
plt.axvline(125.3, color='k', linestyle=':', alpha=0.5)
plt.xlabel("Angle (deg)")
plt.ylabel("Velocity (m/s)")
plt.title("5-Coefficient Harmonic Fit with Slope Constraint")
plt.legend()
plt.grid(True)
plt.show()