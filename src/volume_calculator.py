{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """Calculate cave volumes using truncated cone approximation."""\
import math\
import numpy as np\
from typing import List, Tuple, Dict\
from .survey_processor import SurveyProcessor\
from .geometry import cone_implicit, rotation_matrix_x, rotation_matrix_y\
\
\
def calculate_volume(width1: float, height1: float, width2: float, height2: float, length: float) -> float:\
    """\
    Calculate volume of truncated elliptical cone.\
    V = (1/3) * pi * L * (A1 + A2 + sqrt(A1 * A2))\
    """\
    A_1 = width1 * height1\
    A_2 = width2 * height2\
    V = 1/3 * np.pi * length * (A_1 + A_2 + math.sqrt(A_1 * A_2))\
    return V\
\
\
class VolumeCalculator:\
    """Calculate cave passage volumes."""\
    \
    def __init__(self, processor: SurveyProcessor):\
        self.processor = processor\
        self.survey = processor.survey\
        self.points_dict = processor.points_dict\
    \
    def calculate_sectional_volumes(self) -> List[float]:\
        """Calculate volume for each survey segment."""\
        sectional_v = []\
        \
        for i in range(len(self.survey) - 1):\
            current_row = self.survey.iloc[i]\
            next_row = self.survey.iloc[i + 1]\
            \
            length = abs(float(current_row['length']))\
            width1 = (abs(float(current_row['left'])) + abs(float(current_row['right']))) / 2\
            height1 = (abs(float(current_row['down'])) + abs(float(current_row['up']))) / 2\
            width2 = (abs(float(next_row['left'])) + abs(float(next_row['right']))) / 2\
            height2 = (abs(float(next_row['down'])) + abs(float(next_row['up']))) / 2\
            \
            volume = calculate_volume(width1, height1, width2, height2, length)\
            sectional_v.append(volume)\
        \
        return sectional_v\
    \
    def calculate_total_volume(self) -> float:\
        """Calculate total cave volume."""\
        return sum(self.calculate_sectional_volumes())\
    \
    def get_volume_summary(self) -> List[Dict]:\
        """Return volume calculation summary with from/to labels."""\
        sectional_v = self.calculate_sectional_volumes()\
        combined_data = []\
        \
        for i in range(len(sectional_v)):\
            from_point = self.survey.iloc[i]["from"]\
            to_point = self.survey.iloc[i]["to"]\
            volume = sectional_v[i]\
            combined_data.append(\{\
                "from": from_point,\
                "to": to_point,\
                "sectional_volume": volume\
            \})\
        \
        return combined_data\
    \
    def calculate_intersection_volumes(self, resolution: int = 300) -> Tuple[List[float], float]:\
        """Calculate intersection volumes at branching points using voxel grid."""\
        x = np.linspace(-5, 10, resolution)\
        y = np.linspace(-5, 10, resolution)\
        z = np.linspace(0, 30, resolution)\
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')\
        \
        from_counts = self.processor.get_branching_points()\
        intersection_volumes = []\
        \
        for point in from_counts:\
            x1, y1, z1 = self.points_dict[point]\
            \
            outgoing_connections = self.survey[self.survey["from"] == point]\
            cones = []\
            \
            for _, row in outgoing_connections.iterrows():\
                to_point = row["to"]\
                \
                a0 = (row["left"] + row["right"]) / 2\
                b0 = (row["down"] + row["up"]) / 2\
                \
                if not self.survey[self.survey["from"] == to_point].empty:\
                    a1 = (self.survey[self.survey["from"] == to_point]["left"].values[0] +\
                          self.survey[self.survey["from"] == to_point]["right"].values[0]) / 2\
                    b1 = (self.survey[self.survey["from"] == to_point]["down"].values[0] +\
                          self.survey[self.survey["from"] == to_point]["up"].values[0]) / 2\
                else:\
                    a1 = a0\
                    b1 = b0\
                \
                z0 = 0\
                z1_cone = row["length"]\
                \
                clino = row["clino"]\
                compass = row["compass"]\
                R = rotation_matrix_y(clino) @ rotation_matrix_x(90 - compass)\
                offset = np.array([x1, y1, z1])\
                \
                cone = cone_implicit(X, Y, Z, a0, b0, a1, b1, z0, z1_cone, R=R, offset=offset)\
                cones.append(cone)\
            \
            for i in range(len(cones)):\
                for j in range(i + 1, len(cones)):\
                    intersection = cones[i] & cones[j]\
                    voxel_volume = (x[1] - x[0]) * (y[1] - y[0]) * (z[1] - z[0])\
                    volume = np.sum(intersection) * voxel_volume\
                    intersection_volumes.append(volume)\
        \
        return intersection_volumes, sum(intersection_volumes)\
    \
    def get_corrected_volume(self, resolution: int = 300) -> float:\
        """Calculate total volume minus intersection volumes."""\
        total = self.calculate_total_volume()\
        _, intersection_total = self.calculate_intersection_volumes(resolution)\
        return total - intersection_total}