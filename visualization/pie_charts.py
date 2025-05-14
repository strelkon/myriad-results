# visualization/pie_charts.py
"""
Functions for creating pie and donut chart visualizations in the IIASA ABM analysis.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from constants import sectors_nace_1, sectors_nace_1_colors, sectors_nace_62, sectors_nace_62_colors

def addRelChangePiePlot(piedata, ax, scenarios_dif_rel, scenario_index, time_index, country_index, config):
    """
    Add pie chart with relative change visualization.
    
    Args:
        piedata (ndarray): Base pie chart data
        ax (Axes): Matplotlib axes object
        scenarios_dif_rel (list): List of dictionaries with relative differences
        scenario_index (int): Index of scenario to visualize
        time_index (int): Index of time step
        country_index (int): Index of country
        config (PlotConfig): Plot configuration
    """
    # Add circle scale lines
    ax.add_patch(plt.Circle(
        (0, 0), 
        config.base_radius*(1-0.1*config.rel_change_scaling), 
        linestyle='--',
        fill=False, 
        edgecolor='gray', 
        linewidth=1
    ))
    
    ax.add_patch(plt.Circle(
        (0, 0), 
        config.base_radius*(1-0.05*config.rel_change_scaling), 
        linestyle=':',
        fill=False, 
        edgecolor='gray', 
        linewidth=1
    ))
    
    ax.add_patch(plt.Circle(
        (0, 0), 
        config.base_radius, 
        linestyle='-', 
        fill=False, 
        edgecolor='k'
    ))
    
    ax.add_patch(plt.Circle(
        (0, 0), 
        config.base_radius*(1+0.05*config.rel_change_scaling), 
        linestyle=':',
        fill=False, 
        edgecolor='gray', 
        linewidth=1
    ))

    # Create pie wedges
    for s in range(len(piedata)):
        sector_change = scenarios_dif_rel[scenario_index][config.sector_thing][time_index, country_index, s]
        radius = max(0.000001, config.base_radius + config.rel_change_scaling * sector_change)
        
        wedges, _ = ax.pie(
            piedata, 
            radius=radius,
            colors=sectors_nace_1_colors if len(piedata) == len(sectors_nace_1) else sectors_nace_62_colors, 
            wedgeprops=config.wedgeprops, 
            counterclock=False, 
            startangle=-270
        )
        
        # Show only the current sector wedge
        for wi in range(len(wedges)):
            if wi != s:
                wedges[wi].set_visible(False)

def addBrokenDonutPlot(piedata, ax, sectors_dif_rel, time_index, country_index, config, halo=False):
    """
    Add broken donut chart visualization for relative sector changes.
    
    Args:
        piedata (ndarray): Base pie chart data
        ax (Axes): Matplotlib axes object
        sectors_dif_rel (list): Relative differences for sectors
        time_index (int): Index of time step
        country_index (int): Index of country
        config (PlotConfig): Plot configuration
        halo (bool, optional): Whether to add halo effect to central circle
    """
    # Add circle scale lines
    scale_line_styles = ['--', ':', '-', ':']
    scale_line_widths = [1, 1, 0.1, 1]
    scale_line_radii = [-0.1, -0.05, 0, 0.05]
    scale_line_colors = ['k', 'k', 'k', 'k']
    
    # Create shadow/halo effect parameters
    shadow_circle_radius = 0
    shadow_circle_linewidths = [3, 6, 8, 10, 12, 14, 16, 20, 22, 24, 26, 28, 30]
    
    # Draw scale circles
    for i in range(len(scale_line_radii)):
        radius = config.base_radius * (1 + scale_line_radii[i] * config.rel_change_scaling)
        circle = plt.Circle(
            (0, 0), 
            radius, 
            linestyle=scale_line_styles[i],
            fill=False, 
            edgecolor=scale_line_colors[i], 
            linewidth=scale_line_widths[i]
        )
        ax.add_patch(circle)
        
        # Add halo effect if requested
        if scale_line_radii[i] == shadow_circle_radius and halo:
            for lw in shadow_circle_linewidths:
                shadow_args = dict(
                    alpha=0.05,
                    antialiased=True, 
                    color='white',
                    linewidth=lw,
                    linestyle='-'
                )
                ax.add_patch(patches.Shadow(circle, 0, 0, shade=1, **shadow_args))

    # Draw sector wedges
    for s in range(len(piedata)):
        sector_change = sectors_dif_rel[time_index, country_index, s]
        
        if sector_change >= 0:
            # Positive change - create outer wedge
            radius = config.base_radius * (1 + config.rel_change_scaling * sector_change)
            wedges, _ = ax.pie(
                piedata, 
                radius=radius,
                colors=sectors_nace_1_colors if len(piedata) == len(sectors_nace_1) else sectors_nace_62_colors, 
                wedgeprops=config.wedgeprops, 
                counterclock=False, 
                startangle=-270,
                shadow=False
            )
            
            # Set width of wedge to create donut effect
            wedges[s].set_width(config.base_radius * (1 - 1/1 + config.rel_change_scaling * sector_change))
        else:
            # Negative change - create inner wedge
            wedges, _ = ax.pie(
                piedata, 
                radius=config.base_radius,
                colors=sectors_nace_1_colors if len(piedata) == len(sectors_nace_1) else sectors_nace_62_colors, 
                wedgeprops=config.wedgeprops, 
                counterclock=False, 
                startangle=-270,
                shadow=False
            )
            
            # Set width of wedge to show reduction
            wedges[s].set_width(-config.base_radius * config.rel_change_scaling * sector_change)
        
        # Show only the current sector wedge
        for wi in range(len(wedges)):
            if wi != s:
                wedges[wi].set_visible(False)

def addRelChangeStackedBarPlot(piedata, difData, ax, width=0.7):
    """
    Add stacked bar chart visualization for relative sector changes.
    
    Args:
        piedata (ndarray): Base pie chart data
        difData (ndarray): Difference data for sectors
        ax (Axes): Matplotlib axes object
        width (float, optional): Width of bar
    """
    ax.axis('off')
    ax.set_ylim(-0.2, 0.2)
    ax.set_xlim(-1, 1)
    
    # Sort sectors by size
    indices = np.argsort(piedata)[::-1]
    indices_up = [int(i) for i in indices if difData[i] > 0]
    indices_dn = [int(i) for i in indices if difData[i] < 0]
    width_mult = 0.95 * width / (2 * max(piedata))
    highlight_line_width = 5

    # First draw white background lines
    upsum = 0
    downsum = 0
    plt.plot([-width/2, width/2], [0, 0], 'w-', lw=highlight_line_width, zorder=-6)
    
    # Calculate scale lines for positive changes
    scale_lines = np.arange(0.05, sum(difData[indices_up]) + 0.025, step=0.05).tolist()
    scale_lines_max = max(scale_lines + [0])
    scale_lines_ls = ['-', '-'] * int(round(len(scale_lines) / (len(['-', '-']) * 0.9)))
    scale_lines_wdt = width / 3
    
    # Draw positive bars with white outlines
    for s in indices_up:
        ax.bar(
            0,
            difData[s],
            piedata[s] * width_mult,
            label='',
            bottom=upsum,
            color=sectors_nace_1_colors[s] if len(piedata) == len(sectors_nace_1) else sectors_nace_62_colors[s],
            edgecolor='white',
            linewidth=highlight_line_width,
            zorder=-5
        )
        upsum += difData[s]
        
        # Add scale line if needed
        if len(scale_lines) > 0 and upsum > scale_lines[0]:
            scale_lines_wdt = 0.16 + piedata[s] * width_mult
            plt.plot(
                [-scale_lines_wdt/2, scale_lines_wdt/2], 
                [scale_lines[0], scale_lines[0]],
                color='white',
                ls=scale_lines_ls.pop(),
                lw=highlight_line_width,
                zorder=-5
            )
            scale_lines.pop(0)
    
    # Add final scale line if needed
    if len(scale_lines) > 0:
        plt.plot(
            [-scale_lines_wdt/2, scale_lines_wdt/2], 
            [scale_lines[0], scale_lines[0]],
            color='white',
            ls=scale_lines_ls.pop(),
            lw=highlight_line_width,
            zorder=-5
        )

    # Calculate scale lines for negative changes
    scale_lines = np.arange(-0.05, sum(difData[indices_dn]) + 0.025 - 0.025, step=-0.05).tolist()
    scale_lines_min = min(scale_lines + [0])
    scale_lines_ls = ['-', '-'] * int(round(len(scale_lines) / (len(['-', '-']) * 0.9)))
    scale_lines_wdt = width
    
    # Draw negative bars with white outlines
    for s in indices_dn:
        ax.bar(
            0,
            difData[s],
            piedata[s] * width_mult,
            label='',
            bottom=downsum,
            linewidth=highlight_line_width,
            zorder=-5
        )
        downsum += difData[s]
        
        # Add scale line if needed
        if len(scale_lines) > 0 and downsum < scale_lines[0]:
            scale_lines_wdt = 0.16 + piedata[s] * width_mult
            plt.plot(
                [-scale_lines_wdt/2, scale_lines_wdt/2], 
                [scale_lines[0], scale_lines[0]],
                color='white',
                ls=scale_lines_ls.pop(),
                lw=highlight_line_width,
                zorder=-5
            )
            scale_lines.pop(0)
    
    # Add final scale line if needed
    if len(scale_lines) > 0:
        plt.plot(
            [-scale_lines_wdt/2, scale_lines_wdt/2], 
            [scale_lines[0], scale_lines[0]],
            color='white',
            ls='--',
            lw=highlight_line_width,
            zorder=-5
        )

    # Draw vertical center line
    plt.plot([0, 0], [scale_lines_min, scale_lines_max], color='white', zorder=-6, lw=highlight_line_width)

    # Now redraw with thin black/gray lines over the white ones for better visibility
    upsum = 0
    downsum = 0
    plt.plot([-width/2, width/2], [0, 0], 'k-', lw=1, zorder=-4)
    
    # Recalculate scale lines for positive changes
    scale_lines = np.arange(0.05, sum(difData[indices_up]) + 0.025, step=0.05).tolist()
    scale_lines_ls = ['--', ':'] * int(round(len(scale_lines) / (len(['--', ':']) * 0.9)))
    scale_lines_wdt = width / 3
    
    # Draw positive bars without outlines
    for s in indices_up:
        ax.bar(
            0,
            difData[s],
            piedata[s] * width_mult,
            label='',
            bottom=upsum,
            color=sectors_nace_1_colors[s] if len(piedata) == len(sectors_nace_1) else sectors_nace_62_colors[s],
            edgecolor='white',
            linewidth=0
        )
        upsum += difData[s]
        
        # Add scale line if needed
        if len(scale_lines) > 0 and upsum > scale_lines[0]:
            scale_lines_wdt = 0.15 + piedata[s] * width_mult
            plt.plot(
                [-scale_lines_wdt/2, scale_lines_wdt/2], 
                [scale_lines[0], scale_lines[0]],
                color='gray',
                ls=scale_lines_ls.pop(),
                lw=1,
                zorder=-4
            )
            scale_lines.pop(0)
    
    # Add final scale line if needed
    if len(scale_lines) > 0:
        plt.plot(
            [-scale_lines_wdt/2, scale_lines_wdt/2], 
            [scale_lines[0], scale_lines[0]],
            color='gray',
            ls=scale_lines_ls.pop(),
            lw=1,
            zorder=-4
        )

    # Recalculate scale lines for negative changes
    scale_lines = np.arange(-0.05, sum(difData[indices_dn]) + 0.025 - 0.025, step=-0.05).tolist()
    scale_lines_ls = ['--', ':'] * int(round(len(scale_lines) / (len(['--', ':']) * 0.9)))
    scale_lines_wdt = width
    
    # Draw negative bars without outlines
    for s in indices_dn:
        ax.bar(
            0,
            difData[s],
            piedata[s] * width_mult,
            label='',
            bottom=downsum,
            linewidth=0
        )
        downsum += difData[s]
        
        # Add scale line if needed
        if len(scale_lines) > 0 and downsum < scale_lines[0]:
            scale_lines_wdt = 0.15 + piedata[s] * width_mult
            plt.plot(
                [-scale_lines_wdt/2, scale_lines_wdt/2], 
                [scale_lines[0], scale_lines[0]],
                color='gray',
                ls=scale_lines_ls.pop(),
                lw=1,
                zorder=-4
            )
            scale_lines.pop(0)
    
    # Add final scale line if needed
    if len(scale_lines) > 0:
        plt.plot(
            [-scale_lines_wdt/2, scale_lines_wdt/2], 
            [scale_lines[0], scale_lines[0]],
            color='gray',
            ls='--',
            lw=1,
            zorder=-4
        )

def create_pie_charts_by_country(base, scenarios_dif_rel, config, 
                               country_codes, country_codes_3,
                               scenarios_names, time_steps, show_plots=False):
    """
    Create pie/donut charts for each country across time.
    
    Args:
        base (dict): Baseline data
        scenarios_dif_rel (list): List of dictionaries with relative differences
        config (PlotConfig): Plot configuration
        country_codes (list): List of country codes
        country_codes_3 (list): List of 3-letter country codes
        scenarios_names (list): List of scenario names
        time_steps (list): List of time steps
        show_plots (bool, optional): Whether to display plots interactively
    """
    chart_type = 'brokendonouts'  # Always use broken donuts now
    nrows = 3
    ncols = 5
    subfig_size = [3, 3]
    
    # Iterate through countries and scenarios
    for country_index in range(len(country_codes)):
        for scenario_index in range(len(scenarios_names)):
            # Define output directory
            base_dir = config.get_figure_dir(chart_type, scenarios_names[scenario_index])
            
            # Build filename
            filename = f"{chart_type}-{config.sector_thing}_in_{scenarios_names[scenario_index]}_scenario_as_{config.plot_type} for country {country_codes_3[country_index]}"
            
            # Skip if file already exists
            if not config.should_plot_file(chart_type, filename, scenarios_names[scenario_index]):
                continue
            
            # Create figure
            fig, axes = plt.subplots(
                nrows, 
                ncols, 
                figsize=(subfig_size[0]*ncols, subfig_size[1]*nrows)
            )
            
            fig.suptitle(
                f"{config.sector_thing} in {scenarios_names[scenario_index]} scenario as {config.plot_type} for country {country_codes_3[country_index]}"
            )
            
            # Plot each time step
            row = 0
            col = 0
            for time_index, timestep in enumerate(time_steps):
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
                
                # Create pie data
                piedata = base[config.sector_thing][time_index, country_index, :]
                
                # Add appropriate chart
                addBrokenDonutPlot(
                    piedata, 
                    ax, 
                    sectors_dif_rel=scenarios_dif_rel[scenario_index][config.sector_thing],
                    time_index=time_index,
                    country_index=country_index,
                    config=config
                )
                
                # Set title
                ax.title.set_text(timestep)
            
            # Hide unused subplots
            for time_index in range(len(time_steps), nrows*ncols-2):
                if col == ncols:
                    row += 1
                    col = 0
                axes[row, col].axis('off')
                col += 1
            
            # Add scale lines legend
            add_scale_legend(axes[nrows-1, ncols-2], config)
            
            # Add sector color legend
            add_sector_legend(axes[nrows-1, ncols-1], piedata)
            
            # Adjust layout and save figure
            plt.tight_layout()
            
            if show_plots:
                plt.show()
            
            # Save figure
            fig.savefig(os.path.join(base_dir, f"{filename}.png"), dpi=300)
            fig.savefig(os.path.join(base_dir, f"{filename}.pdf"))
            
            plt.close(fig)

def create_pie_charts_by_time(base, scenarios_dif_rel, config,
                            country_codes, scenarios_names, time_steps, show_plots=False):
    """
    Create pie/donut charts for each time step across countries.
    
    Args:
        base (dict): Baseline data
        scenarios_dif_rel (list): List of dictionaries with relative differences
        config (PlotConfig): Plot configuration
        country_codes (list): List of country codes
        scenarios_names (list): List of scenario names
        time_steps (list): List of time steps
        show_plots (bool, optional): Whether to display plots interactively
    """
    chart_type = 'brokendonouts'  # Always use broken donuts now
    nrows = 5
    ncols = 6
    subfig_size = [3, 3]
    
    # Iterate through scenarios and time steps
    for scenario_index in range(len(scenarios_names)):
        for time_index, timestep in enumerate(time_steps):
            # Define output directory
            base_dir = config.get_figure_dir(chart_type, scenarios_names[scenario_index])
            
            # Build filename
            filename = f"{chart_type}-{config.sector_thing}_in_{scenarios_names[scenario_index]}_scenario_as_{config.plot_type} for time {timestep}"
            
            # Skip if file already exists
            if not config.should_plot_file(chart_type, filename, scenarios_names[scenario_index]):
                continue
            
            # Create figure
            fig, axes = plt.subplots(
                nrows, 
                ncols, 
                figsize=(subfig_size[0]*ncols, subfig_size[1]*nrows)
            )
            
            fig.suptitle(
                f"{config.sector_thing} in {scenarios_names[scenario_index]} scenario as {config.plot_type} for time {timestep}"
            )
            
            # Plot each country
            row = 0
            col = 0
            for country_index in range(len(country_codes)):
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
                
                # Create pie data
                piedata = base[config.sector_thing][time_index, country_index, :]
                
                # Add appropriate chart
                addBrokenDonutPlot(
                    piedata, 
                    ax, 
                    sectors_dif_rel=scenarios_dif_rel[scenario_index][config.sector_thing],
                    time_index=time_index,
                    country_index=country_index,
                    config=config
                )
                
                # Set title
                ax.title.set_text(country_codes[country_index])
            
            # Hide unused subplots
            for country_index in range(len(country_codes), nrows*ncols-2):
                if col == ncols:
                    row += 1
                    col = 0
                axes[row, col].axis('off')
                col += 1
            
            # Add scale lines legend
            add_scale_legend(axes[nrows-1, ncols-2], config)
            
            # Add sector color legend
            add_sector_legend(axes[nrows-1, ncols-1], piedata)
            
            # Adjust layout and save figure
            plt.tight_layout()
            
            if show_plots:
                plt.show()
            
            # Save figure
            fig.savefig(os.path.join(base_dir, f"{filename}.png"), dpi=300)
            fig.savefig(os.path.join(base_dir, f"{filename}.pdf"))
            
            plt.close(fig)

def add_scale_legend(ax, config):
    """Add scale legend to the chart."""
    limits = 1 + (0.09 * config.rel_change_scaling)
    ax.set_xlim(-limits, limits)
    ax.set_ylim(-limits, limits)
    ax.axis('off')
    
    # Add reference circles
    ax.add_patch(plt.Circle((0, 0), (1-0.1*config.rel_change_scaling), linestyle='--', fill=False, edgecolor='gray', linewidth=1))
    ax.add_patch(plt.Circle((0, 0), (1-0.05*config.rel_change_scaling), linestyle=':', fill=False, edgecolor='gray', linewidth=1))
    ax.add_patch(plt.Circle((0, 0), 1, linestyle='-', fill=False, edgecolor='k'))
    ax.add_patch(plt.Circle((0, 0), (1+0.05*config.rel_change_scaling), linestyle=':', fill=False, edgecolor='gray', linewidth=1))
    
    # Add labels
    ax.text(0, (1-0.1*config.rel_change_scaling), '-10%', fontsize=10,
            backgroundcolor='white', color='gray', horizontalalignment='center', verticalalignment='center')
    ax.text(0, (1-0.05*config.rel_change_scaling), '-5%', fontsize=10,
            backgroundcolor='white', color='gray', horizontalalignment='center', verticalalignment='center')
    ax.text(0, 1, 'reference', fontsize=10,
            backgroundcolor='white', color='black', horizontalalignment='center', verticalalignment='center')
    ax.text(0, (1+0.05*config.rel_change_scaling), '+5%', fontsize=10,
            backgroundcolor='white', color='gray', horizontalalignment='center', verticalalignment='center')

def add_sector_legend(ax, piedata):
    """Add sector legend to the chart."""
    # Determine which sector classification is being used
    if len(piedata) == len(sectors_nace_1):
        sector_colors = sectors_nace_1_colors
        sector_names = sectors_nace_1
    else:
        sector_colors = sectors_nace_62_colors
        sector_names = sectors_nace_62
        
    # Create wedges for legend
    wedges, texts = ax.pie(
        np.ones(len(piedata)),
        radius=0.5,  # Use constant radius for legend
        colors=sector_colors, 
        labels=sector_names,
        wedgeprops={"edgecolor": "k", "linewidth": 0.5}, 
        counterclock=False, 
        startangle=-270
    )
    
    ax.title.set_text('Sectors')
