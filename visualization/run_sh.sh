# run.sh (updated)
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

# Parse command-line arguments
OUTPUT_DIR="figures"
SHOW_PLOTS=false
SCENARIOS=()
SCENARIO_FILES=()

# Process arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --show-plots)
            SHOW_PLOTS=true
            shift
            ;;
        --scenario-names)
            shift
            while [[ $# -gt 0 && ! $1 =~ ^-- ]]; do
                SCENARIOS+=("$1")
                shift
            done
            ;;
        --scenario-files)
            shift
            while [[ $# -gt 0 && ! $1 =~ ^-- ]]; do
                SCENARIO_FILES+=("$1")
                shift
            done
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Prepare command
CMD="python main.py --output-dir $OUTPUT_DIR"

# Add show-plots flag if enabled
if $SHOW_PLOTS; then
    CMD="$CMD --show-plots"
fi

# Add scenarios if provided
if [ ${#SCENARIOS[@]} -gt 0 ]; then
    CMD="$CMD --scenario-names ${SCENARIOS[@]}"
fi

# Add scenario files if provided
if [ ${#SCENARIO_FILES[@]} -gt 0 ]; then
    CMD="$CMD --scenario-files ${SCENARIO_FILES[@]}"
fi

# Run the analysis
echo "Running IIASA ABM Results Analysis with command:"
echo "$CMD"
eval "$CMD"

echo "Analysis and visualization complete!"
echo "Results are available in the '$OUTPUT_DIR' directory."
