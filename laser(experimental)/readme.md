# Laser Measurement Volume Calculator

Calculate volumes between two laser measurement circles using frustum approximation.

This is conceptual and has not been tested on real-world data. Only calculations of single segment supported. Calculating point locations possible with main script, subsititue data reading and volume calculation should lead to functioning volume estimation. Corrections should be done on all frustums in segments.
## Method

Measurements are considered as $n$ points around X. Points of two measurements are matched by angle. Segments are split into frustum sections.

<p float="left">
  <img src="https://github.com/timmhopp/CaveVolume/blob/main/laser(experimental)/figures/laser_circles.png" width="49%" />
  <img src="https://github.com/timmhopp/CaveVolume/blob/main/laser(experimental)/figures/laser_frustum.png" width="39%" />
</p>

1. **Measurements**: Generate points around two measurement centers with random distances
2. **Volume Calculation**: Divide the space into frustum sections between corresponding points
3. **Frustum Formula**: `V = (h/3) * (A1 + A2 + sqrt(A1*A2))`

Where:
- h = distance between centers
- A1, A2 = triangular base areas at each measurement

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Basic calculation
python main.py

# With visualization
python main.py --plot

# Custom number of points
python main.py --n-points 50 --plot
```

### As Library

```python
from src.measurement import LaserMeasurement
from src.volume_calculator import FrustumVolumeCalculator
from src.visualizer import MeasurementVisualizer

# Create measurements
m1 = LaserMeasurement(
    center_x=0, center_y=0, z=0,
    n_points=30,
    radius_min=25, radius_max=30,
    seed=42
)

m2 = LaserMeasurement(
    center_x=50, center_y=0, z=0,
    n_points=30,
    radius_min=20, radius_max=25,
    seed=123
)

# Calculate volume
calculator = FrustumVolumeCalculator(m1, m2)
print(f"Total Volume: {calculator.calculate_total_volume():.2f}")

# Visualize
viz = MeasurementVisualizer(m1, m2)
viz.show_all()
```
