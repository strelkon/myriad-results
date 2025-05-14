# main.py (updated)
#!/usr/bin/env python
# coding: utf-8

"""
IIASA ABM Results Analysis and Visualization
Main script that orchestrates the data loading, processing, and visualization.
"""

import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from data_processing.loaders import load_scenario_data, load_map_data
from data_processing.aggregation import calculate_means_and_differences, aggregateSectorNace62ToNace1
from visualization.config import PlotConfig
from visualization.time_series import create_time_series_plots
from visualization.maps import create_map_plots, create_map_with_insets
from visualization.pie_charts import create_pie_charts_by_country, create_pie_charts_by_time

# Constants and settings
from constants import (
    country_codes, country_codes_3, time_steps, experiments, 
    sectors_nace_62, sectors_nace_1, danube_countries, danube_nuts_2
)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='IIASA ABM Results Analysis')
    
    # Add arguments
    parser.add_argument('--output-dir', type=str, default='figures',
                       help='Base output directory for figures (default: figures)')
    parser.add_argument('--show-plots', action='store_true',
                       help='Show plots interactively')
    parser.add_argument('--scenario-names', type=str, nargs='+', 
                        default=['drought', 'flood', 'earthquake', 'consecutive flood earthquake', 'consecutive earthquake flood'],
                        help='Names of scenarios to analyze (first is baseline)')
    parser.add_argument('--scenario-files', type=str, nargs='+',
                        default=['No_Shock_1_100_MC_30', 'Drought_Q1_1_100_MC_30', 'Flood_Q1_1_100_MC_30', 
                                'Earthquake_Q1_1_100_MC_30', 'FL_Q1_EQ_Q5_1_100_MC_30', 'EQ_Q1_FL_Q5_1_100_MC_30'],
                        help='File names of scenarios (without .mat extension)')
    
    return parser.parse_args()

def main():
    """Main function to run the analysis."""
    # Parse command line arguments
    args = parse_arguments()
    
    print('Starting IIASA ABM Results Analysis')
    
    # Base configuration
    config = PlotConfig(
        thing='real_output_mean',
        sector_thing='real_sector_output_mean_nace1',
        plot_type='dif_rel',
        base_dir=args.output_dir
    )
    
    # Colors and line styles for scenarios
    default_colors = ["green", "orange", "deepskyblue", "indianred", "purple", "brown", "darkgreen", "pink", "gray", "olive"]
    default_linestyles = ["-", "-", "-", "-", "-", "--", "--", "--", "--", "--"]
    
    # Ensure we have enough colors and line styles
    if len(args.scenario_names) > len(default_colors):
        # Repeat the last color for additional scenarios
        default_colors.extend([default_colors[-1]] * (len(args.scenario_names) - len(default_colors)))
    
    if len(args.scenario_names) > len(default_linestyles):
        # Repeat the last line style for additional scenarios
        default_linestyles.extend([default_linestyles[-1]] * (len(args.scenario_names) - len(default_linestyles)))
    
    # Load base scenario data (always the first file)
    print('Loading data')
    base = load_scenario_data(args.scenario_files[0])
    
    # Load the shock scenarios
    scenarios = []
    scenarios_names = []
    scenarios_colors = []
    scenarios_linest = []
    
    # Start from index 1 (skip baseline)
    for i in range(1, len(args.scenario_files)):
        scenarios.append(load_scenario_data(args.scenario_files[i]))
        scenarios_names.append(args.scenario_names[i-1])  # Adjust index for scenario names
        scenarios_colors.append(default_colors[i-1])
        scenarios_linest.append(default_linestyles[i-1])
    
    # Calculate means, differences to baseline, aggregate sectors
    print('Calculating means and aggregating sectors')
    scenarios_rel, scenarios_dif, scenarios_dif_rel = calculate_means_and_differences(
        base, scenarios, sectors_nace_1, sectors_nace_62, time_steps
    )
    
    # Update config with calculated data
    config.update_scenario_data(scenarios_dif_rel)
    
    # Load map data
    print('Loading map')
    europe = load_map_data()
    
    # Create time series plots
    print('Plotting time series')
    create_time_series_plots(
        base, scenarios, scenarios_dif_rel, 
        scenarios_names, scenarios_colors, scenarios_linest,
        config, country_codes, time_steps, args.show_plots
    )
    
    # Decide which scenarios to plot maps for
    # By default, plot all scenarios, but limit to first 4 if there are many
    scenarios_to_plot = list(range(min(len(scenarios), 4)))
    
    # Create map plots
    print('Plotting maps')
    create_map_plots(
        base, scenarios_dif_rel, europe, 
        config, scenarios_names, scenarios_to_plot, 
        country_codes, country_codes_3, time_steps, args.show_plots
    )
    
    # Create pie charts by country
    print('Plotting broken donuts by country')
    create_pie_charts_by_country(
        base, scenarios_dif_rel, config, 
        country_codes, country_codes_3,
        scenarios_names, time_steps, args.show_plots
    )
    
    # Create pie charts by time
    print('Plotting broken donuts by time')
    create_pie_charts_by_time(
        base, scenarios_dif_rel, config,
        country_codes, scenarios_names, time_steps, args.show_plots
    )
    
    # Create maps with inset charts (only for first scenario)
    print('Plotting maps with broken donuts')
    inset_type = 'brokendonut'
    create_map_with_insets(
        base, scenarios_dif_rel, europe,
        config, scenarios_names, [0],  # Only plot first scenario for this visualization
        country_codes, country_codes_3, time_steps,
        inset_type, args.show_plots
    )
    
    print('Analysis complete')

if __name__ == "__main__":
    main()
