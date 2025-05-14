# visualization/time_series.py
"""
Functions for creating time series plots in the IIASA ABM analysis.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

def create_time_series_plots(base, scenarios, scenarios_dif_rel, 
                            scenarios_names, scenarios_colors, scenarios_linest,
                            config, country_codes, time_steps, show_plots=False):
    """
    Create time series plots for all countries.
    
    Args:
        base (dict): Baseline data
        scenarios (list): List of scenario data dictionaries
        scenarios_dif_rel (list): List of dictionaries with relative differences
        scenarios_names (list): List of scenario names
        scenarios_colors (list): List of scenario colors
        scenarios_linest (list): List of scenario line styles
        config (PlotConfig): Plot configuration
        country_codes (list): List of country codes
        time_steps (list): List of time steps
        show_plots (bool, optional): Whether to display plots interactively
        
    Returns:
        None
    """
    figdir = config.get_figure_dir('timeseries')
    plot_types = ['abs', 'dif_rel']
    num_countries = len(country_codes)
    
    for plot_type in plot_types:
        # Skip if file already exists
        filename = f'timeseries_{config.thing}_as_{plot_type}'
        if not config.should_plot_file('timeseries', filename):
            continue
            
        # Create figure and grid of subplots
        nrows = 6
        ncols = 5
        subfig_size = [2.5, 2]
        fig, axes = plt.subplots(
            nrows=nrows, 
            ncols=ncols, 
            figsize=(subfig_size[0]*ncols, subfig_size[1]*nrows)
        )
        fig.suptitle(f"{config.thing} as {plot_type}")
        fig.subplots_adjust(hspace=0.5, wspace=0.5)
        
        # Find min/max values for consistent y-axis scaling
        if plot_type == 'dif_rel':
            max_val = 0
            min_val = 0
            for s in range(len(scenarios)):
                max_val = max(max_val, np.max(scenarios_dif_rel[s][config.thing]))
                min_val = min(min_val, np.min(scenarios_dif_rel[s][config.thing]))
        
        # Plot data for each country
        row = 0
        col = 0
        for index, code in enumerate(country_codes):
            if col == ncols:
                row += 1
                col = 0
                
            ax = axes[row, col]
            
            # Plot baseline for absolute values
            if plot_type == 'abs':
                ax.plot(base[config.thing][:, index], label='Baseline', color='k')
            
            # Plot each scenario
            for s in range(len(scenarios)):
                if plot_type == 'abs':
                    ax.plot(
                        scenarios[s][config.thing][:, index], 
                        label=scenarios_names[s],
                        color=scenarios_colors[s],
                        linestyle=scenarios_linest[s]
                    )
                elif plot_type == 'dif_rel':
                    ax.plot(
                        scenarios_dif_rel[s][config.thing][:, index], 
                        label=scenarios_names[s],
                        color=scenarios_colors[s],
                        linestyle=scenarios_linest[s]
                    )
                    ax.set_ylim(min_val, max_val)
            
            # Set labels
            ax.set_title(f'{code}')
            ax.set_xlabel('Quarter')
            ax.set_ylabel(config.thing)
            col += 1
        
        # Add legend
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='lower right', prop={'size': 18})
        
        # Hide unused subplots
        for index in range(num_countries, nrows*ncols):
            if col == ncols:
                row += 1
                col = 0
            axes[row, col].axis('off')
            col += 1
        
        # Adjust layout and save figure
        plt.tight_layout()
        
        if show_plots:
            plt.show()
        
        # Save figure in multiple formats
        fig.savefig(config.get_filepath('timeseries', filename, file_format='png'), dpi=300)
        fig.savefig(config.get_filepath('timeseries', filename, file_format='pdf'))
        
        plt.close(fig)
