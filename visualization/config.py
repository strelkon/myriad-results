# visualization/config.py (updated)
"""
Configuration classes for visualization settings in the IIASA ABM analysis.
"""

import os
import numpy as np
import matplotlib.cm as cm

class PlotConfig:
    """
    Configuration class to manage plot settings.
    """
    
    def __init__(self, thing, sector_thing, plot_type, base_dir='figures',
                 base_radius=0.5, cmap_rel=cm.coolwarm_r, cmap_abs=cm.BuPu):
        """
        Initialize plot configuration.
        
        Args:
            thing (str): Main variable to plot
            sector_thing (str): Sector variable to plot
            plot_type (str): Type of plot ('abs' or 'dif_rel')
            base_dir (str): Base directory for saving figures
            base_radius (float): Base radius for pie charts
            cmap_rel (colormap): Colormap for relative difference plots
            cmap_abs (colormap): Colormap for absolute value plots
        """
        self.thing = thing
        self.sector_thing = sector_thing
        self.plot_type = plot_type
        self.base_dir = base_dir
        self.base_radius = base_radius
        self.cmap_rel = cmap_rel
        self.cmap_abs = cmap_abs
        self.rel_change_scaling = 5
        self.wedgeprops = {"edgecolor": "k", "linewidth": 0.5}
        
        # Values to be updated later
        self.min_val = 0
        self.max_val = 0
        self.min_sector_val = 0
        self.max_sector_val = 0
    
    def update_scenario_data(self, scenarios_dif_rel):
        """
        Update configuration with calculated scenario data.
        
        Args:
            scenarios_dif_rel (list): List of dictionaries with relative differences
        """
        # Calculate min/max values across all scenarios for consistent visualizations
        for s in range(len(scenarios_dif_rel)):
            if self.thing in scenarios_dif_rel[s]:
                self.max_val = max(self.max_val, np.max(scenarios_dif_rel[s][self.thing]))
                self.min_val = min(self.min_val, np.min(scenarios_dif_rel[s][self.thing]))
            
            if self.sector_thing in scenarios_dif_rel[s]:
                self.max_sector_val = max(self.max_sector_val, np.max(scenarios_dif_rel[s][self.sector_thing]))
                self.min_sector_val = min(self.min_sector_val, np.min(scenarios_dif_rel[s][self.sector_thing]))
        
        # Make the color scale symmetric around zero for relative differences
        self.max_val = max(abs(self.min_val), abs(self.max_val))
        self.min_val = -self.max_val
    
    def get_colormap(self):
        """Get the appropriate colormap based on plot type."""
        return self.cmap_rel if self.plot_type == 'dif_rel' else self.cmap_abs
    
    def get_figure_dir(self, plot_type, subfolder=None):
        """
        Get the figure directory path.
        
        Args:
            plot_type (str): Type of plot (e.g., 'timeseries', 'maps')
            subfolder (str, optional): Subfolder name
            
        Returns:
            str: Path to the figure directory
        """
        path = os.path.join(self.base_dir, plot_type)
        if subfolder:
            path = os.path.join(path, subfolder)
        
        # Create directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
        
        return path
    
    def get_filepath(self, plot_type, filename, subfolder=None, file_format='png'):
        """
        Get the full filepath for saving a figure.
        
        Args:
            plot_type (str): Type of plot (e.g., 'timeseries', 'maps')
            filename (str): Name of the file
            subfolder (str, optional): Subfolder name
            file_format (str, optional): File format (e.g., 'png', 'pdf')
            
        Returns:
            str: Full filepath
        """
        return os.path.join(
            self.get_figure_dir(plot_type, subfolder),
            f"{filename}.{file_format}"
        )
    
    def should_plot_file(self, plot_type, filename, subfolder=None):
        """
        Check if a file already exists and should be skipped.
        
        Args:
            plot_type (str): Type of plot
            filename (str): Name of the file
            subfolder (str, optional): Subfolder name
            
        Returns:
            bool: True if the file should be generated, False if it exists and should be skipped
        """
        filepath = self.get_filepath(plot_type, filename, subfolder)
        
        if os.path.isfile(filepath):
            print(f'Skipping {filename} - file exists.')
            return False
        
        print(f'Plotting {filename}')
        return True
