import math

def calculate_v100(v111, h111, h100):
    """
    Calculates the normalized velocity of 100 dislocations (v100)
    given the velocity of 111 dislocations and their respective enthalpies.

    Based on the relation: v_100 = v_111 ^ (h_100 / h_111)
    This is derived from the Arrhenius law: v ~ exp(-H / kT)
    """
    # Avoid division by zero or log of zero errors
    if v111 <= 0:
        return 0.0
    if h111 == 0:
        raise ValueError("Enthalpy for 111 cannot be zero.")

    # The direct power law derived from eliminating kT
    exponent = h100 / h111
    v100 = pow(v111, exponent)
    
    return v100

# --- User Input Section ---
# Replace these values with your specific inputs
velocity_111_input = 0.0007354141115665397  # Normalized velocity (v/c)
enthalpy_111_input = 33                   # Reference enthalpy for 111
enthalpy_100_input = 195.9                   # Reference enthalpy for 100

# --- Calculation ---
velocity_100_output = calculate_v100(velocity_111_input, 
                                     enthalpy_111_input, 
                                     enthalpy_100_input)

# --- Output ---
print(f"Inputs:")
print(f"  v_111: {velocity_111_input}")
print(f"  H_111: {enthalpy_111_input}")
print(f"  H_100: {enthalpy_100_input}")
print("-" * 30)
print(f"Calculated v_100: {velocity_100_output}")