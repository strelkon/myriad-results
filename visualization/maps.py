# visualization/maps.py
"""
Functions for creating map visualizations in the IIASA ABM analysis.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib.patheffects as path_effects
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from constants import sectors_nace_1, sectors_nace_1_colors, sectors_nace_62, sectors_nace_62_colors

def create_map_plots(base, scenarios_dif_rel, europe, 
                    config, scenarios_names, scenarios_to_plot, 
                    country_codes, country_codes_3, time_steps, show_plots=False):
    """
    Create spatial map visualizations.
    
    Args:
        base (dict): Baseline data
        scenarios_dif_rel (list): List of dictionaries with relative differences
        europe (GeoDataFrame): Map data for Europe
        config (PlotConfig): Plot configuration
        scenarios_names (list): List of scenario names
        scenarios_to_plot (list): List of scenario indices to plot
        country_codes (list): List of country codes
        country_codes_3 (list): List of 3-letter country codes
        time_steps (list): List of time steps
        show_plots (bool, optional): Whether to display plots interactively
        
    Returns:
        None
    """
    # Setup parameters
    subfig_size = (15, 15)
    nrows = 3
    ncols = 5
    plot_type = config.plot_type
    
    # Iterate through scenarios to plot
    for scenario_index in scenarios_to_plot:
        # Skip if file already exists
        filename = f'map-{config.thing}_in_{scenarios_names[scenario_index]}_scenario_as_{plot_type}'
        scenario_dir = config.get_figure_dir('maps', scenarios_names[scenario_index])
        
        if not config.should_plot_file('maps', filename):
            continue
            
        # Create dataframe for plotting
        if plot_type == 'abs':
            thing_df = pd.DataFrame({
                'time': np.repeat(time_steps, len(country_codes)),
                'country': country_codes_3 * len(time_steps),
                config.thing: base[config.thing].flatten()
            })
        else:  # dif_rel
            thing_df = pd.DataFrame({
                'time': np.repeat(time_steps, len(country_codes)),
                'country': country_codes_3 * len(time_steps),
                config.thing: scenarios_dif_rel[scenario_index][config.thing].flatten()
            })
        
        # Initialize figure
        fig, axes = plt.subplots(
            nrows, 
            ncols, 
            figsize=(subfig_size[0]*ncols, subfig_size[1]*nrows)
        )
        fig.suptitle(f"{config.thing} in {scenarios_names[scenario_index]} scenario as {plot_type}")
        
        # Plot each time step
        row = 0
        col = 0
        for index, timestep in enumerate(time_steps[1:]):  # Skip first time step
            # Filter data for current time step
            thing_df_1 = thing_df[thing_df['time'] == timestep]
            merged_data = europe.merge(thing_df_1, how='left', left_on='ADM0_A3', right_on='country')
            
            # Determine subplot position
            if col == ncols:
                row += 1
                col = 0
            
            if row >= nrows or col >= ncols:
                break
                
            if ncols > 1:
                ax = axes[row, col]
            else:
                ax = axes[row]
                
            col += 1
            
            # Define colors and normalization
            if plot_type == 'abs':
                cmap = config.cmap_abs
                min_val, max_val = min(thing_df[config.thing]), max(thing_df[config.thing])
            else:  # dif_rel
                cmap = config.cmap_rel
                min_val, max_val = config.min_val, config.max_val
                
            norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
            
            # Create the map plot
            merged_data.plot(
                column=config.thing, 
                cmap=cmap, 
                norm=norm,
                edgecolor='black', 
                linewidth=0.2,
                ax=ax
            )
            
            # Set map boundaries and disable axis
            ax.set_xlim(-15, 35)
            ax.set_ylim(32, 72)
            ax.axis('off')
            
            # Add color legend
            ax_lgd = inset_axes(
                ax, 
                width=subfig_size[0]*0.02, 
                height=subfig_size[1]*0.2, 
                loc='right'
            )
            norm_lgd = mcolors.Normalize(vmin=min_val*100, vmax=max_val*100)
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_lgd)
            
            plt.colorbar(
                sm,
                cax=ax_lgd,
                location='left',
                shrink=0.01,
                label='change relative to baseline',
                format="%+.0f %%"
            )
            
            # Set title
            ax.title.set_text(timestep)
            
            # Save individual subplot
            timestep_filename = f'map-{config.sector_thing}_in_{scenarios_names[scenario_index]}_scenario_as_{plot_type}_time_step_ {timestep}'
            
            # Save with tight bounding box around the subplot
            bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(1.04, 1.06)
            
            fig.savefig(
                os.path.join(scenario_dir, f'{timestep_filename}.png'),
                dpi=300,
                bbox_inches=bbox
            )
            
            fig.savefig(
                os.path.join(scenario_dir, f'{timestep_filename}.pdf'),
                bbox_inches=bbox
            )
        
        # Hide unused subplots
        for index in range(len(time_steps), nrows*ncols):
            if col == ncols:
                row += 1
                col = 0
            axes[row, col].axis('off')
            col += 1
        
        # Display the plot if requested
        plt.tight_layout()
        if show_plots:
            plt.show()
        
        # Save the complete figure
        fig.savefig(
            config.get_filepath('maps', filename, file_format='png'),
            dpi=300
        )
        
        fig.savefig(
            config.get_filepath('maps', filename, file_format='pdf')
        )
        
        plt.close(fig)

def create_map_with_insets(base, scenarios_dif_rel, europe,
                          config, scenarios_names, scenarios_to_plot,
                          country_codes, country_codes_3, time_steps,
                          inset_type, show_plots=False):
    """
    Create map visualizations with inset charts for each country.
    
    Args:
        base (dict): Baseline data
        scenarios_dif_rel (list): List of dictionaries with relative differences
        europe (GeoDataFrame): Map data for Europe
        config (PlotConfig): Plot configuration
        scenarios_names (list): List of scenario names
        scenarios_to_plot (list): List of scenario indices to plot
        country_codes (list): List of country codes
        country_codes_3 (list): List of 3-letter country codes
        time_steps (list): List of time steps
        inset_type (str): Type of inset chart ('brokendonut' or 'stackedbar')
        show_plots (bool, optional): Whether to display plots interactively
        
    Returns:
        None
    """
    from visualization.pie_charts import addBrokenDonutPlot, addRelChangeStackedBarPlot
    
    # Setup parameters
    subfig_size = (15, 15)
    insetfig_size = min(subfig_size) * 0.15
    plot_type = config.plot_type
    
    # Configure plot settings
    base_dir = f'maps-{inset_type}'
    
    for scenario_index in scenarios_to_plot:
        scenario_dir = config.get_figure_dir(base_dir, scenarios_names[scenario_index])
        
        # Iterate through time steps
        for time_index, timestep in enumerate(time_steps):
            # Skip if file already exists
            filename = f'{inset_type}-{config.sector_thing}_in_{scenarios_names[scenario_index]}_scenario_as_{plot_type}_time_ {timestep}'
            
            if not config.should_plot_file(base_dir, filename, scenarios_names[scenario_index]):
                continue
                
            print(f'Running scenario {scenarios_names[scenario_index]} for time {timestep}')
            
            # Create dataframe for the map
            if plot_type == 'abs':
                thing_df = pd.DataFrame({
                    'time': np.repeat(time_steps, len(country_codes)),
                    'country': country_codes_3 * len(time_steps),
                    config.thing: base[config.thing].flatten()
                })
            else:  # dif_rel
                thing_df = pd.DataFrame({
                    'time': np.repeat(time_steps, len(country_codes)),
                    'country': country_codes_3 * len(time_steps),
                    config.thing: scenarios_dif_rel[scenario_index][config.thing].flatten()
                })
            
            # Initialize figure
            nrows = 3
            ncols = 5
            fig, axes = plt.subplots(
                nrows, 
                ncols, 
                figsize=(subfig_size[0]*ncols, subfig_size[1]*nrows)
            )
            plt.tight_layout()
            fig.suptitle(f"{config.thing} in {scenarios_names[scenario_index]} scenario as {plot_type}")
            
            # Determine subplot position
            row, col = 0, 0
            if col == ncols:
                row += 1
                col = 0
            
            if ncols > 1:
                ax = axes[row, col]
            else:
                ax = axes[row]
                
            col += 1
            
            # Define colors and normalization
            cmap = config.get_colormap()
            norm = mcolors.Normalize(vmin=config.min_val, vmax=config.max_val)
            
            # Create the map
            thing_df_1 = thing_df[thing_df['time'] == timestep]
            merged_data = europe.merge(thing_df_1, how='left', left_on='ADM0_A3', right_on='country')
            
            merged_data.plot(
                column=config.thing, 
                cmap=cmap, 
                norm=norm,
                edgecolor='black', 
                linewidth=0.2,
                ax=ax
            )
            
            # Set map boundaries and disable axis
            ax.set_xlim(-10, 35)
            ax.set_ylim(32, 67)
            ax.axis('off')
            
            # Add arrows for specific countries with insets
            arrow_adjustments = {
                'BEL': {'end_offset': [-0, -1.9], 'style': "arc3,rad=-.3"},
                'LUX': {'end_offset': [1.3, -1.3], 'style': "arc3,rad=-.3"},
                'SVN': {'end_offset': [1.9, 0], 'style': "arc3,rad=-.6"},
                'SVK': {'end_offset': [-1.3, -1.3], 'style': "arc3,rad=.1"}
            }
            
            for country, adjust in arrow_adjustments.items():
                start_x = europe['LABEL_X'][europe['ADM0_A3'] == country].iloc[0]
                start_y = europe['LABEL_Y'][europe['ADM0_A3'] == country].iloc[0]
                
                end_x = europe['INSET_FIG_X'][europe['ADM0_A3'] == country].iloc[0] + adjust['end_offset'][0]
                end_y = europe['INSET_FIG_Y'][europe['ADM0_A3'] == country].iloc[0] + adjust['end_offset'][1]
                
                ax.add_patch(
                    patches.FancyArrowPatch(
                        (start_x, start_y),
                        (end_x, end_y),
                        color='k', 
                        linewidth=0.2,
                        connectionstyle=adjust['style']
                    )
                )
            
            # Add inset plots for each country
            for country_index in range(len(country_codes)):
                print(f'   Making inset {country_codes_3[country_index]}')
                
                # Create inset axes
                inset_x = europe[europe['ADM0_A3'] == country_codes_3[country_index]]['INSET_FIG_X']
                inset_y = europe[europe['ADM0_A3'] == country_codes_3[country_index]]['INSET_FIG_Y']
                
                ax_sub = inset_axes(
                    ax, 
                    width=insetfig_size, 
                    height=insetfig_size, 
                    loc=10,
                    bbox_to_anchor=(inset_x, inset_y),
                    bbox_transform=ax.transData
                )
                
                # Get sector data
                piedata = base[config.sector_thing][time_index, country_index, :]
                
                # Add appropriate chart type
                if inset_type == 'brokendonut':
                    addBrokenDonutPlot(
                        piedata, 
                        ax_sub, 
                        sectors_dif_rel=scenarios_dif_rel[scenario_index][config.sector_thing],
                        time_index=time_index, 
                        country_index=country_index, 
                        config=config, 
                        halo=True
                    )
                    text = ax_sub.text(0, 0, country_codes[country_index], color='gray', ha='center', va='center', weight='bold')
                else:  # stackedbar
                    addRelChangeStackedBarPlot(
                        piedata,
                        scenarios_dif_rel[scenario_index][config.sector_thing][time_index, country_index, :],
                        ax_sub
                    )
                    text = ax_sub.text(0.3, 0, country_codes[country_index], color='gray', ha='center', va='center', weight='bold')
                
                # Add text shadow effect
                text.set_path_effects([
                    path_effects.Stroke(linewidth=3, foreground='white', alpha=0.8),
                    path_effects.Normal()
                ])
            
            # Add color legend
            ax_lgd = inset_axes(
                ax,
                width=subfig_size[0]*0.04,
                height=subfig_size[1]*0.4,
                loc='right'
            )
            
            norm_lgd = mcolors.Normalize(vmin=config.min_val*100, vmax=config.max_val*100)
            sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_lgd)
            
            plt.colorbar(
                sm,
                cax=ax_lgd,
                location='left',
                shrink=0.01,
                label='change relative to baseline',
                format="%+.0f %%"
            )
            
            # Set title
            ax.title.set_text(timestep)
            
            # Add scale lines legend
            add_scale_legend(ax, config)
            
            # Add sector color legend
            add_sector_legend(ax, piedata)
            
            # Save just the subplot
            fig.savefig(
                os.path.join(scenario_dir, f'map-{plot_type}-{config.sector_thing}_in_{scenarios_names[scenario_index]}_scenario_as_{plot_type}_time_step_ {timestep}.png'),
                dpi=300,
                bbox_inches=ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(1.03, 1.06)
            )
            
            fig.savefig(
                os.path.join(scenario_dir, f'map-{plot_type}-{config.sector_thing}_in_{scenarios_names[scenario_index]}_scenario_as_{plot_type}_time_step_ {timestep}.pdf'),
                bbox_inches=ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted()).expanded(1.03, 1.06)
            )
            
            # Hide unused subplots
            for index in range(len(time_steps), nrows*ncols):
                if col == ncols:
                    row += 1
                    col = 0
                axes[row, col].axis('off')
                col += 1
            
            # Display the plot if requested
            if show_plots:
                plt.show()
            
            # Save the complete figure
            base_figdir = config.get_figure_dir(base_dir)
            
            fig.savefig(
                os.path.join(base_figdir, f'map-{plot_type}-{config.sector_thing}_in_{scenarios_names[scenario_index]}_scenario_as_{plot_type}.png'),
                dpi=300
            )
            
            fig.savefig(
                os.path.join(base_figdir, f'map-{plot_type}-{config.sector_thing}_in_{scenarios_names[scenario_index]}_scenario_as_{plot_type}.pdf')
            )
            
            plt.close(fig)

def add_scale_legend(ax, config):
    """
    Add scale legend to the map for broken donut visualizations.
    
    Args:
        ax (Axes): Matplotlib axes object
        config (PlotConfig): Plot configuration
    """
    insetfig_size = 3
    ax_sub = inset_axes(
        ax, 
        width=insetfig_size, 
        height=insetfig_size, 
        loc=10,
        bbox_to_anchor=(ax.get_xlim()[0]+3, ax.get_ylim()[1]-5),
        bbox_transform=ax.transData
    )
    
    ax_sub.title.set_text('Relative Change')
    limits = config.base_radius*(1+.09*config.rel_change_scaling)
    ax_sub.set_xlim(-limits, limits)
    ax_sub.set_ylim(-limits, limits)
    ax_sub.axis('off')
    
    # Add scale lines
    scale_lines = [
        {'radius': -0.1, 'style': '--', 'color': 'gray', 'width': 1, 'label': '-10%'},
        {'radius': -0.05, 'style': ':', 'color': 'gray', 'width': 1, 'label': '-5%'},
        {'radius': 0, 'style': '-', 'color': 'k', 'width': 1, 'label': ''},
        {'radius': 0.05, 'style': ':', 'color': 'gray', 'width': 1, 'label': '+5%'}
    ]
    
    text_kwargs = dict(facecolor='white', linewidth=0, pad=1)
    
    for line in scale_lines:
        radius = config.base_radius * (1 + line['radius'] * config.rel_change_scaling)
        circle = plt.Circle(
            (0, 0), 
            radius, 
            linestyle=line['style'],
            fill=False, 
            edgecolor=line['color'], 
            linewidth=line['width']
        )
        ax_sub.add_patch(circle)
        
        if line['label']:
            txt = ax_sub.text(
                0, 
                radius,
                line['label'],
                fontsize=10,
                backgroundcolor='white',
                color=line['color'],
                horizontalalignment='center',
                verticalalignment='center'
            )
            txt.set_bbox(text_kwargs)

def add_sector_legend(ax, piedata):
    """
    Add sector legend to the map.
    
    Args:
        ax (Axes): Matplotlib axes object
        piedata (ndarray): Base pie chart data
    """
    insetfig_size = 3
    ax_sub = inset_axes(
        ax, 
        width=insetfig_size, 
        height=insetfig_size, 
        loc=10,
        bbox_to_anchor=(ax.get_xlim()[0]+10, ax.get_ylim()[1]-5),
        bbox_transform=ax.transData
    )
    
    # Determine which sector classification is being used
    if len(piedata) == len(sectors_nace_1):
        sector_colors = sectors_nace_1_colors
        sector_names = sectors_nace_1
    else:
        sector_colors = sectors_nace_62_colors
        sector_names = sectors_nace_62
    
    # Create pie chart as legend
    wedges, texts = ax_sub.pie(
        np.ones(len(piedata)), 
        colors=sector_colors, 
        labels=sector_names,
        wedgeprops={"edgecolor": "k", "linewidth": 0.5}, 
        counterclock=False, 
        startangle=-270
    )
    
    ax_sub.title.set_text('Sectors')
