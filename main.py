{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #!/usr/bin/env python3\
"""Main entry point for cave volume calculations."""\
import argparse\
import sys\
import pandas as pd\
from pathlib import Path\
\
sys.path.insert(0, str(Path(__file__).parent))\
\
from src.survey_processor import SurveyProcessor\
from src.volume_calculator import VolumeCalculator\
from src.visualizer import CaveVisualizer\
\
\
def main():\
    parser = argparse.ArgumentParser(description="Calculate cave volumes from survey data")\
    parser.add_argument("csv_file", help="Path to survey CSV file")\
    parser.add_argument("--resolution", type=int, default=300,\
                        help="Voxel grid resolution for intersection calculations")\
    parser.add_argument("--plot", choices=["path", "ellipses", "cones"],\
                        help="Show 3D visualization")\
    parser.add_argument("--output", help="Output CSV file for sectional volumes")\
    parser.add_argument("--intersections", action="store_true",\
                        help="Calculate intersection volumes (slow)")\
    \
    args = parser.parse_args()\
    \
    print(f"Loading survey: \{args.csv_file\}")\
    processor = SurveyProcessor(args.csv_file)\
    print(f"Processed \{len(processor.points_dict)\} survey stations")\
    \
    calculator = VolumeCalculator(processor)\
    sectional_v = calculator.calculate_sectional_volumes()\
    total_v = sum(sectional_v)\
    \
    print(f"\\nTotal Volume: \{total_v:.2f\} m3")\
    print(f"Sectional Volumes: \{[round(v, 2) for v in sectional_v]\} m3")\
    \
    summary = calculator.get_volume_summary()\
    print("\\nSegment Details:")\
    for entry in summary:\
        print(f"  \{entry['from']\} -> \{entry['to']\}: \{entry['sectional_volume']:.2f\} m3")\
    \
    if args.intersections:\
        print(f"\\nCalculating intersections (resolution=\{args.resolution\})...")\
        intersection_v, total_intersection = calculator.calculate_intersection_volumes(args.resolution)\
        print(f"Intersection Volumes: \{intersection_v\}")\
        print(f"Total Intersection Volume: \{total_intersection:.2f\} m3")\
        corrected = total_v - total_intersection\
        print(f"Corrected Total Volume: \{corrected:.2f\} m3")\
    \
    if args.output:\
        df = pd.DataFrame(summary)\
        df = df.round(decimals=2)\
        df.to_csv(args.output, index=False)\
        print(f"\\nResults saved to \{args.output\}")\
    \
    if args.plot:\
        visualizer = CaveVisualizer(processor)\
        if args.plot == "path":\
            fig = visualizer.plot_survey_path()\
        elif args.plot == "ellipses":\
            fig = visualizer.plot_with_ellipses()\
        elif args.plot == "cones":\
            fig = visualizer.plot_cones()\
        fig.show()\
\
\
if __name__ == "__main__":\
    main()}