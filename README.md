# Satellite_Conjuction_and_Collision_Risk_Assessment

## Overview
This project analyzes satellite orbits using Two-Line Element (TLE) datasets,
detects potential close approaches, and performs risk assessment with EDA.

## Tech Stack
- Python
- Skyfield (orbital mechanics)
- Pandas, Numpy (data analysis)
- Matplotlib, Seaborn, Plotly (visualizations)

## Project Workflow
1. Load TLE data (`src/load_data.py`)
2. Propagate satellite orbits (`src/orbit_utils.py`)
3. Detect close approaches between satellites
4. Perform EDA (`src/eda_utils.py`)
5. Generate reports and figures (`outputs/`)

## Usage
```bash
pip install -r requirements.txt


## (additional)

##Demo  Streamlit App
   streamlit run main_app.py
   
   """ SIMULATION  For real-time conjunction analysis and collision risk assesment done on  sample 
      12757 satellites(TLE data),
        For the selected satellite with respect to other satellites(if found any in the closest approach)
        displays the result with the graph, or else ends with displaying only eda, orbit data, ground track information."""
