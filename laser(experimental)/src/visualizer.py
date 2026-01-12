"""Visualization functions for laser measurements."""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import Tuple
from .measurement import LaserMeasurement


class MeasurementVisualizer:
    """Visualize laser measurements and volumes."""
    
    def __init__(self, measurement1: LaserMeasurement, measurement2: LaserMeasurement):
        self.m1 = measurement1
        self.m2 = measurement2
    
    def plot_2d(self, figsize: Tuple[int, int] = (10, 5)) -> plt.Figure:
        """Create 2D plot of both measurements."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        
        # First measurement
        ax1.scatter(self.m1.x_points, self.m1.y_points, c='red', label='Points')
        ax1.scatter([self.m1.center_x], [self.m1.center_y], c='blue', s=80, label='Center')
        
        for i in range(self.m1.n_points):
            x1, y1 = self.m1.x_points[i], self.m1.y_points[i]
            x2, y2 = self.m1.x_points[(i+1) % self.m1.n_points], self.m1.y_points[(i+1) % self.m1.n_points]
            ax1.plot(
                [self.m1.center_x, x1, x2, self.m1.center_x],
                [self.m1.center_y, y1, y2, self.m1.center_y],
                'k-', alpha=0.4
            )
        
        ax1.set_title('Measurement 1')
        ax1.axis('equal')
        ax1.legend()
        
        # Second measurement
        ax2.scatter(self.m2.x_points, self.m2.y_points, c='green', label='Points')
        ax2.scatter([self.m2.center_x], [self.m2.center_y], c='purple', s=80, label='Center')
        
        for i in range(self.m2.n_points):
            x1, y1 = self.m2.x_points[i], self.m2.y_points[i]
            x2, y2 = self.m2.x_points[(i+1) % self.m2.n_points], self.m2.y_points[(i+1) % self.m2.n_points]
            ax2.plot(
                [self.m2.center_x, x1, x2, self.m2.center_x],
                [self.m2.center_y, y1, y2, self.m2.center_y],
                'k-', alpha=0.4
            )
        
        ax2.set_title('Measurement 2')
        ax2.axis('equal')
        ax2.legend()
        
        plt.tight_layout()
        return fig
    
    def plot_3d(self, figsize: Tuple[int, int] = (10, 8)) -> plt.Figure:
        """Create 3D plot showing connected measurements."""
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot measurement circles
        ax.plot(self.m1.x_points, self.m1.y_points, self.m1.z_points, 'ro-', label='Circle 1')
        ax.plot(self.m2.x_points, self.m2.y_points, self.m2.z_points, 'go-', label='Circle 2')
        
        # Plot connecting faces
        n = self.m1.n_points
        for i in range(n):
            j = (i + 1) % n
            verts_x = [
                self.m1.x_points[i], self.m1.x_points[j],
                self.m2.x_points[j], self.m2.x_points[i],
                self.m1.x_points[i]
            ]
            verts_y = [
                self.m1.y_points[i], self.m1.y_points[j],
                self.m2.y_points[j], self.m2.y_points[i],
                self.m1.y_points[i]
            ]
            verts_z = [
                self.m1.z_points[i], self.m1.z_points[j],
                self.m2.z_points[j], self.m2.z_points[i],
                self.m1.z_points[i]
            ]
            ax.plot(verts_x, verts_y, verts_z, color='gray', alpha=0.5)
        
        # Plot centers
        ax.scatter(
            [self.m1.center_x, self.m2.center_x],
            [self.m1.center_y, self.m2.center_y],
            [self.m1.z, self.m2.z],
            c='k', s=50, label='Centers'
        )
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Connected Measurements')
        ax.legend()
        
        plt.tight_layout()
        return fig
    
    def show_all(self) -> None:
        """Display both 2D and 3D plots."""
        self.plot_2d()
        self.plot_3d()
        plt.show()