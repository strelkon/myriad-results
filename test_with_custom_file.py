#!/usr/bin/env python
"""
Test script for custom MAT files
Usage: python test_with_custom_file.py <path_to_your_file.mat>
"""

import sys
import os
from scipy.io import loadmat
import numpy as np

def inspect_mat_file(filepath):
    """Inspect the structure of a MAT file."""
    print(f"\n{'='*60}")
    print(f"Inspecting MAT file: {filepath}")
    print(f"{'='*60}\n")

    try:
        data = loadmat(filepath)

        print(f"✓ File loaded successfully")
        print(f"  Total keys found: {len(data.keys())}\n")

        # Filter out metadata keys
        data_keys = [k for k in data.keys() if not k.startswith('__')]

        print("Data Arrays Found:")
        print("-" * 60)

        for key in sorted(data_keys):
            value = data[key]
            if isinstance(value, np.ndarray):
                print(f"  {key:40s} {str(value.shape):20s} {value.dtype}")
            else:
                print(f"  {key:40s} {str(type(value)):20s}")

        print("\n" + "="*60)
        print("Checking for expected variables:")
        print("="*60 + "\n")

        expected_vars = [
            'real_output',
            'real_sector_output',
            'nominal_gdp',
            'real_gdp',
            'unemployment_rate'
        ]

        for var in expected_vars:
            if var in data:
                print(f"  ✓ {var:30s} shape: {data[var].shape}")
            else:
                print(f"  ✗ {var:30s} NOT FOUND")

        print("\n" + "="*60)
        print("Compatibility Check:")
        print("="*60 + "\n")

        # Check if it has the expected structure
        compatible = True
        issues = []

        if 'real_output' in data:
            shape = data['real_output'].shape
            print(f"  real_output shape: {shape}")

            # Check dimensions
            if len(shape) >= 2:
                print(f"    - Time dimension: {shape[0]}")
                print(f"    - Experiment dimension: {shape[1]}")
                if len(shape) > 2:
                    print(f"    - Country dimension: {shape[2] if len(shape) > 2 else 'N/A'}")
            else:
                compatible = False
                issues.append("real_output has unexpected number of dimensions")
        else:
            compatible = False
            issues.append("Missing 'real_output' variable")

        if 'real_sector_output' in data:
            shape = data['real_sector_output'].shape
            print(f"\n  real_sector_output shape: {shape}")

            if len(shape) >= 3:
                print(f"    - Time dimension: {shape[0]}")
                print(f"    - Experiment dimension: {shape[1]}")
                print(f"    - Country dimension: {shape[2]}")
                if len(shape) > 3:
                    print(f"    - Sector dimension: {shape[3]}")

                    # Check if sector count matches
                    if shape[3] == 62:
                        print(f"    ✓ Sector count matches NACE-62 classification (62 sectors)")
                    else:
                        print(f"    ⚠ Sector count is {shape[3]}, expected 62")
            else:
                compatible = False
                issues.append("real_sector_output has unexpected dimensions")

        print("\n" + "="*60)
        if compatible and not issues:
            print("✓ FILE IS COMPATIBLE with the analysis scripts!")
            print("="*60 + "\n")

            print("You can use this file with:")
            print(f"  python main.py --scenario-files {os.path.basename(filepath)} --scenario-names 'Your Scenario'")
            print("\nOr for testing with two files:")
            print(f"  python main.py --scenario-files baseline.mat {os.path.basename(filepath)} --scenario-names 'Shock'")
        else:
            print("⚠ POTENTIAL COMPATIBILITY ISSUES FOUND:")
            print("="*60 + "\n")
            for issue in issues:
                print(f"  - {issue}")
            print("\nThe file may still work, but some features might not function correctly.")

        return data, compatible

    except FileNotFoundError:
        print(f"✗ ERROR: File not found: {filepath}")
        return None, False
    except Exception as e:
        print(f"✗ ERROR loading file: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, False

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_with_custom_file.py <path_to_mat_file>")
        print("\nExample:")
        print("  python test_with_custom_file.py data/my_scenario.mat")
        sys.exit(1)

    filepath = sys.argv[1]

    if not os.path.exists(filepath):
        print(f"Error: File does not exist: {filepath}")
        sys.exit(1)

    data, compatible = inspect_mat_file(filepath)

    if data and compatible:
        print("\n" + "="*60)
        print("Next Steps:")
        print("="*60)
        print("\n1. Place your file in the data/ directory")
        print("2. Run the analysis:")
        print(f"   python main.py --scenario-files baseline.mat {os.path.basename(filepath)} --debug")
        print("\n3. Or use the legacy script by editing the file paths in:")
        print("   IIASA_ABM_Raw_Results_Analysis.py (lines 66-71)")

    return 0 if compatible else 1

if __name__ == "__main__":
    sys.exit(main())
