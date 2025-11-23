import pandas as pd
import matplotlib.pyplot as plt
from process_shots import calculate_zone_stats
from visualize_shots import create_shot_chart, create_combined_shot_chart

def main():
    """
    Main function to process shot data and create visualizations.
    """
    # Load the shot data
    print("Loading shot data...")
    try:
        df = pd.read_csv('shots_data.csv')
        print(f"Loaded {len(df)} shots from shots_data.csv")
    except FileNotFoundError:
        print("Error: shots_data.csv not found. Please create a CSV file with your shot data.")
        print("Expected columns: GameClock, Quarter, Player, Team, ShotType, Result, X, Y, AssistBy, Distance")
        return
    
    # Validate required columns
    required_columns = ['X', 'Y', 'ShotType', 'Result']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        return
    
    # Set grid dimensions (adjust as needed)
    grid_rows = 5
    grid_cols = 5
    
    # Calculate zone statistics
    print("Calculating zone statistics...")
    stats_df = calculate_zone_stats(df, grid_rows=grid_rows, grid_cols=grid_cols)
    
    # Display summary statistics
    print("\n=== Zone Statistics Summary ===")
    print(stats_df[['Zone', 'TotalShots', 'PointsPerShot', 'PointsPerPossession', 'FieldGoalPercentage']].to_string(index=False))
    
    # Save statistics to CSV
    stats_df.to_csv('zone_statistics.csv', index=False)
    print("\nZone statistics saved to zone_statistics.csv")
    
    # Create visualizations
    print("\nCreating visualizations...")
    
    # Option 1: Side-by-side comparison
    fig1 = create_shot_chart(stats_df, grid_rows=grid_rows, grid_cols=grid_cols,
                             show_pps=True, show_ppp=True,
                             title="Basketball Shot Chart Analysis")
    fig1.savefig('shot_chart_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: shot_chart_comparison.png")
    
    # Option 2: Combined chart
    fig2 = create_combined_shot_chart(stats_df, grid_rows=grid_rows, grid_cols=grid_cols)
    fig2.savefig('shot_chart_combined.png', dpi=300, bbox_inches='tight')
    print("Saved: shot_chart_combined.png")
    
    # Option 3: Points Per Shot only
    fig3 = create_shot_chart(stats_df, grid_rows=grid_rows, grid_cols=grid_cols,
                             show_pps=True, show_ppp=False,
                             title="Points Per Shot by Zone")
    fig3.savefig('shot_chart_pps.png', dpi=300, bbox_inches='tight')
    print("Saved: shot_chart_pps.png")
    
    # Option 4: Points Per Possession only
    fig4 = create_shot_chart(stats_df, grid_rows=grid_rows, grid_cols=grid_cols,
                             show_pps=False, show_ppp=True,
                             title="Points Per Possession by Zone")
    fig4.savefig('shot_chart_ppp.png', dpi=300, bbox_inches='tight')
    print("Saved: shot_chart_ppp.png")
    
    print("\nAll visualizations created successfully!")
    print("\nNote: The court is divided into a grid where:")
    print(f"  - Rows represent zones along the court length (Y-axis)")
    print(f"  - Columns represent zones along the court width (X-axis)")
    print(f"  - Each cell shows the metric value and number of shots taken")
    
    # Show the plots
    plt.show()

if __name__ == "__main__":
    main()

