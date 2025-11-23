import pandas as pd
import numpy as np

def assign_zone(x, y, court_width=94, court_length=50, grid_rows=5, grid_cols=5):
    """
    Assign a shot to a zone based on X, Y coordinates.
    Assumes X is horizontal (0-94 feet) and Y is vertical (0-50 feet).
    Creates a grid similar to a confusion matrix.
    
    Args:
        x: X coordinate of the shot
        y: Y coordinate of the shot
        court_width: Width of the court (default 94 feet)
        court_length: Length of the court (default 50 feet)
        grid_rows: Number of rows in the grid
        grid_cols: Number of columns in the grid
    
    Returns:
        tuple: (row, col) zone coordinates
    """
    # Normalize coordinates to 0-1 range
    x_norm = max(0, min(1, x / court_width))
    y_norm = max(0, min(1, y / court_length))
    
    # Convert to grid indices (0-based)
    col = int(x_norm * grid_cols)
    row = int(y_norm * grid_rows)
    
    # Ensure indices are within bounds
    col = min(col, grid_cols - 1)
    row = min(row, grid_rows - 1)
    
    return (row, col)

def calculate_zone_stats(df, court_width=94, court_length=50, grid_rows=5, grid_cols=5):
    """
    Calculate points per possession and points per shot for each zone.
    
    Args:
        df: DataFrame with shot data
        court_width: Width of the court
        court_length: Length of the court
        grid_rows: Number of rows in the grid
        grid_cols: Number of columns in the grid
    
    Returns:
        DataFrame with zone statistics
    """
    # Create a copy to avoid modifying original
    df = df.copy()
    
    # Assign zones to each shot
    df['Zone'] = df.apply(lambda row: assign_zone(row['X'], row['Y'], 
                                                   court_width, court_length,
                                                   grid_rows, grid_cols), axis=1)
    
    # Calculate points for each shot
    # Initialize all points to 0
    df['Points'] = 0
    
    # 3PT shots made = 3 points
    df.loc[df['ShotType'].str.contains('3PT', na=False) & (df['Result'] == 'Made'), 'Points'] = 3
    
    # Other shots made = 2 points
    df.loc[~df['ShotType'].str.contains('3PT', na=False) & (df['Result'] == 'Made'), 'Points'] = 2
    
    # Missed shots = 0 points (already set, but explicit for clarity)
    df.loc[df['Result'] != 'Made', 'Points'] = 0
    
    # Group by zone and calculate statistics
    zone_stats = []
    
    for row_idx in range(grid_rows):
        for col_idx in range(grid_cols):
            zone_shots = df[df['Zone'] == (row_idx, col_idx)]
            
            if len(zone_shots) > 0:
                total_shots = len(zone_shots)
                made_shots = len(zone_shots[zone_shots['Result'] == 'Made'])
                total_points = zone_shots['Points'].sum()
                
                # Points per shot
                pps = total_points / total_shots if total_shots > 0 else 0
                
                # Points per possession (assuming each shot is a possession)
                # In real basketball, possessions can end without shots, but for this dataset
                # we'll treat each shot as a possession
                ppp = total_points / total_shots if total_shots > 0 else 0
                
                zone_stats.append({
                    'Row': row_idx,
                    'Col': col_idx,
                    'Zone': f"({row_idx},{col_idx})",
                    'TotalShots': total_shots,
                    'MadeShots': made_shots,
                    'MissedShots': total_shots - made_shots,
                    'TotalPoints': total_points,
                    'PointsPerShot': round(pps, 2),
                    'PointsPerPossession': round(ppp, 2),
                    'FieldGoalPercentage': round(made_shots / total_shots * 100, 1) if total_shots > 0 else 0
                })
            else:
                zone_stats.append({
                    'Row': row_idx,
                    'Col': col_idx,
                    'Zone': f"({row_idx},{col_idx})",
                    'TotalShots': 0,
                    'MadeShots': 0,
                    'MissedShots': 0,
                    'TotalPoints': 0,
                    'PointsPerShot': 0.0,
                    'PointsPerPossession': 0.0,
                    'FieldGoalPercentage': 0.0
                })
    
    return pd.DataFrame(zone_stats)

def create_zone_matrix(stats_df, grid_rows=5, grid_cols=5, metric='PointsPerShot'):
    """
    Create a matrix representation of zone statistics.
    
    Args:
        stats_df: DataFrame with zone statistics
        grid_rows: Number of rows in the grid
        grid_cols: Number of columns in the grid
        metric: Which metric to use ('PointsPerShot' or 'PointsPerPossession')
    
    Returns:
        numpy array with shape (grid_rows, grid_cols)
    """
    matrix = np.zeros((grid_rows, grid_cols))
    
    for _, row in stats_df.iterrows():
        r = int(row['Row'])
        c = int(row['Col'])
        matrix[r, c] = row[metric]
    
    return matrix

