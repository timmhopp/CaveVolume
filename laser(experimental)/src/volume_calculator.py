"""Calculate volumes between laser measurements."""
import numpy as np
from typing import List
from .measurement import LaserMeasurement


class FrustumVolumeCalculator:
    """Calculate frustum volumes between two measurements."""
    
    def __init__(self, measurement1: LaserMeasurement, measurement2: LaserMeasurement):
        if measurement1.n_points != measurement2.n_points:
            raise ValueError("Measurements must have the same number of points")
        
        self.m1 = measurement1
        self.m2 = measurement2
        self.n_points = measurement1.n_points
        
        # Calculate center distance
        self.center_vec = self.m2.center - self.m1.center
        self.center_dist = np.linalg.norm(self.center_vec)
    
    def calculate_frustum_volume(self, index: int) -> float:
        """
        Calculate volume of a single frustum section.
        
        Uses the formula: V = (h/3) * (A1 + A2 + sqrt(A1*A2))
        where A1, A2 are the areas of the two triangular bases.
        """
        j = (index + 1) % self.n_points
        
        # Four points of the frustum
        A1 = self.m1.get_point(index)
        A2 = self.m1.get_point(j)
        B1 = self.m2.get_point(index)
        B2 = self.m2.get_point(j)
        
        # Calculate triangle areas using cross product
        base1_area = 0.5 * np.linalg.norm(np.cross(A1 - self.m1.center, A2 - self.m1.center))
        base2_area = 0.5 * np.linalg.norm(np.cross(B1 - self.m2.center, B2 - self.m2.center))
        
        # Height is the distance between centers
        h = self.center_dist
        
        # Frustum volume formula
        V = (h / 3) * (base1_area + base2_area + np.sqrt(base1_area * base2_area))
        return V
    
    def calculate_all_volumes(self) -> List[float]:
        """Calculate volumes for all frustum sections."""
        return [self.calculate_frustum_volume(i) for i in range(self.n_points)]
    
    def calculate_total_volume(self) -> float:
        """Calculate total volume."""
        return sum(self.calculate_all_volumes())
    
    def get_summary(self) -> dict:
        """Return volume calculation summary."""
        volumes = self.calculate_all_volumes()
        return {
            "frustum_volumes": volumes,
            "total_volume": sum(volumes),
            "n_sections": self.n_points,
            "center_distance": self.center_dist
        }