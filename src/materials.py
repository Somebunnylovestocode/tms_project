class Material:
    def __init__(self, name, young_mod, poisson_rat, dielectric_K):
        """
        Initialize a material with its properties.
        
        Parameters:
        - name: Name of the material
        - young_mod: Young's modulus (Pa)
        - poisson_rat: Poisson's ratio (dimensionless)
        - dielectric_K: Dielectric constant (dimensionless)
        """
        self.name = name
        self.young_mod = young_mod
        self.poisson_rat = poisson_rat
        self.dielectric_K = dielectric_K

    # Predefined materials for easy access
    PREDEFINED_MATERIALS = {
        "Aluminum": {"young_mod": 70e9, "poisson_rat": 0.33, "dielectric_K": 1},
        "Steel": {"young_mod": 200e9, "poisson_rat": 0.3, "dielectric_K": 1},
        "Glass": {"young_mod": 70e9, "poisson_rat": 0.2, "dielectric_K": 4.5},
        "Test": {"young_mod": 169.8e9, "poisson_rat": 0.066, "dielectric_K": 1.1}
    }

    @classmethod
    def get_material(cls, material_name):
        """
        Retrieve a material by name.
        
        Parameters:
        - material_name: The name of the material
        
        Returns:
        - A Material object if found, else None
        """
        material_properties = cls.PREDEFINED_MATERIALS.get(material_name, None)
        if material_properties:
            return Material(material_name, **material_properties)
        return None
    
    @classmethod
    def add_material(cls, name, young_mod, poisson_rat, dielectric_K):
        """
        Add a new material to the predefined materials list.
        
        Parameters:
        - name: Name of the new material
        - young_mod: Young's modulus (Pa)
        - poisson_rat: Poisson's ratio (dimensionless)
        - dielectric_K: Dielectric constant (dimensionless)
        
        Returns:
        - A new Material object
        """
        new_material = Material(name, young_mod, poisson_rat, dielectric_K)
        cls.PREDEFINED_MATERIALS[name] = {
            "young_mod": young_mod,
            "poisson_rat": poisson_rat,
            "dielectric_K": dielectric_K
        }
        return new_material

    @classmethod
    def list_materials(cls):
        """
        Get a list of all available material names.
        
        Returns:
        - List of material names as strings
        """
        return list(cls.PREDEFINED_MATERIALS.keys())