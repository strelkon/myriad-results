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

# NUTS regions
regions = ['AT11', 'AT12', 'AT13', 'AT21', 'AT22', 'AT31', 'AT32', 'AT33', 'AT34', 'BE10', 'BE21', 'BE22', 'BE23',
         'BE24', 'BE25', 'BE31', 'BE32', 'BE33', 'BE34', 'BE35', 'BG31', 'BG32', 'BG33', 'BG34', 'BG41', 'BG42',
         'CY00', 'CZ01', 'CZ02', 'CZ03', 'CZ04', 'CZ05', 'CZ06', 'CZ07', 'CZ08', 'DE11', 'DE12', 'DE13', 'DE14',
         'DE21', 'DE22', 'DE23', 'DE24', 'DE25', 'DE26', 'DE27', 'DE30', 'DE40', 'DE50', 'DE60', 'DE71', 'DE72',
         'DE73', 'DE80', 'DE91', 'DE92', 'DE93', 'DE94', 'DEA1', 'DEA2', 'DEA3', 'DEA4', 'DEA5', 'DEB1', 'DEB2',
         'DEB3', 'DEC0', 'DED2', 'DED4', 'DED5', 'DEE0', 'DEF0', 'DEG0', 'DK01', 'DK02', 'DK03', 'DK04', 'DK05',
         'EE00', 'EL30', 'EL41', 'EL42', 'EL43', 'EL51', 'EL52', 'EL53', 'EL54', 'EL61', 'EL62', 'EL63', 'EL64',
         'EL65', 'ES11', 'ES12', 'ES13', 'ES21', 'ES22', 'ES23', 'ES24', 'ES30', 'ES41', 'ES42', 'ES43', 'ES51',
         'ES52', 'ES53', 'ES61', 'ES62', 'ES63', 'ES64', 'ES70', 'FI1B', 'FI1C', 'FI1D', 'FI19', 'FI20', 'FR10',
         'FRB0', 'FRC1', 'FRC2', 'FRD1', 'FRD2', 'FRE1', 'FRE2', 'FRF1', 'FRF2', 'FRF3', 'FRG0', 'FRH0', 'FRI1',
         'FRI2', 'FRI3', 'FRJ1', 'FRJ2', 'FRK1', 'FRK2', 'FRL0', 'FRM0', 'FRY1', 'FRY2', 'FRY3', 'FRY4', 'HR03',
         'HU11', 'HU12', 'HU21', 'HU22', 'HU23', 'HU31', 'HU32', 'HU33', 'IE04', 'IE05', 'IE06', 'ITC1', 'ITC2',
         'ITC3', 'ITC4', 'ITF1', 'ITF2', 'ITF3', 'ITF4', 'ITF5', 'ITF6', 'ITG1', 'ITG2', 'ITH1', 'ITH2', 'ITH3',
         'ITH4', 'ITH5', 'ITI1', 'ITI2', 'ITI3', 'ITI4', 'LT01', 'LT02', 'LU00', 'LV00', 'NL11', 'NL12', 'NL13',
         'NL21', 'NL22', 'NL23', 'NL31', 'NL32', 'NL33', 'NL34', 'NL41', 'NL42', 'PL21', 'PL22', 'PL41', 'PL42',
         'PL43', 'PL51', 'PL52', 'PL61', 'PL62', 'PL63', 'PL71', 'PL72', 'PL81', 'PL82', 'PL84', 'PL91', 'PL92',
         'PT11', 'PT15', 'PT16', 'PT17', 'PT18', 'PT20', 'PT30', 'RO11', 'RO12', 'RO21', 'RO22', 'RO31', 'RO32',
         'RO41', 'RO42', 'SE11', 'SE12', 'SE21', 'SE22', 'SE23', 'SE31', 'SE32', 'SE33', 'SI03', 'SI04', 'SK01',
         'SK02', 'SK03', 'SK04']

# Danube region related countries and regions
danube_countries = ['DE', 'AT', 'CZ', 'HU', 'SK', 'SI', 'RO', 'BG', 'HR']

# NUTS-2 codes for Danube region countries and German regions
danube_nuts_2 = [
    # Germany
    'DE11', 'DE13', 'DE14', 'DE21', 'DE22', 'DE23', 'DE24', 'DE25', 'DE26', 'DE27',
    # Austria
    'AT11', 'AT12', 'AT13', 'AT21', 'AT22', 'AT31', 'AT32', 'AT33', 'AT34',
    # Czechia
    'CZ01', 'CZ02', 'CZ03', 'CZ04', 'CZ05', 'CZ06', 'CZ07', 'CZ08',
    # Hungary
    'HU11', 'HU12', 'HU21', 'HU22', 'HU23', 'HU31', 'HU32', 'HU33',
    # Slovenia
    'SI03', 'SI04',
    # Croatia
    'HR03',
    # Romania
    'RO11', 'RO12', 'RO21', 'RO22', 'RO31', 'RO32', 'RO41', 'RO42',
    # Bulgaria
    'BG31', 'BG32', 'BG33', 'BG34', 'BG41', 'BG42'
]

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
