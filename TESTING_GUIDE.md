# Testing Guide for Custom MAT Files

This guide explains how to test the analysis scripts with your own MAT files.

## Step 1: Download Your File

Download the file from Google Drive to your local machine.

## Step 2: Inspect the File Structure

Use the provided test script to check if your file is compatible:

```bash
python test_with_custom_file.py /path/to/your/downloaded/file.mat
```

This will show you:
- ✓ All variables in the file
- ✓ Their shapes and data types
- ✓ Whether it's compatible with the analysis scripts
- ✓ Any potential issues

## Step 3: Place the File

Put your downloaded file in the appropriate directory:

```bash
# Create data directory if needed
mkdir -p data

# Move your file
mv ~/Downloads/your_file.mat data/
```

## Step 4: Run the Analysis

### Option A: Modern Modular Approach (Recommended)

```bash
# Single scenario file
python main.py \
  --scenario-files data/your_file.mat \
  --scenario-names "My Scenario" \
  --debug

# With baseline + shock scenario
python main.py \
  --scenario-files data/baseline.mat data/your_shock.mat \
  --scenario-names "Shock Scenario" \
  --debug \
  --show-plots
```

### Option B: Legacy Script

1. Edit `IIASA_ABM_Raw_Results_Analysis.py`
2. Modify lines 66-71 to point to your files:
   ```python
   base = loadmat('data/your_baseline.mat')
   shock_eq = loadmat('data/your_shock.mat')
   # ... etc
   ```
3. Run: `python IIASA_ABM_Raw_Results_Analysis.py`

## Troubleshooting

### File Not Compatible?

If the test script shows compatibility issues:

1. **Check variable names**: The script expects variables like:
   - `real_output`
   - `real_sector_output`
   - `nominal_gdp`
   - etc.

2. **Check dimensions**: Arrays should have shapes like:
   - `real_output`: (time_steps, experiments, countries)
   - `real_sector_output`: (time_steps, experiments, countries, sectors)

3. **Enable debug mode** to see detailed error messages:
   ```bash
   python main.py --scenario-files your_file.mat --debug
   ```

### Common Issues

**Issue**: "FileNotFoundError"
- **Solution**: Check the file path is correct
- Use absolute paths if needed: `/full/path/to/file.mat`

**Issue**: "KeyError" for a variable
- **Solution**: Your file may have different variable names
- Use the test script to see all available variables
- Modify the analysis scripts if needed

**Issue**: "Shape mismatch" errors
- **Solution**: Your data may have different dimensions
- Check the test script output for actual shapes
- May need to adjust constants (time_steps, countries, etc.)

## Expected File Structure

For best compatibility, MAT files should contain:

### Required Variables
- `real_output` - Real economic output (time × experiments × countries)
- `real_sector_output` - Sectoral output (time × experiments × countries × sectors)

### Optional but Recommended
- `nominal_gdp` - Nominal GDP
- `real_gdp` - Real GDP
- `unemployment_rate` - Unemployment rate
- All other economic variables (see `constants.py` for full list)

### Dimensions
- **Time steps**: Typically 13 quarters (0-12)
- **Experiments**: Typically 18 Monte Carlo runs
- **Countries**: 26 EU countries
- **Sectors**: 62 NACE sectors

## Getting Help

If you encounter issues:

1. Run the test script first to diagnose
2. Enable `--debug` mode for detailed logging
3. Check the error messages carefully
4. Verify your file structure matches expectations

## Quick Reference

```bash
# Test file compatibility
python test_with_custom_file.py data/your_file.mat

# Run with debug mode
python main.py --scenario-files data/file.mat --debug

# Run with multiple scenarios
python main.py \
  --scenario-files data/baseline.mat data/shock1.mat data/shock2.mat \
  --scenario-names "Shock 1" "Shock 2" \
  --debug

# Show plots interactively
python main.py --scenario-files data/file.mat --show-plots
```
