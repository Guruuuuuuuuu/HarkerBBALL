# Basketball Game Statistics Analysis System

A comprehensive analysis framework for basketball game statistics that calculates efficiency metrics, analyzes turnovers, evaluates rebounding, optimizes shot selection, and generates detailed coaching reports.

## Features

- **Efficiency Metrics**: Calculates points per possession (PPP) and points per shot (PPS)
- **Turnover Analysis**: Identifies turnover trends, potential points lost, and reduction strategies
- **Rebounding Analysis**: Evaluates offensive/defensive rebounding performance and opponent rebounding ability
- **Shot Selection Optimization**: Determines optimal 2PT vs 3PT shot mix based on expected values
- **Possession Tracking**: Accurately calculates and tracks possessions
- **Comprehensive Coach Reports**: Generates detailed PDF reports with actionable insights

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

## Data Format

The system requires two CSV files:

### 1. Team Box Score CSV
Should contain columns including:
- `Team`: Team name (e.g., "Harker", "Aptos")
- `Points`: Total points scored
- `FG Made`, `FG Attempts`, `FG%`: Field goal statistics
- `2FG Made`, `2FG Attempts`, `2FG%`: Two-point field goals
- `3FG Made`, `3FG Att`, `3FG%`: Three-point field goals
- `Offensive Rebounds`, `Defensive Rebounds`, `Rebounds`: Rebounding stats
- `Assists`, `Turnovers`, `Fouls`: Other statistics
- `True Shooting%`, `Effective Field Goal%`: Advanced metrics
- `Points Per Possession`: Points per possession (if available)

### 2. Player Statistics CSV
Should contain columns including:
- `Team`: "home" for our team, or team identifier
- `Athlete`: Player name
- `#`: Player number
- `Basic:MP`: Minutes played (MM:SS format)
- `Basic:PTS`, `Basic:FGM`, `Basic:FGA`, `Basic:FG%`: Basic shooting stats
- `Basic:3FGM`, `Basic:3FGA`, `Basic:3FG%`: Three-point shooting
- `Basic:ORB`, `Basic:DRB`, `Basic:TRB`: Rebounding stats
- `Basic:AST`, `Basic:STL`, `Basic:BLK`, `Basic:TO`: Other stats
- `Advanced:USG%`, `Advanced:ORB%`, `Advanced:DRB%`: Advanced metrics
- `Shooting:TS%`, `Shooting:eFG%`: Shooting efficiency metrics

## Usage

Run the analysis script with your CSV files:

```bash
source venv/bin/activate
python analyze_game_stats.py [team_box_score.csv] [player_stats.csv]
```

If no arguments are provided, it will look for files in your Downloads folder with default names.

Example:
```bash
python analyze_game_stats.py "2025-10-21 Harker vs Aptos -team-box-score.csv" "2025-10-21 Harker vs Aptos stats.csv"
```

## Output

The script generates:

1. **Console Output**: Real-time analysis results showing:
   - Efficiency metrics comparison
   - Turnover analysis
   - Rebounding statistics
   - Shot selection recommendations

2. **gamma_report_prompt.txt**: Detailed, formatted prompt for Gamma.app including:
   - Executive summary with key metrics
   - Comprehensive efficiency analysis
   - Turnover analysis and reduction strategies
   - Rebounding analysis and opponent assessment
   - Shot selection optimization recommendations
   - Player performance highlights
   - Action items and next steps
   - Visualization recommendations for charts/graphs
   
   **How to use:**
   - Copy the content from `gamma_report_prompt.txt`
   - Go to [Gamma.app](https://gamma.app)
   - Create a new presentation
   - Paste the content to generate a beautiful, interactive graphical report

3. **game_summary.txt**: Quick text summary for easy reference

## Customization

You can customize the team names in `analyze_game_stats.py`:

```python
analyzer = GameAnalyzer(
    team_box_score_path=team_box_score_path,
    player_stats_path=player_stats_path,
    our_team="Harker",      # Change to your team name
    opponent_team="Aptos"   # Change to opponent team name
)
```

## Key Metrics Explained

- **Points Per Possession (PPP)**: Average points scored per possession. Higher is better.
- **Points Per Shot (PPS)**: Average points per shot attempt. Higher is better.
- **Expected Value**: Statistical expected points for shot types (2PT vs 3PT)
- **Turnover Rate**: Percentage of possessions ending in turnovers. Lower is better.
- **Rebounding Percentage**: Percentage of available rebounds captured. Higher is better.

## Analysis Features

### Turnover Reduction System
- Identifies high-risk players and situations
- Calculates potential points lost from turnovers
- Provides specific reduction strategies
- Tracks assist-to-turnover ratios

### Rebounding Intelligence
- Analyzes offensive rebounding opportunities
- Evaluates opponent rebounding strengths/weaknesses
- Identifies second-chance opportunities
- Provides positioning recommendations

### Shot Selection Optimization
- Compares expected values of 2PT vs 3PT shots
- Recommends optimal shot mix
- Identifies inefficient shot patterns
- Analyzes player-level shooting efficiency

## Requirements

- Python 3.7+
- pandas
- numpy
- matplotlib
- seaborn

## License

This project is for coaching and analysis purposes.
