# Cave Volume Calculator

Calculate cave passage volumes from survey data using truncated cone approximation with intersection correction.

## Method

1. **Survey Processing**: Convert compass/clino/length measurements to 3D coordinates
2. **Volume Calculation**: Approximate each passage segment as a truncated elliptical cone
3. **Intersection Correction**: Use voxel grid to detect and subtract overlapping volumes at junctions

### Volume Formula

For each segment:

```
V = (pi/3) * L * (A1 + A2 + sqrt(A1 * A2))
```

Where:
- L = segment length
- A1 = width1 * height1 (start cross-section area)
- A2 = width2 * height2 (end cross-section area)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
# Basic calculation
python main.py data/test2.csv

# With visualization
python main.py data/test2.csv --plot ellipses

# Calculate intersection volumes
python main.py data/test2.csv --intersections --resolution 300

# Save results to CSV
python main.py data/test2.csv --output results.csv
```

### As Library

```python
from src.survey_processor import SurveyProcessor
from src.volume_calculator import VolumeCalculator
from src.visualizer import CaveVisualizer

# Load survey
processor = SurveyProcessor("data/test2.csv")

# Calculate volumes
calculator = VolumeCalculator(processor)
total = calculator.calculate_total_volume()
print(f"Total: {total:.2f} m3")

# Get detailed summary
summary = calculator.get_volume_summary()
for seg in summary:
    print(f"{seg['from']} -> {seg['to']}: {seg['sectional_volume']:.2f} m3")

# Calculate intersection corrections
intersection_v, total_intersection = calculator.calculate_intersection_volumes(resolution=300)
corrected = total - total_intersection

# Visualize
viz = CaveVisualizer(processor)
fig = viz.plot_with_ellipses()
fig.show()
```

## CSV Format

Required columns:
- `from`: Start station name
- `to`: End station name
- `length`: Distance (meters)
- `compass`: Bearing (degrees)
- `clino`: Inclination (degrees)
- `left`, `right`, `up`, `down`: Passage dimensions (meters)
