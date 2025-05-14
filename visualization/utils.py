# visualization/utils.py
"""
Utility functions for visualization in the IIASA ABM analysis.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

def ensure_dir_exists(directory):
    """
    Create directory if it doesn't exist.
    
    Args:
        directory (str): Path to the directory
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

def save_figure(fig, filepath, formats=None, dpi=300):
    """
    Save figure in multiple formats.
    
    Args:
        fig (Figure): Matplotlib figure object
        filepath (str): Base filepath without extension
        formats (list, optional): List of formats to save (default: ['png', 'pdf'])
        dpi (int, optional): DPI for raster formats
    """
    if formats is None:
        formats = ['png', 'pdf']
    
    # Ensure directory exists
    directory = os.path.dirname(filepath)
    ensure_dir_exists(directory)
    
    # Save in each format
    for fmt in formats:
        fig.savefig(f"{filepath}.{fmt}", dpi=dpi if fmt in ['png', 'jpg', 'jpeg'] else None)

def describe_data(data):
    """
    Describe the structure of the data.
    
    Args:
        data (dict): Dictionary containing data arrays
    """
    from constants import dimensionLabels, dimensionLabelsLengths
    
    for key in list(data.keys()):
        print(key)
        if not isinstance(data[key], np.ndarray):
            print("   Is not a data array, ignoring.")
        else:
            x = data[key]
            print("   Is an array with shape: " + str(x.shape))
            dimensions = ''
            for j in range(0, len(list(x.shape))):
                if key[-5:] == "_mean" and j == 1 and x.shape[j] == 1:
                    dimensions = dimensions + "experiment mean" + ', '
                else:
                    dimensions = dimensions + list(dimensionLabels.keys())[dimensionLabelsLengths.index(x.shape[j])] + ', '
            dimensions = dimensions[:-2]  # Remove trailing comma and space
            print("   dimensions: " + dimensions)

def should_plot_file(filepath, label):
    """
    Check if file exists and print appropriate message.
    
    Args:
        filepath (str): Path to the file
        label (str): Label for the file (for printing messages)
        
    Returns:
        bool: True if the file should be generated, False if it exists
    """
    if os.path.isfile(filepath):
        print(f'Skipping {label} - file exists.')
        return False
    
    print(f'Plotting {label}')
    return True

def create_figure(nrows, ncols, figsize, title=None):
    """
    Create a new figure with appropriate settings.
    
    Args:
        nrows (int): Number of rows
        ncols (int): Number of columns
        figsize (tuple): Figure size (width, height)
        title (str, optional): Figure title
        
    Returns:
        tuple: (fig, axes) Matplotlib figure and axes objects
    """
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    
    if title:
        fig.suptitle(title)
    
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    return fig, axes
