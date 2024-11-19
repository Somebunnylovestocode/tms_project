import numpy as np

# Define the deflection function for a simply supported circular plate
def deflection_circular_simply_supported(r, P, D, a):
    """
    Returns the deflection of a simply supported circular plate at a radial distance r.
    """
    # Maximum deflection formula for simply supported circular plate
    w_max = (P * a**4) / (64 * D)
    
    # Calculate deflection at radius r
    deflection = w_max * (1 - (r**2 / a**2))
    
    # Ensure that deflection does not exceed w_max
    return min(deflection, w_max)

# Define the deflection function for a clamped circular plate
def deflection_circular_clamped(r, P, D, a):
    """
    Returns the deflection of a clamped circular plate at a radial distance r.
    """
    # Maximum deflection formula for clamped circular plate
    w_max = (P * a**4) / (32 * D)
    
    # Calculate deflection at radius r
    deflection = w_max * (1 - (r**2 / a**2))
    
    # Ensure that deflection does not exceed w_max
    return min(deflection, w_max)

# Define the deflection function for a simply supported rectangular plate
def deflection_rectangular_simply_supported(x, y, P, D, a, b):
    """
    Returns the deflection of a simply supported rectangular plate at coordinates (x, y).
    """
    # For simplification, assume a summation of modes for simply supported plate
    deflection = 0
    for m in range(1, 5):  # First few terms for approximation
        for n in range(1, 5):
            W_mn = (P * a**4) / (D * (m**2 + n**2))
            deflection += W_mn * np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b)
    
    # Calculate maximum deflection
    w_max = (P * a**4) / (64 * D)
    
    # Ensure that deflection does not exceed w_max
    return min(deflection, w_max)

# Define the deflection function for a clamped rectangular plate
def deflection_rectangular_clamped(x, y, P, D, a, b):
    """
    Returns the deflection of a clamped rectangular plate at coordinates (x, y).
    """
    # For simplification, assume a summation of modes for clamped plate
    deflection = 0
    for m in range(1, 5):  # First few terms for approximation
        for n in range(1, 51):
            W_mn = (P * a**4) / (4 * D * (m**2 + n**2))
            deflection += W_mn * np.sin(m * np.pi * x / a) * np.sin(n * np.pi * y / b)
    
    # Calculate maximum deflection
    w_max = (P * a**4) / (32 * D)
    
    # Ensure that deflection does not exceed w_max
    return min(deflection, w_max)

# Main function to select the deflection function based on shape and boundary condition
def get_deflection_function(shape, boundary_condition, P, D, a, b=None):
    """
    Given the shape (circular or rectangular) and boundary condition (simply_supported or clamped),
    return the corresponding deflection function that can be integrated for capacitance calculation.
    """
    if shape == 'circular':
        if boundary_condition == 'simply_supported':
            return lambda r: deflection_circular_simply_supported(r, P, D, a)
        elif boundary_condition == 'clamped':
            return lambda r: deflection_circular_clamped(r, P, D, a)
        else:
            raise ValueError("Invalid boundary condition for circular plate")
    
    elif shape == 'rectangular':
        if boundary_condition == 'simply_supported':
            return lambda x, y: deflection_rectangular_simply_supported(x, y, P, D, a, b)
        elif boundary_condition == 'clamped':
            return lambda x, y: deflection_rectangular_clamped(x, y, P, D, a, b)
        else:
            raise ValueError("Invalid boundary condition for rectangular plate")
    
    else:
        raise ValueError("Invalid shape type. Choose 'circular' or 'rectangular'")

