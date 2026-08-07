import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. PARAMETERS
# ==========================================
kB_eV = 8.617333262e-5
T = 300.0  
bNorm = 2.722e-10 
mu = 161.0e9   

# Stress Magnitude (1.61 GPa)
s0 = 0.01 
applied_stress_mag = s0 * mu 

# Mobility Parameters (From your C++ Code)
Bs = 9.8e-4 
Be = 4.26e-4
dH0_vals = np.array([1.24, 0.71, 7.29, 1.91]) # eV

# Non-Schmid 
p = 0.86
q = 1.69
T0 = 0.8 * 3695.0 
tauC = 1.7e9 
a0 = 0.92
a1 = 0.0 # a1=0 for <100> usually, matching your file
a2 = 0.0
a3 = 0.0

# ==========================================
# 2. SOLVER FUNCTIONS
# ==========================================
def sigmoid(x):
    x = np.clip(x, -100, 100)
    return 2.0 / (1.0 + np.exp(2.0 * x))

def solve_5x5(A, b_vec):
    try:
        return np.linalg.solve(A, b_vec)
    except np.linalg.LinAlgError:
        return np.zeros(5)

def calculate_profile(stress_axis_normalized):
    m = stress_axis_normalized
    S = np.outer(m, m) * applied_stress_mag
    
    # Slip System Reference: b=[001], n=[110]
    b_vec = np.array([0, 0, 1])
    n_vec = np.array([1, 1, 0]) / np.sqrt(2)
    
    # 1. Resolve Stress
    tau = np.dot(n_vec, np.dot(S, b_vec))
    
    # Schmid Guard
    if abs(tau) < 1e-6:
        return None 

    # 2. Geometry for Activation (Screw Reference)
    s = b_vec 
    # n1 rotation (90 deg around s)
    n1 = np.array([-n_vec[1], n_vec[0], n_vec[2]]) 
    
    # Calculate Non-Schmid Terms
    # tauOrt = (n x s) . S . n
    vec_cross = np.cross(n_vec, s)
    tauOrt = np.dot(vec_cross, np.dot(S, n_vec))
    
    # tau1 = s . S . n1
    tau1 = np.dot(n1, np.dot(S, s))
    
    # tauOrt1 = (n1 x s) . S . n1
    vec_cross1 = np.cross(n1, s)
    tauOrt1 = np.dot(vec_cross1, np.dot(S, n1))
    
    # 3. Activation Energy (dg1)
    num = abs(tau + a1 * tau1)
    den_arg = (a2 * tauOrt + a3 * tauOrt1)
    if abs(a0 * tauC) > 1e-12:
        den_arg /= (a0 * tauC)
    
    den = a0 * tauC * sigmoid(den_arg)
    Theta = num / den if abs(den) > 1e-12 else 0.0
    
    dg = 0.0
    if Theta < 1.0:
        dg = (1.0 - Theta**p)**q - (T/T0)
    dg1 = dg if dg > 0.0 else 0.0
    
    # 4. Calculate Targets
    barrier_scale = 1.0 # C++ Value
    v_targ = np.zeros(4)
    for i in range(4):
        dG = dH0_vals[i] * barrier_scale * dg1
        if dG < 0: dG = 0.0
        
        B_val = Be if i == 3 else Bs
        pre_factor = (abs(tau) * bNorm) / B_val
        
        exponent = -dG / (2.0 * kB_eV * T)
        if exponent < -700: exponent = -700 # Safety
        
        v_targ[i] = pre_factor * np.exp(exponent)
        
    # 5. Build 5x5 System
    angles_deg = np.array([0.0, 35.3, 54.7, 90.0])
    angles_rad = np.radians(angles_deg)
    
    A_mat = np.zeros((5, 5))
    b_rhs = np.zeros(5)
    
    # Rows 0-3: Values
    for i in range(4):
        b_rhs[i] = v_targ[i]
        for k in range(5):
            A_mat[i, k] = np.cos(2 * k * angles_rad[i])
            
    # Row 4: Constraint (Slope=0 at 54.7)
    th_dip = angles_rad[2]
    b_rhs[4] = 0.0
    for k in range(1, 5):
        A_mat[4, k] = -2.0 * k * np.sin(2.0 * k * th_dip)
        
    coeffs = solve_5x5(A_mat, b_rhs)
    
    # 6. Check Minimum Velocity in Profile
    thetas = np.linspace(0, np.pi/2, 200)
    velocities = np.zeros_like(thetas)
    for k in range(5):
        velocities += coeffs[k] * np.cos(2 * k * thetas)
        
    min_v = np.min(velocities)
    return coeffs, min_v, v_targ

# ==========================================
# 3. FULL SPHERE SCAN
# ==========================================
print("Starting FULL SPHERE Scan...")
print("Testing all orientations (positive and negative coordinates).")
print("-" * 60)

# Fibonacci Sphere Algorithm (Uniform sampling of sphere)
num_points = 5000
golden_ratio = (1 + 5**0.5)/2
i = np.arange(0, num_points)
theta = 2 * np.pi * i / golden_ratio
phi = np.arccos(1 - 2*(i+0.5)/num_points)
x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi)

failures = []
min_global_v = 1e9

for k in range(num_points):
    m = np.array([x[k], y[k], z[k]])
    
    # Run Model
    res = calculate_profile(m)
    if res is None: continue 
    
    coeffs, min_v, targets = res
    
    # Track Global Min
    if min_v < min_global_v:
        min_global_v = min_v
    
    # Threshold Check (Allow numerical noise -1e-15)
    if min_v < -1e-12:
        failures.append((m, min_v))

print(f"\nScan Complete. Tested {num_points} orientations.")
print("-" * 60)

if len(failures) == 0:
    print(f"SUCCESS: No negative velocities detected.")
    print(f"Global Minimum Velocity found: {min_global_v:.4e} m/s")
else:
    print(f"WARNING: {len(failures)} orientations failed!")
    failures.sort(key=lambda x: x[1])
    print("\nWorst Offender:")
    print(f"Orientation: {failures[0][0]}")
    print(f"Velocity:    {failures[0][1]:.4e}")