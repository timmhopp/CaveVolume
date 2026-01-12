{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Bold;\f1\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red107\green0\blue1;\red255\green255\blue255;\red0\green0\blue0;
\red9\green60\blue148;\red0\green0\blue109;\red144\green1\blue18;\red15\green112\blue1;\red19\green118\blue70;
\red0\green0\blue255;}
{\*\expandedcolortbl;;\cssrgb\c50196\c0\c0;\cssrgb\c100000\c100000\c100000;\cssrgb\c0\c0\c0;
\cssrgb\c1569\c31765\c64706;\cssrgb\c0\c0\c50196;\cssrgb\c63922\c8235\c8235;\cssrgb\c0\c50196\c0;\cssrgb\c3529\c52549\c34510;
\cssrgb\c0\c0\c100000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\b\fs24 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 # Cave Volume Calculator
\f1\b0 \cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 Calculate cave passage volumes from survey data using truncated cone approximation with intersection correction.\cb1 \
\
\pard\pardeftab720\partightenfactor0

\f0\b \cf2 \cb3 \strokec2 ## Method
\f1\b0 \cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 1.\cf0 \strokec4  
\f0\b \cf6 \strokec6 **Survey Processing**
\f1\b0 \cf0 \strokec4 : Convert compass/clino/length measurements to 3D coordinates\cb1 \
\cf5 \cb3 \strokec5 2.\cf0 \strokec4  
\f0\b \cf6 \strokec6 **Volume Calculation**
\f1\b0 \cf0 \strokec4 : Approximate each passage segment as a truncated elliptical cone\cb1 \
\cf5 \cb3 \strokec5 3.\cf0 \strokec4  
\f0\b \cf6 \strokec6 **Intersection Correction**
\f1\b0 \cf0 \strokec4 : Use voxel grid to detect and subtract overlapping volumes at junctions\cb1 \
\
\pard\pardeftab720\partightenfactor0

\f0\b \cf2 \cb3 \strokec2 ### Volume Formula
\f1\b0 \cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 For each segment:\cb1 \
\
\cb3 ```\cb1 \
\cb3 V = (pi/3) * L * (A1 + A2 + sqrt(A1 * A2))\cb1 \
\cb3 ```\cb1 \
\
\cb3 Where:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 -\cf0 \strokec4  L = segment length\cb1 \
\cf5 \cb3 \strokec5 -\cf0 \strokec4  A1 = width1 * height1 (start cross-section area)\cb1 \
\cf5 \cb3 \strokec5 -\cf0 \strokec4  A2 = width2 * height2 (end cross-section area)\cb1 \
\
\pard\pardeftab720\partightenfactor0

\f0\b \cf2 \cb3 \strokec2 ## Installation
\f1\b0 \cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 ```bash\cb1 \
\cb3 pip \cf7 \strokec7 install\cf0 \strokec4  \cf7 \strokec7 -r\cf0 \strokec4  \cf7 \strokec7 requirements.txt\cf0 \cb1 \strokec4 \
\cb3 ```\cb1 \
\
\pard\pardeftab720\partightenfactor0

\f0\b \cf2 \cb3 \strokec2 ## Usage
\f1\b0 \cf0 \cb1 \strokec4 \
\

\f0\b \cf2 \cb3 \strokec2 ### Command Line
\f1\b0 \cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 ```bash\cb1 \
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # Basic calculation\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 python \cf7 \strokec7 main.py\cf0 \strokec4  \cf7 \strokec7 data/test2.csv\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # With visualization\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 python \cf7 \strokec7 main.py\cf0 \strokec4  \cf7 \strokec7 data/test2.csv\cf0 \strokec4  \cf7 \strokec7 --plot\cf0 \strokec4  \cf7 \strokec7 ellipses\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # Calculate intersection volumes\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 python \cf7 \strokec7 main.py\cf0 \strokec4  \cf7 \strokec7 data/test2.csv\cf0 \strokec4  \cf7 \strokec7 --intersections\cf0 \strokec4  \cf7 \strokec7 --resolution\cf0 \strokec4  \cf9 \strokec9 300\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # Save results to CSV\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 python \cf7 \strokec7 main.py\cf0 \strokec4  \cf7 \strokec7 data/test2.csv\cf0 \strokec4  \cf7 \strokec7 --output\cf0 \strokec4  \cf7 \strokec7 results.csv\cf0 \cb1 \strokec4 \
\cb3 ```\cb1 \
\
\pard\pardeftab720\partightenfactor0

\f0\b \cf2 \cb3 \strokec2 ### As Library
\f1\b0 \cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 ```python\cb1 \
\pard\pardeftab720\partightenfactor0
\cf10 \cb3 \strokec10 from\cf0 \strokec4  src.survey_processor \cf10 \strokec10 import\cf0 \strokec4  SurveyProcessor\cb1 \
\cf10 \cb3 \strokec10 from\cf0 \strokec4  src.volume_calculator \cf10 \strokec10 import\cf0 \strokec4  VolumeCalculator\cb1 \
\cf10 \cb3 \strokec10 from\cf0 \strokec4  src.visualizer \cf10 \strokec10 import\cf0 \strokec4  CaveVisualizer\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # Load survey\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 processor = SurveyProcessor(\cf7 \strokec7 "data/test2.csv"\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # Calculate volumes\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 calculator = VolumeCalculator(processor)\cb1 \
\cb3 total = calculator.calculate_total_volume()\cb1 \
\cb3 print(\cf10 \strokec10 f\cf7 \strokec7 "Total: \cf0 \strokec4 \{total\cf10 \strokec10 :.2f\cf0 \strokec4 \}\cf7 \strokec7  m3"\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # Get detailed summary\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 summary = calculator.get_volume_summary()\cb1 \
\pard\pardeftab720\partightenfactor0
\cf10 \cb3 \strokec10 for\cf0 \strokec4  seg \cf10 \strokec10 in\cf0 \strokec4  summary:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     print(\cf10 \strokec10 f\cf7 \strokec7 "\cf0 \strokec4 \{seg[\cf7 \strokec7 'from'\cf0 \strokec4 ]\}\cf7 \strokec7  -> \cf0 \strokec4 \{seg[\cf7 \strokec7 'to'\cf0 \strokec4 ]\}\cf7 \strokec7 : \cf0 \strokec4 \{seg[\cf7 \strokec7 'sectional_volume'\cf0 \strokec4 ]\cf10 \strokec10 :.2f\cf0 \strokec4 \}\cf7 \strokec7  m3"\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # Calculate intersection corrections\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 intersection_v, total_intersection = calculator.calculate_intersection_volumes(resolution=\cf9 \strokec9 300\cf0 \strokec4 )\cb1 \
\cb3 corrected = total - total_intersection\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf8 \cb3 \strokec8 # Visualize\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 viz = CaveVisualizer(processor)\cb1 \
\cb3 fig = viz.plot_with_ellipses()\cb1 \
\cb3 fig.show()\cb1 \
\cb3 ```\cb1 \
\
\pard\pardeftab720\partightenfactor0

\f0\b \cf2 \cb3 \strokec2 ## CSV Format
\f1\b0 \cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 Required columns:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 -\cf0 \strokec4  \cf2 \strokec2 `from`\cf0 \strokec4 : Start station name\cb1 \
\cf5 \cb3 \strokec5 -\cf0 \strokec4  \cf2 \strokec2 `to`\cf0 \strokec4 : End station name\cb1 \
\cf5 \cb3 \strokec5 -\cf0 \strokec4  \cf2 \strokec2 `length`\cf0 \strokec4 : Distance (meters)\cb1 \
\cf5 \cb3 \strokec5 -\cf0 \strokec4  \cf2 \strokec2 `compass`\cf0 \strokec4 : Bearing (degrees)\cb1 \
\cf5 \cb3 \strokec5 -\cf0 \strokec4  \cf2 \strokec2 `clino`\cf0 \strokec4 : Inclination (degrees)\cb1 \
\cf5 \cb3 \strokec5 -\cf0 \strokec4  \cf2 \strokec2 `left`\cf0 \strokec4 , \cf2 \strokec2 `right`\cf0 \strokec4 , \cf2 \strokec2 `up`\cf0 \strokec4 , \cf2 \strokec2 `down`\cf0 \strokec4 : Passage dimensions (meters)\cb1 \
\
}