"""Generate laser measurement point data."""
import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class LaserMeasurement:
    """Represents a single laser measurement circle."""
    center_x: float
    center_y: float
    z: float
    n_points: int
    radius_min: float
    radius_max: float
    seed: int = None
    
    def __post_init__(self):
        self._generate_points()
    
    def _generate_points(self) -> None:
        """Generate measurement points around the center."""
        if self.seed is not None:
            np.random.seed(self.seed)
        
        self.angles = np.linspace(0, 360, self.n_points, endpoint=False)
        self.distances = np.random.uniform(self.radius_min, self.radius_max, self.n_points)
        
        self.x_points = self.center_x + self.distances * np.cos(np.radians(self.angles))
        self.y_points = self.center_y + self.distances * np.sin(np.radians(self.angles))
        self.z_points = np.full_like(self.x_points, self.z)
    
    @property
    def center(self) -> np.ndarray:
        """Return center as numpy array."""
        return np.array([self.center_x, self.center_y, self.z])
    
    def get_point(self, index: int) -> np.ndarray:
        """Get a single point by index."""
        return np.array([
            self.x_points[index],
            self.y_points[index],
            self.z_points[index]
        ])
    
    def get_all_points(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return all points as tuple of arrays."""
        return self.x_points, self.y_points, self.z_points