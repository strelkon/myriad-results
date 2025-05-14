# main.py (debugging added)
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
    sectors_nace_62, sectors_nace_1, danube_countries
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
                        default=['earthquake'], #'drought', 'flood', 'consecutive flood earthquake', 'consecutive earthquake flood'
                        help='Names of scenarios to analyze (first is baseline)')
    parser.add_argument('--scenario-files', type=str, nargs='+',
                        default=['S0_Sc10000_C0_2023Q4', 'S2_Sc10000_C0_2023Q4'],
                        help='File names of scenarios (without .mat extension)')
    parser.add_argument('--data-dir', type=str, default='data',
                       help='Directory containing the data files (default: data)')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode with extra logging')
    
    return parser.parse_args()

def debug_print(message, debug_enabled=False):
    """Print debug message if debug mode is enabled."""
    if debug_enabled:
        print(f"DEBUG: {message}")

def inspect_data(data, name, keys_to_show=None, debug_enabled=False):
    """
    Print debug information about a data dictionary.
    
    Args:
        data (dict): Data dictionary to inspect
        name (str): Name of the data for logging
        keys_to_show (list, optional): List of keys to show (if None, show all)
        debug_enabled (bool): Whether debug mode is enabled
    """
    if not debug_enabled:
        return
    
    print(f"\nDEBUG: Inspecting {name} data:")
    print(f"  - Number of keys: {len(data.keys())}")
    
    if keys_to_show is None:
        keys_to_show = list(data.keys())
    
    for key in keys_to_show:
        if key in data:
            if isinstance(data[key], np.ndarray):
                print(f"  - {key}: ndarray with shape {data[key].shape}, dtype {data[key].dtype}")
            else:
                print(f"  - {key}: {type(data[key])}")
        else:
            print(f"  - {key}: Not present")

def main():
    """Main function to run the analysis."""
    try:
        # Parse command line arguments
        args = parse_arguments()
        debug_enabled = args.debug
        
        if debug_enabled:
            print("\nDEBUG MODE ENABLED - Extra logging will be shown\n")
        
        print('Starting IIASA ABM Results Analysis')
        debug_print(f"Command line arguments: {args}", debug_enabled)
        
        # Validate inputs
        if len(args.scenario_files) < 2:
            raise ValueError("At least two scenario files are required (baseline and one shock scenario)")
        
        if len(args.scenario_names) != len(args.scenario_files) - 1:
            print(f"Warning: Number of scenario names ({len(args.scenario_names)}) doesn't match number of shock files ({len(args.scenario_files) - 1})")
            print("Using default scenario names for any missing names")
            default_names = ['scenario_' + str(i+1) for i in range(len(args.scenario_files) - 1)]
            # Extend with default names if too few names provided
            if len(args.scenario_names) < len(args.scenario_files) - 1:
                args.scenario_names.extend(default_names[len(args.scenario_names):])
            # Truncate if too many names provided    
            args.scenario_names = args.scenario_names[:len(args.scenario_files) - 1]
        
        # Base configuration
        config = PlotConfig(
            thing='real_output_mean',
            sector_thing='real_sector_output_mean_nace1',
            plot_type='dif_rel',
            base_dir=args.output_dir
        )
        
        # Colors and line styles for scenarios
        default_colors = ["black", "indianred"] # "orange", "deepskyblue", , "purple", "brown", "darkgreen", "pink", "gray", "olive"
        default_linestyles = ["-", "-"]
        
        # Ensure we have enough colors and line styles
        if len(args.scenario_names) > len(default_colors):
            # Repeat the last color for additional scenarios
            default_colors.extend([default_colors[-1]] * (len(args.scenario_names) - len(default_colors)))
        
        if len(args.scenario_names) > len(default_linestyles):
            # Repeat the last line style for additional scenarios
            default_linestyles.extend([default_linestyles[-1]] * (len(args.scenario_names) - len(default_linestyles)))
        
        # Load base scenario data (always the first file)
        print('Loading data')
        base = load_scenario_data(args.scenario_files[0], args.data_dir)
        
        # Debug info for base data
        inspect_data(base, "Base scenario", 
                   keys_to_show=['real_output', 'real_output_mean', 'real_sector_output', 'real_sector_output_mean'],
                   debug_enabled=debug_enabled)
        
        # Load the shock scenarios
        scenarios = []
        scenarios_names = []
        scenarios_colors = []
        scenarios_linest = []
        
        # Start from index 1 (skip baseline)
        for i in range(1, len(args.scenario_files)):
            try:
                scen_data = load_scenario_data(args.scenario_files[i], args.data_dir)
                scenarios.append(scen_data)
                scenarios_names.append(args.scenario_names[i-1])  # Adjust index for scenario names
                scenarios_colors.append(default_colors[i-1])
                scenarios_linest.append(default_linestyles[i-1])
                
                # Debug info for scenario data
                inspect_data(scen_data, f"Scenario {args.scenario_names[i-1]}",
                           keys_to_show=['real_output', 'real_output_mean', 'real_sector_output', 'real_sector_output_mean'],
                           debug_enabled=debug_enabled)
            except Exception as e:
                print(f"Error loading scenario {args.scenario_files[i]}: {str(e)}")
                print("Skipping this scenario")
        
        if not scenarios:
            raise ValueError("No valid shock scenarios could be loaded")
        
        # Debug info for important arrays
        if debug_enabled:
            print("\nDEBUG: Key array shapes before processing:")
            if 'real_sector_output' in base:
                print(f"  - Base real_sector_output shape: {base['real_sector_output'].shape}")
            if 'real_sector_output_mean' in base:
                print(f"  - Base real_sector_output_mean shape: {base['real_sector_output_mean'].shape}")
            print(f"  - NACE 62 sectors count: {len(sectors_nace_62)}")
            print(f"  - NACE 1 sectors count: {len(sectors_nace_1)}")
            print(f"  - Time steps count: {len(time_steps)}")
            print(f"  - Countries count: {len(country_codes)}")
        
        # Calculate means, differences to baseline, aggregate sectors
        print('Calculating means and aggregating sectors')
        scenarios_rel, scenarios_dif, scenarios_dif_rel = calculate_means_and_differences(
            base, scenarios, sectors_nace_1, sectors_nace_62, time_steps
        )
        
        # Debug info after calculation
        if debug_enabled:
            print("\nDEBUG: After calculations:")
            if 'real_sector_output_mean_nace1' in base:
                print(f"  - Base real_sector_output_mean_nace1 shape: {base['real_sector_output_mean_nace1'].shape}")
            
            # Check calculated differences
            if len(scenarios_dif_rel) > 0:
                for key in ['real_output_mean', 'real_sector_output_mean_nace1']:
                    if key in scenarios_dif_rel[0]:
                        print(f"  - scenarios_dif_rel[0][{key}] shape: {scenarios_dif_rel[0][key].shape}")
                    else:
                        print(f"  - scenarios_dif_rel[0][{key}] not found")
        
        # Update config with calculated data
        config.update_scenario_data(scenarios_dif_rel)
        
        # Check if required variables exist before proceeding
        required_vars = ['real_output_mean', 'real_sector_output_mean_nace1']
        missing_vars = [var for var in required_vars if var not in base]
        
        if missing_vars:
            print(f"Warning: The following required variables are missing: {missing_vars}")
            print("Some visualizations may not work correctly")
        
        # Load map data
        print('Loading map')
        try:
            europe = load_map_data()
        except FileNotFoundError as e:
            print(f"Warning: Could not load map data: {str(e)}")
            print("Map visualizations will be skipped")
            europe = None
        
        # Create time series plots
        print('Plotting time series')
        create_time_series_plots(
            base, scenarios, scenarios_dif_rel, 
            scenarios_names, scenarios_colors, scenarios_linest,
            config, country_codes, time_steps, args.show_plots
        )
        
        # Skip map visualizations if map data couldn't be loaded
        if europe is not None:
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
            
            # Create maps with inset charts (only for first scenario)
            print('Plotting maps with broken donuts')
            inset_type = 'brokendonut'
            create_map_with_insets(
                base, scenarios_dif_rel, europe,
                config, scenarios_names, [0],  # Only plot first scenario for this visualization
                country_codes, country_codes_3, time_steps,
                inset_type, args.show_plots
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
        
        print('Analysis complete')
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
