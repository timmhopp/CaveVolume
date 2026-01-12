"""Geometry functions for cone calculations."""
import numpy as np


def rotation_matrix_x(angle_deg: float) -> np.ndarray:
    """Rotation matrix around X axis."""
    angle = np.radians(angle_deg)
    return np.array([
        [1, 0, 0],
        [0, np.cos(angle), -np.sin(angle)],
        [0, np.sin(angle), np.cos(angle)]
    ])


def rotation_matrix_y(angle_deg: float) -> np.ndarray:
    """Rotation matrix around Y axis."""
    angle = np.radians(angle_deg)
    return np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
    ])


def rotation_matrix_z(angle_deg: float) -> np.ndarray:
    """Rotation matrix around Z axis."""
    angle = np.radians(angle_deg)
    return np.array([
        [np.cos(angle), -np.sin(angle), 0],
        [np.sin(angle), np.cos(angle), 0],
        [0, 0, 1]
    ])


def cone_implicit(X: np.ndarray, Y: np.ndarray, Z: np.ndarray,
                  a0: float, b0: float, a1: float, b1: float,
                  z0: float, z1: float,
                  R: np.ndarray = None, offset: np.ndarray = None) -> np.ndarray:
    """
    Define elliptical truncated cone using implicit surface test.
    
    Args:
        X, Y, Z: Meshgrid arrays
        a0, b0: Base ellipse semi-axes
        a1, b1: Top ellipse semi-axes
        z0, z1: Height range
        R: Rotation matrix (default: identity)
        offset: Translation vector (default: zero)
    
    Returns:
        Boolean array indicating points inside cone
    """
    if R is None:
        R = np.eye(3)
    if offset is None:
        offset = np.zeros(3)
    
    points = np.stack([X.ravel(), Y.ravel(), Z.ravel()])
    points = np.linalg.inv(R) @ (points - offset[:, np.newaxis])
    x, y, z = points
    
    t = (z - z0) / (z1 - z0)
    inside_height = (t >= 0) & (t <= 1)
    
    a_t = (1 - t) * a0 + t * a1
    b_t = (1 - t) * b0 + t * b1
    
    inside_ellipse = (x / a_t) ** 2 + (y / b_t) ** 2 <= 1
    
    return (inside_height & inside_ellipse).reshape(X.shape)
