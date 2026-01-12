#!/usr/bin/env python3
"""Main entry point for laser measurement volume calculations."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.measurement import LaserMeasurement
from src.volume_calculator import FrustumVolumeCalculator
from src.visualizer import MeasurementVisualizer


def main():
    parser = argparse.ArgumentParser(description="Calculate volumes from laser measurements")
    parser.add_argument("--n-points", type=int, default=30, help="Number of measurement points")
    parser.add_argument("--plot", action="store_true", help="Show visualization")
    parser.add_argument("--plot-2d", action="store_true", help="Show 2D plot only")
    parser.add_argument("--plot-3d", action="store_true", help="Show 3D plot only")
    
    args = parser.parse_args()
    
    # Create measurements
    m1 = LaserMeasurement(
        center_x=0, center_y=0, z=0,
        n_points=args.n_points,
        radius_min=25, radius_max=30,
        seed=42
    )
    
    m2 = LaserMeasurement(
        center_x=50, center_y=0, z=0,
        n_points=args.n_points,
        radius_min=20, radius_max=25,
        seed=123
    )
    
    # Calculate volumes
    calculator = FrustumVolumeCalculator(m1, m2)
    summary = calculator.get_summary()
    
    print(f"Number of sections: {summary['n_sections']}")
    print(f"Center distance: {summary['center_distance']:.2f}")
    print(f"\nFrustum Volumes: {[round(v, 2) for v in summary['frustum_volumes']]}")
    print(f"\nTotal Volume: {summary['total_volume']:.2f}")
    
    # Visualization
    if args.plot or args.plot_2d or args.plot_3d:
        import matplotlib.pyplot as plt
        visualizer = MeasurementVisualizer(m1, m2)
        
        if args.plot or args.plot_2d:
            visualizer.plot_2d()
        if args.plot or args.plot_3d:
            visualizer.plot_3d()
        
        plt.show()


if __name__ == "__main__":
    main()