# README.md
# IIASA Macroeconomic ABM Results Analysis

This repository contains a refactored codebase for visualizing and analyzing the IIASA macroeconomic Agent-Based Model (ABM). The code processes data from various disaster scenarios and creates visualizations to compare their economic impacts.

## Project Structure

The codebase is organized as follows:

```
project/
├── main.py                   # Main script that orchestrates the process
├── constants.py              # Constants and reference data
├── data_processing/          # Data processing modules
│   ├── __init__.py
│   ├── loaders.py            # Data loading functions
│   └── aggregation.py        # Data aggregation functions
└── visualization/            # Visualization modules
    ├── __init__.py
    ├── config.py             # Plot configuration classes
    ├── maps.py               # Map plotting functions
    ├── time_series.py        # Time series plotting functions  
    ├── pie_charts.py         # Pie/donut chart functions
    └── utils.py              # Utility functions
```

## Key Features

- Modular, maintainable code structure
- Memory-optimized data processing for large datasets
- Vectorized operations for improved performance
- Reusable visualization components
- Consistent styling across different visualization types

## Visualizations

The code generates several types of visualizations:

1. **Time Series Plots**: Economic indicators over time for each country
2. **Spatial Maps**: Choropleth maps showing economic impacts across countries
3. **Broken Donut Charts**: Sectoral economic changes visualized with donut charts
4. **Combined Visualizations**: Maps with embedded sector-specific visualizations

## Usage

Run the main script to generate all visualizations:

```bash
python main.py
```

You can configure which scenarios to analyze and what type of visualizations to generate by modifying the parameters in `main.py`.

## Data Requirements

The code expects MAT files with specific structures in the `data/IIASA_ABM/2024-06-11/` directory:

- `No_Shock_1_100_MC_30.mat`: Baseline scenario
- `Drought_Q1_1_100_MC_30.mat`: Drought scenario
- `Flood_Q1_1_100_MC_30.mat`: Flood scenario
- `Earthquake_Q1_1_100_MC_30.mat`: Earthquake scenario
- `FL_Q1_EQ_Q5_1_100_MC_30.mat`: Consecutive flood-earthquake scenario
- `EQ_Q1_FL_Q5_1_100_MC_30.mat`: Consecutive earthquake-flood scenario

Additionally, map shapefiles should be present in `data/ne_110m_admin_0_countries/` for the geospatial visualizations.

## Performance Optimizations

This codebase includes several optimizations compared to the original:

1. **Vectorized operations** using NumPy for faster data processing
2. **Cached sector mappings** to avoid redundant calculations
3. **On-demand file loading** to reduce memory usage
4. **Modular visualization functions** to eliminate code duplication
5. **Consistent configuration** for all visualization types

## Dependencies

- NumPy
- Pandas
- Matplotlib
- GeoPandas
- SciPy
- Seaborn
