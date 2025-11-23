# Basketball Shot Chart Analysis

This project creates a confusion-matrix-style shot chart visualization that displays points per shot (PPS) and points per possession (PPP) for different zones on the basketball court.

## Features

- Divides the basketball court into a grid (default: 5x5 zones)
- Calculates points per shot for each zone
- Calculates points per possession for each zone
- Creates heatmap visualizations similar to a confusion matrix
- Displays shot counts in each zone

## Setup

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

2. Prepare your shot data CSV file with the following columns:
   - `GameClock`: Time on the game clock
   - `Quarter`: Quarter number
   - `Player`: Player name
   - `Team`: Team name
   - `ShotType`: Type of shot (e.g., "Jump Shot", "3PT Shot", "Layup", "Dunk")
   - `Result`: "Made" or "Miss"
   - `X`: X coordinate of the shot (0-94 feet, court width)
   - `Y`: Y coordinate of the shot (0-50 feet, court length)
   - `AssistBy`: Player who assisted (or "N/A")
   - `Distance`: Distance of the shot

3. Name your CSV file `shots_data.csv` or modify `main.py` to use a different filename.

## Usage

Run the main script (make sure virtual environment is activated):
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
python main.py
```

Or use the convenience script:
```bash
./run.sh
```

The script will:
1. Load your shot data
2. Calculate statistics for each zone
3. Generate multiple visualization files:
   - `shot_chart_comparison.png`: Side-by-side comparison of PPS and PPP
   - `shot_chart_combined.png`: Combined chart showing both metrics
   - `shot_chart_pps.png`: Points per shot only
   - `shot_chart_ppp.png`: Points per possession only
4. Save zone statistics to `zone_statistics.csv`

## Customization

You can adjust the grid size by modifying the `grid_rows` and `grid_cols` parameters in `main.py`:

```python
grid_rows = 5  # Number of zones along court length
grid_cols = 5  # Number of zones along court width
```

You can also adjust court dimensions in `process_shots.py` if your coordinate system differs:
- `court_width`: Default 94 feet
- `court_length`: Default 50 feet

## Sample Data

A sample dataset (`sample_shots_data.csv`) is included for testing. You can rename it to `shots_data.csv` to use it.

## Output

The visualizations show:
- Color intensity: Higher values are shown in blue/green, lower values in red
- Text annotations: Each cell displays the metric value and number of shots
- Grid layout: Similar to a confusion matrix, with zones labeled

## Notes

- Each shot is treated as a possession for PPP calculation
- 3PT shots are worth 3 points when made, all other made shots are worth 2 points
- Zones with no shots are displayed in gray with "No Shots" text

