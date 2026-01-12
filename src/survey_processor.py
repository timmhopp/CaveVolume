"""Process cave survey data and calculate 3D coordinates."""
import math
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple


class SurveyProcessor:
    """Process cave survey data from CSV files."""
    
    def __init__(self, csv_path: str):
        self.survey = pd.read_csv(csv_path)
        self.points_dict: Dict[str, List[float]] = {}
        self.all_points: np.ndarray = None
        self.lines: List[List[List[float]]] = []
        self._process_survey()
    
    def _process_survey(self) -> None:
        """Convert survey measurements to 3D coordinates."""
        all_points_list = []
        
        for i in range(len(self.survey)):
            current_from = str(self.survey.iloc[i]["from"])
            current_to = str(self.survey.iloc[i]["to"])
            length = float(self.survey.iloc[i]["length"])
            clino = math.radians(float(self.survey.iloc[i]["clino"]))
            compass = math.radians(90 - float(self.survey.iloc[i]["compass"]))
            
            if current_from in self.points_dict:
                x, y, z = self.points_dict[current_from]
            else:
                x, y, z = 0, 0, 0
                self.points_dict[str(self.survey.iloc[0]["from"])] = [x, y, z]
            
            dx = length * math.cos(clino) * math.sin(compass)
            dy = length * math.cos(clino) * math.cos(compass)
            dz = length * math.sin(clino)
            
            x_new = x + dx
            y_new = y + dy
            z_new = z + dz
            
            self.points_dict[current_to] = [x_new, y_new, z_new]
            all_points_list.append([x_new, y_new, z_new])
            self.lines.append([[x, x_new], [y, y_new], [z, z_new]])
        
        self.all_points = np.array(all_points_list)
    
    def get_branching_points(self) -> List[str]:
        """Find points with multiple outgoing connections."""
        from_counts = self.survey["from"].value_counts() > 1
        return from_counts[from_counts].index.tolist()
