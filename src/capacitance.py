import numpy as np
from scipy.integrate import quad, dblquad
from .deflections import get_deflection_function
from .materials import Material

# Constants
epsilon_0 = 8.85418782e-12  # Permittivity of free space in F/m

def calculate_flexural_rigidity(young_mod, poisson_rat, thickness):
    """
    Calculate the flexural rigidity (D) of the plate based on the material properties.
    """
    return young_mod * thickness**3 / (12 * (1 - poisson_rat**2))

def calculate_capacitance_circular(shape, boundary_condition, P, material_name, thickness, a, d0):
    """
    Calculate the capacitance for a circular plate using the deflection functions, now with double integration.
    
    Parameters:
    - shape: 'circular'
    - boundary_condition: 'simply_supported' or 'clamped'
    - P: Applied force (N)
    - material_name: Name of the material
    - thickness: Thickness of the plate (m)
    - a: Radius of the circular plate (m)
    - d0: Initial gap distance (m)
    
    Returns:
    - Capacitance in Farads
    """
    # Get material properties
    material = Material.get_material(material_name)
    if material is None:
        raise ValueError(f"Material {material_name} not found!")

    # Calculate flexural rigidity
    D = calculate_flexural_rigidity(material.young_mod, material.poisson_rat, thickness)
    
    # Get deflection function
    deflection_func = get_deflection_function(shape, boundary_condition, P, D, a)
    
    # Define integrand for capacitance calculation in polar coordinates
    def integrand(r, theta):
        return r / (d0 - deflection_func(r))

    try:
        # Perform double integration over the plate area (in polar coordinates)
        result, _ = dblquad(
            integrand,
            0, 2 * np.pi,  # theta limits from 0 to 2π
            lambda theta: 0, lambda theta: a  # r limits from 0 to a
        )
        return material.dielectric_K * epsilon_0 * result
    except Exception as e:
        raise ValueError(f"Integration failed: {str(e)}")

def calculate_capacitance_rectangular(shape, boundary_condition, P, material_name, thickness, a, b, d0):
    """
    Calculate the capacitance for a rectangular plate using the deflection functions.
    
    Parameters:
    - shape: 'rectangular'
    - boundary_condition: 'simply_supported' or 'clamped'
    - P: Applied force (N)
    - material_name: Name of the material
    - thickness: Thickness of the plate (m)
    - a: Length of the rectangular plate (m)
    - b: Width of the rectangular plate (m)
    - d0: Initial gap distance (m)
    
    Returns:
    - Capacitance in Farads
    """
    # Get material properties
    material = Material.get_material(material_name)
    if material is None:
        raise ValueError(f"Material {material_name} not found!")

    # Calculate flexural rigidity
    D = calculate_flexural_rigidity(material.young_mod, material.poisson_rat, thickness)
    
    # Get deflection function
    deflection_func = get_deflection_function(shape, boundary_condition, P, D, a, b)
    
    # Define integrand for capacitance calculation
    def integrand(x, y):
        return 1 / (d0 - deflection_func(x, y))
    
    try:
        # Perform double integration over the plate area
        result = dblquad(
            integrand,
            0, b,  # y limits
            lambda y: 0, lambda y: a  # x limits
        )
        return material.dielectric_K * epsilon_0 * result[0]
    except Exception as e:
        raise ValueError(f"Integration failed: {str(e)}")

def calculate_capacitance(shape, boundary_condition, P, material_name, thickness, a, b=None, d0=1e-6):
    """
    Main function to calculate capacitance based on plate shape and parameters.
    
    Parameters:
    shape: 'circular' or 'rectangular'
    boundary_condition: 'simply_supported' or 'clamped'
    P: Applied force (N)
    material_name: Name of the material
    thickness: Thickness of the plate (m)
    a: Radius for circular plate or length for rectangular plate (m)
    b: Width for rectangular plate (m), None for circular plate
    d0: Initial gap distance (m), default 1 µm
    
    Returns:
    Capacitance value in Farads
    """
    if shape not in ['circular', 'rectangular']:
        raise ValueError("Shape must be either 'circular' or 'rectangular'")
    
    if boundary_condition not in ['simply_supported', 'clamped']:
        raise ValueError("Boundary condition must be either 'simply_supported' or 'clamped'")
    
    if shape == 'circular':
        return calculate_capacitance_circular(
            shape, boundary_condition, P, material_name, thickness, a, d0
        )
    else:  # rectangular
        if b is None:
            raise ValueError("Width 'b' must be specified for rectangular plate")
            print("Width 'b' must be specified for rectangular plate")
        print("Rectangle Caclc init")
        return calculate_capacitance_rectangular(
            shape, boundary_condition, P, material_name, thickness, a, b, d0
        )