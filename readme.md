# Cave Volume Calculator

Calculate cave passage volumes from survey data using truncated cone approximation with intersection correction.

## Method
1. **Survey Processing**: Convert compass/clino/length measurements to 3D coordinates
2. **Volume Calculation**: Approximate each passage segment as a truncated elliptical cone
3. **Intersection Correction**: Use voxel grid to detect and subtract overlapping volumes at junctions
___
### Survey Processing

Calculate point location from section length, compass (yaw; around Z),and clinometer reading (pitch; around Y). First point in data read as (0,0,0).

$$ dx = \text{LENGTH} \cdot \cos(\text{CLINO}) \cdot \sin(90 - \text{COMPASS}) $$
$$ dy = \text{LENGTH} \cdot \cos(\text{CLINO}) \cdot \cos(90 - \text{COMPASS}) $$
$$ dz = \text{LENGTH} \cdot \sin(\text{CLINO}) $$

<p float="left">
  <img src="https://github.com/timmhopp/CaveVolume/blob/main/figures/system.png" width="59%" />
  <img src="https://github.com/timmhopp/CaveVolume/blob/main/figures/system_detail.png" width="39%" /> 
</p>

### Volume Formula

For each segment:

```
V = (pi/3) * L * (A1 + A2 + sqrt(A1 * A2))
```

Where:
- L = segment length
- A1 = width1 * height1 (start cross-section area)
- A2 = width2 * height2 (end cross-section area)

### Intersection Correction
As method of measuring can lead to overlapping segments, volume corretions are necessary to remove potential redundant volumes. Cave segments are considered as their outer surfaces:

$$
\overrightarrow{X}(u,v)=\overrightarrow{P_0}+u\overrightarrow{d}
+\big[(1-u)r_{1a}+u r_{2a}\big]\cos(v)\overrightarrow{e_1}
+\big[(1-u)r_{1b}+u r_{2b}\big]\sin(v)\overrightarrow{e_2}
$$



**Where:**

| Symbol | Description |
|------|-------------|
| $\overrightarrow{P_0}$ | The center of the start ellipse |
| $\overrightarrow{P_1}$ | The center of the end ellipse |
| $u \in [0,1]$ | Interpolating parameter of the height of the cone from $\overrightarrow{P_0}$ to $\overrightarrow{P_1}$ |
| $v \in [0,2\pi]$ | Angle parameter describing the ellipses |
| $\overrightarrow{d}$ | Vector along the centreline $\overrightarrow{P_1} - \overrightarrow{P_0}$ |
| $\overrightarrow{e_1}, \overrightarrow{e_2}$ | Orthonormal vectors perpendicular to $\overrightarrow{d}$ |

and their orientation in space by:

$$
R_x =
\begin{bmatrix}
1 & 0 & 0 \\
0 & \cos(\alpha) & -\sin(\alpha) \\
0 & \sin(\alpha) & \cos(\alpha)
\end{bmatrix}
$$

and

$$
R_y =
\begin{bmatrix}
\cos(\beta) & 0 & \sin(\beta) \\
0 & 1 & 0 \\
-\sin(\beta) & 0 & \cos(\beta)
\end{bmatrix}
$$

**Where:**

| Symbol | Description |
|------|-------------|
| $\alpha$ | Rotation around the x-axis (polar orientation) |
| $\beta$ | Rotation around the y-axis (inclination) |

They are then voxalized, shared voxels considered as overlap, and removed once.

Example:

<p float="left">
  <img src="https://github.com/timmhopp/CaveVolume/blob/main/figures/intersection.png" width="39%" />
  <img src="https://github.com/timmhopp/CaveVolume/blob/main/figures/intersection_calc.png" width="39%" /> 
</p>


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

___

Detailed explanations can be found in the seminar paper pdf
