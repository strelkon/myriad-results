# data_processing/aggregation.py (more robust)
"""
Functions for aggregating and processing data for the IIASA ABM analysis.
"""

import numpy as np
from functools import lru_cache
from constants import thingsWeCareAbout, experiments

@lru_cache(maxsize=128)
def get_sector_mappings(sector_index, nace1_code, sectors_nace_62_tuple):
    """
    Return cached sector mappings to avoid recalculation.
    
    Args:
        sector_index (int): Index of the sector in sectors_nace_1
        nace1_code (str): NACE 1 sector code at the given index
        sectors_nace_62_tuple (tuple): Tuple of NACE 62 sector codes
        
    Returns:
        list: Indices of sectors in NACE 62 that map to the given NACE 1 sector
    """
    return [i for i, sector in enumerate(sectors_nace_62_tuple) 
            if sector.startswith(nace1_code)]

def find_dimension_index(shape, target_length):
    """
    Find the index of the dimension with length equal to the target.
    
    Args:
        shape (list): Shape of the array
        target_length (int): Length to search for
        
    Returns:
        int: Index of the dimension with target length, or -1 if not found
    """
    for i, dim_length in enumerate(shape):
        if dim_length == target_length:
            return i
    return -1

def aggregateSectorNace62ToNace1(inArray, sectors_nace_1, sectors_nace_62, time_steps):
    """
    Aggregate sector data from NACE 62 to NACE 1 classification.
    
    Args:
        inArray (ndarray): Input array with sector data
        sectors_nace_1 (list): List of NACE 1 sector codes
        sectors_nace_62 (list): List of NACE 62 sector codes
        time_steps (list): List of time steps
        
    Returns:
        ndarray: Aggregated array with NACE 1 sectors
    """
    shape = list(inArray.shape)
    
    # Find the dimension corresponding to sectors
    sectorDim = find_dimension_index(shape, len(sectors_nace_62))
    
    if sectorDim == -1:
        # If no dimension matches exactly, print debug info and try best guess
        print(f"Warning: Could not find dimension with length {len(sectors_nace_62)} in array with shape {shape}")
        print(f"Input array shape: {shape}")
        print(f"Sectors NACE 62 length: {len(sectors_nace_62)}")
        print(f"Sectors NACE 1 length: {len(sectors_nace_1)}")
        
        # Try to determine the sector dimension based on typical array structure
        if len(shape) == 3:  # Typically (time, country, sector)
            sectorDim = 2
        elif len(shape) == 4:  # Typically (time, experiment, country, sector)
            sectorDim = 3
        else:
            raise ValueError(f"Cannot determine sector dimension in array with shape {shape}")
        
        print(f"Using best guess for sector dimension: {sectorDim}")
    
    # Create output array with new shape
    new_shape = shape.copy()
    new_shape[sectorDim] = len(sectors_nace_1)
    aggArray = np.ones(new_shape)
    
    # Convert lists to tuples for caching
    sectors_nace_62_tuple = tuple(sectors_nace_62)
    
    # Use pre-computed sector mappings for faster aggregation
    if len(shape) == 4:  # 4D array with experiments dimension
        # Determine which dimension is which
        timeDim = find_dimension_index(shape, len(time_steps))
        if timeDim == -1:
            timeDim = 0  # Default to first dimension
        
        expDim = find_dimension_index(shape, len(experiments))
        if expDim == -1:
            expDim = 1  # Default to second dimension
        
        countryDim = 3 - sectorDim - timeDim - expDim  # The remaining dimension
        
        # Perform aggregation
        for t in range(shape[timeDim]):
            for e in range(shape[expDim]):
                for c in range(shape[countryDim]):
                    for s in range(len(sectors_nace_1)):
                        matched_sector_idcs = get_sector_mappings(s, sectors_nace_1[s], sectors_nace_62_tuple)
                        # Create index tuple dynamically
                        idx = [0] * 4
                        idx[timeDim] = t
                        idx[expDim] = e
                        idx[countryDim] = c
                        
                        # For the original array, iterate over matched sectors
                        sum_val = 0
                        for sec_idx in matched_sector_idcs:
                            idx[sectorDim] = sec_idx
                            sum_val += inArray[tuple(idx)]
                        
                        # For the aggregated array, set the value
                        idx[sectorDim] = s
                        aggArray[tuple(idx)] = sum_val
                        
    else:  # 3D array without experiments dimension
        # Determine which dimension is which
        timeDim = find_dimension_index(shape, len(time_steps))
        if timeDim == -1:
            timeDim = 0  # Default to first dimension
        
        # The remaining dimension is the country dimension
        countryDim = 3 - sectorDim - timeDim 
        
        # Perform aggregation
        for t in range(shape[timeDim]):
            for c in range(shape[countryDim]):
                for s in range(len(sectors_nace_1)):
                    matched_sector_idcs = get_sector_mappings(s, sectors_nace_1[s], sectors_nace_62_tuple)
                    # Create index tuple dynamically
                    idx = [0] * 3
                    idx[timeDim] = t
                    idx[countryDim] = c
                    
                    # For the original array, iterate over matched sectors
                    sum_val = 0
                    for sec_idx in matched_sector_idcs:
                        idx[sectorDim] = sec_idx
                        sum_val += inArray[tuple(idx)]
                    
                    # For the aggregated array, set the value
                    idx[sectorDim] = s
                    aggArray[tuple(idx)] = sum_val
    
    return aggArray

def calculate_means_and_differences(base, scenarios, sectors_nace_1, sectors_nace_62, time_steps):
    """
    Calculate means, differences, and relative differences between scenarios and baseline.
    
    Args:
        base (dict): Baseline data
        scenarios (list): List of scenario data dictionaries
        sectors_nace_1 (list): List of NACE 1 sector codes
        sectors_nace_62 (list): List of NACE 62 sector codes
        time_steps (list): List of time steps
        
    Returns:
        tuple: (scenarios_rel, scenarios_dif, scenarios_dif_rel) - relative values, 
               absolute differences, and relative differences
    """
    # First calculate means for each scenario
    for key in thingsWeCareAbout:
        if key in base:
            # Handle arrays with different dimensions correctly
            if base[key].ndim >= 2:
                # Assume the second dimension is the one to average over
                base[key + "_mean"] = np.mean(base[key], axis=1)
                for s in range(len(scenarios)):
                    if key in scenarios[s]:
                        scenarios[s][key + "_mean"] = np.mean(scenarios[s][key], axis=1)
    
    # Add mean items to the list of things we care about
    extended_things = thingsWeCareAbout.copy()
    for key in thingsWeCareAbout:
        if key + "_mean" in base:
            extended_things.append(key + "_mean")
    
    # Aggregate sectors from NACE 62 to NACE 1
    for key in extended_things.copy():  # Use a copy since we're modifying the list
        if 'sector' in key and key in base:
            try:
                base[key + "_nace1"] = aggregateSectorNace62ToNace1(
                    base[key], sectors_nace_1, sectors_nace_62, time_steps
                )
                extended_things.append(key + "_nace1")
                
                for s in range(len(scenarios)):
                    if key in scenarios[s]:
                        scenarios[s][key + "_nace1"] = aggregateSectorNace62ToNace1(
                            scenarios[s][key], sectors_nace_1, sectors_nace_62, time_steps
                        )
            except Exception as e:
                print(f"Warning: Could not aggregate sectors for {key}: {str(e)}")
                print(f"Skipping sector aggregation for {key}")
    
    # Calculate relative values and differences
    scenarios_rel = []
    scenarios_dif = []
    scenarios_dif_rel = []

    print(extended_things)
    
    for s in range(len(scenarios)):
        scenarios_rel.append({})
        scenarios_dif.append({})
        scenarios_dif_rel.append({})
        
        for key in extended_things:
            # Skip if key doesn't exist in base or scenario
            if key not in base or key not in scenarios[s]:
                continue
            
            # Skip if shapes don't match
            if base[key].shape != scenarios[s][key].shape:
                print(f"Warning: Shapes don't match for {key}. Base: {base[key].shape}, Scenario: {scenarios[s][key].shape}")
                continue
                
            # Calculate relative values (scenario/base)
            scenarios_rel[s][key] = np.divide(
                scenarios[s][key], 
                base[key], 
                out=np.zeros_like(scenarios[s][key]), 
                where=base[key]!=0
            )
            
            # Calculate absolute differences (scenario-base)
            scenarios_dif[s][key] = scenarios[s][key] - base[key]
            
            # Calculate relative differences ((scenario-base)/base)
            scenarios_dif_rel[s][key] = np.divide(
                scenarios[s][key] - base[key], 
                base[key], 
                out=np.zeros_like(scenarios[s][key]), 
                where=base[key]!=0
            )
    
    return scenarios_rel, scenarios_dif, scenarios_dif_rel
