# run.sh
#!/bin/bash

# Setup Python environment
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Creating and activating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Create output directories if they don't exist
mkdir -p figures/timeseries
mkdir -p figures/maps
mkdir -p figures/brokendonouts
mkdir -p figures/maps-brokendonut

# Run the analysis and visualization script
echo "Running IIASA ABM Results Analysis..."
python main.py

echo "Analysis and visualization complete!"
echo "Results are available in the 'figures' directory."
