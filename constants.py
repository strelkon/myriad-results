# constants.py
"""
Constants and data labels for the IIASA ABM Results Analysis.
Centralizes all the reference data used throughout the project.
"""

import numpy as np
import matplotlib.cm as cm

# List of country codes
country_codes = ['AT', 'BE', 'BG', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR', 'HR',
                'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'NL', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK']

country_codes_3 = ['AUT', 'BEL', 'BGR', 'CYP', 'CZE', 'DEU', 'DNK', 'EST', 'GRC', 'ESP', 'FIN', 'FRA', 'HRV',
                 'HUN', 'IRL', 'ITA', 'LTU', 'LUX', 'LVA', 'NLD', 'POL', 'PRT', 'ROU', 'SWE', 'SVN', 'SVK']

# Danube region related countries and regions
danube_countries = ['DE', 'AT', 'CZ', 'HU', 'SK', 'SI', 'RO', 'BG', 'HR']

# Sector codes
sectors_nace_62 = ['A01', 'A02', 'A03', 'B', 'C10-C12', 'C13-C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23',
           'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30', 'C31_C32', 'C33', 'D', 'E36', 'E37-E39', 'F', 'G45',
           'G46', 'G47', 'H49', 'H50', 'H51', 'H52', 'H53', 'I', 'J58', 'J59_J60', 'J61', 'J62_J63', 'K64', 'K65',
           'K66', 'L', 'M69_M70', 'M71', 'M72', 'M73', 'M74_M75', 'N77', 'N78', 'N79', 'N80-N82', 'O', 'P',
           'Q86', 'Q87_Q88', 'R90-R92', 'R93', 'S94', 'S95', 'S96']

sectors_nace_1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S']

key_sectors = ['A01', 'H50', 'H51', 'H52', 'H53', 'K64', 'K65']

# Time steps and experiment labels
time_steps = [f"Quarter {i}" for i in range(0, 13)]
experiments = [f"E{i}" for i in range(0, 18)]

# Dict of dimension labels and their lengths for referencing
dimensionLabels = {
    "countries": country_codes,
    "sectors_nace_62": sectors_nace_62,
    "sectors_nace_1": sectors_nace_1,
    "time": time_steps,
    "experiments": experiments
}

dimensionLabelsLengths = [len(dimensionLabels[i]) for i in dimensionLabels.keys()]

# Colors for sectors
sectors_nace_1_colors = cm.tab20.colors
sectors_nace_62_colors = cm.tab20(np.linspace(0, 1, len(sectors_nace_62)))

# List of economic variables we're interested in
thingsWeCareAbout = [
    'capital_consumption', 'capital_loss', 'compensation_employees', 'euribor',
    'government_debt', 'government_deficit', 'nominal_capitalformation', 'nominal_exports',
    'nominal_fixed_capitalformation', 'nominal_fixed_capitalformation_dwellings',
    'nominal_gdp', 'nominal_government_consumption', 'nominal_gva',
    'nominal_household_consumption', 'nominal_imports', 'nominal_output', 'nominal_sector_gva',
    'nominal_sector_output', 'operating_surplus', 'real_capitalformation', 'real_exports',
    'real_fixed_capitalformation', 'real_fixed_capitalformation_dwellings', 'real_gdp',
    'real_government_consumption', 'real_gva', 'real_household_consumption', 'real_imports',
    'real_output', 'real_sector_gva', 'real_sector_output', 'sector_capital_consumption',
    'sector_capital_loss', 'sector_operating_surplus', 'taxes_production', 'unemployment_rate',
    'wages'
]

# Base directory for data files
data_dir = 'data'
