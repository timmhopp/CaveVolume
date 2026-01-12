{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 """Visualization functions for cave survey data."""\
import numpy as np\
import plotly.graph_objects as go\
from typing import List\
from .survey_processor import SurveyProcessor\
from .geometry import cone_implicit, rotation_matrix_x, rotation_matrix_y\
\
\
def generate_upright_ellipse_yz(center: List[float], width: float, height: float) -> tuple:\
    """Generate ellipse points in YZ plane."""\
    theta = np.linspace(0, 2 * np.pi, 50)\
    ellipse_y = width * np.cos(theta)\
    ellipse_z = height * np.sin(theta)\
    ellipse_x = np.zeros_like(theta)\
    \
    ellipse_y += center[1]\
    ellipse_z += center[2]\
    ellipse_x += center[0]\
    \
    return ellipse_x, ellipse_y, ellipse_z\
\
\
def generate_rotated_ellipse(center: List[float], width: float, height: float, \
                              compass: float, clino: float) -> tuple:\
    """Generate and rotate an ellipse in 3D."""\
    import math\
    theta = np.linspace(0, 2 * np.pi, 50)\
    ellipse_x = width * np.cos(theta)\
    ellipse_y = height * np.sin(theta)\
    ellipse_z = np.zeros_like(theta)\
\
    compass_rad = math.radians(90 - compass)\
    clino_rad = math.radians(clino)\
\
    rotation_y = np.array([\
        [np.cos(compass_rad), 0, np.sin(compass_rad)],\
        [0, 1, 0],\
        [-np.sin(compass_rad), 0, np.cos(compass_rad)]\
    ])\
\
    rotation_x = np.array([\
        [1, 0, 0],\
        [0, np.cos(clino_rad), -np.sin(clino_rad)],\
        [0, np.sin(clino_rad), np.cos(clino_rad)]\
    ])\
\
    rotation_matrix = rotation_y @ rotation_x\
\
    ellipse_points = np.stack([ellipse_x, ellipse_y, ellipse_z])\
    rotated_points = rotation_matrix @ ellipse_points\
    rotated_x = rotated_points[0] + center[0]\
    rotated_y = rotated_points[1] + center[1]\
    rotated_z = rotated_points[2] + center[2]\
\
    return rotated_x, rotated_y, rotated_z\
\
\
class CaveVisualizer:\
    """Create 3D visualizations of cave surveys."""\
    \
    def __init__(self, processor: SurveyProcessor):\
        self.processor = processor\
        self.survey = processor.survey\
        self.points_dict = processor.points_dict\
        self.all_points = processor.all_points\
        self.lines = processor.lines\
    \
    def plot_survey_path(self, width: int = 1000, height: int = 800) -> go.Figure:\
        """Plot survey points and connections."""\
        fig = go.Figure()\
        \
        fig.add_trace(go.Scatter3d(\
            x=self.all_points[:, 0],\
            y=self.all_points[:, 1],\
            z=self.all_points[:, 2],\
            mode='markers',\
            marker=dict(size=1, color='red'),\
            name='Points'\
        ))\
        \
        for line in self.lines:\
            fig.add_trace(go.Scatter3d(\
                x=line[0],\
                y=line[1],\
                z=line[2],\
                mode='lines',\
                line=dict(color='blue', width=2),\
                name='Connections',\
                showlegend=False\
            ))\
        \
        fig.update_layout(\
            scene=dict(aspectmode='data'),\
            title="Survey Points with Connections",\
            width=width,\
            height=height\
        )\
        \
        return fig\
    \
    def plot_with_ellipses(self, width: int = 1000, height: int = 800) -> go.Figure:\
        """Plot survey with cross-section ellipses in YZ plane."""\
        fig = go.Figure()\
        \
        for i in range(1, len(self.survey)):\
            current_row = self.survey.iloc[i]\
            center = self.points_dict[str(current_row["from"])]\
            w = abs(float(current_row['left'])) + abs(float(current_row['right']))\
            h = abs(float(current_row['down'])) + abs(float(current_row['up']))\
            \
            ellipse_x, ellipse_y, ellipse_z = generate_upright_ellipse_yz(center, w, h)\
            \
            fig.add_trace(go.Scatter3d(\
                x=ellipse_x,\
                y=ellipse_y,\
                z=ellipse_z,\
                mode='lines',\
                line=dict(color='red', width=2),\
                name=f'Ellipse \{i\}',\
                showlegend=False\
            ))\
        \
        for line in self.lines:\
            fig.add_trace(go.Scatter3d(\
                x=line[0],\
                y=line[1],\
                z=line[2],\
                mode='lines',\
                line=dict(color='blue', width=2),\
                name='Connections',\
                showlegend=False\
            ))\
        \
        fig.add_trace(go.Scatter3d(\
            x=self.all_points[:, 0],\
            y=self.all_points[:, 1],\
            z=self.all_points[:, 2],\
            mode='markers',\
            marker=dict(size=1, color='red'),\
            name='Points'\
        ))\
        \
        fig.update_layout(\
            scene=dict(\
                xaxis_title='X',\
                yaxis_title='Y',\
                zaxis_title='Z',\
                aspectmode='data'\
            ),\
            title="Survey Points with Ellipses",\
            width=width,\
            height=height\
        )\
        \
        return fig\
    \
    def plot_cones(self, resolution: int = 50, width: int = 1000, height: int = 800) -> go.Figure:\
        """Plot truncated cones for each segment."""\
        x = np.linspace(-10, 10, resolution)\
        y = np.linspace(-10, 10, resolution)\
        z = np.linspace(-10, 30, resolution)\
        X, Y, Z = np.meshgrid(x, y, z, indexing='ij')\
        \
        fig = go.Figure()\
        \
        for i in range(len(self.survey)):\
            current_row = self.survey.iloc[i]\
            center = self.points_dict[str(current_row["from"])]\
            \
            a0 = (current_row["left"] + current_row["right"]) / 2\
            b0 = (current_row["down"] + current_row["up"]) / 2\
            a1 = a0\
            b1 = b0\
            z0 = 0\
            z1 = current_row["length"]\
            \
            clino = current_row["clino"]\
            compass = current_row["compass"]\
            R = rotation_matrix_y(clino) @ rotation_matrix_x(90 - compass)\
            offset = np.array(center)\
            \
            cone = cone_implicit(X, Y, Z, a0, b0, a1, b1, z0, z1, R=R, offset=offset)\
            \
            fig.add_trace(go.Volume(\
                x=X.ravel(),\
                y=Y.ravel(),\
                z=Z.ravel(),\
                value=cone.ravel().astype(float),\
                isomin=0.5,\
                isomax=1,\
                opacity=0.1,\
                surface_count=10,\
                colorscale="Viridis",\
                showscale=False\
            ))\
        \
        fig.update_layout(\
            scene=dict(\
                xaxis_title='X',\
                yaxis_title='Y',\
                zaxis_title='Z',\
                aspectmode='data'\
            ),\
            title="3D Cones",\
            width=width,\
            height=height\
        )\
        \
        return fig}