# data_processing/loaders.py (updated)
"""
Functions for loading and preparing data for the IIASA ABM analysis.
"""

import os
from scipy.io import loadmat
import numpy as np
import pandas as pd
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt

def load_scenario_data(scenario_name, data_dir='data'):
    """
    Load a specific scenario data file.
    
    Args:
        scenario_name (str): Name of the scenario file (without .mat extension)
        data_dir (str, optional): Directory containing the data files
        
    Returns:
        dict: Dictionary containing the loaded data
    """
    file_path = f'{data_dir}/{scenario_name}.mat'
    
    # Check if file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Could not find scenario file: {file_path}")
    
    print(f'Loading {scenario_name} data')
    return loadmat(file_path)

def load_map_data(shapefile_path="maps/ne_110m_admin_0_countries.shp"):
    """
    Load and prepare map shape data for visualization.
    
    Args:
        shapefile_path (str, optional): Path to the shapefile
        
    Returns:
        GeoDataFrame: Prepared map data for Europe
    """
    # Check if file exists
    if not os.path.isfile(shapefile_path):
        raise FileNotFoundError(f"Could not find shapefile: {shapefile_path}")
    
    sns.set(style="whitegrid", palette="pastel", color_codes=True)
    sns.mpl.rc("figure", figsize=(10, 6))
    
    # Load world map shapefile
    world = gpd.read_file(shapefile_path)
    
    # Filter and prepare Europe data
    europe = world  # world[world['CONTINENT']=='Europe']
    europe.insert(len(europe.columns), 'INSET_FIG_X', europe['LABEL_X'])
    europe.insert(len(europe.columns), 'INSET_FIG_Y', europe['LABEL_Y'])
    
    # Manually adjust position coordinates for specific countries
    country_adjustments = {
        'LUX': {'x': 0.2, 'y': 52.5},
        'NLD': {'x': 5.8, 'y': 53},
        'BEL': {'x': 2.4, 'y': 56},
        'HRV': {'x': 16.9, 'y': 43.7},
        'AUT': {'x': 12.3, 'y': 47.5},
        'ITA': {'x': 12, 'y': 43.3},
        'LVA': {'x': 21, 'y': 58.2},
        'HUN': {'x': 19.6, 'y': 47.5},
        'ROU': {'x': 24.2, 'y': 46.5},
        'BGR': {'x': 25.5, 'y': 42.1},
        'SVN': {'x': 5, 'y': 40},
        'SVK': {'x': 26, 'y': 50.5},
        'EST': {'x': 25.9, 'y': 59},
        'CZE': {'x': 15.8, 'y': 49.88},
        'POL': {'x': 19.6, 'y': 52},
        'SWE': {'x': 15, 'y': 62}
    }
    
    for country_code, position in country_adjustments.items():
        europe.loc[europe['ADM0_A3'] == country_code, 'INSET_FIG_X'] = position['x']
        europe.loc[europe['ADM0_A3'] == country_code, 'INSET_FIG_Y'] = position['y']
    
    return europe

def shape(listOfLists):
    """
    Find the shape of a nested list as Python is deficient in this area.
    
    Args:
        listOfLists: A (potentially) nested list structure
        
    Returns:
        list: The shape of the nested list structure
    """
    shape_list = []
    b = listOfLists
    while isinstance(b, list):
        shape_list.append(len(b))
        b = b[0]
    return shape_list
