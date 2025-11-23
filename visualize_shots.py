import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

def create_shot_chart(stats_df, grid_rows=5, grid_cols=5, 
                      show_pps=True, show_ppp=True, 
                      figsize=(14, 10), title="Shot Chart Analysis"):
    """
    Create a confusion-matrix-style shot chart showing points per shot and points per possession.
    
    Args:
        stats_df: DataFrame with zone statistics
        grid_rows: Number of rows in the grid
        grid_cols: Number of columns in the grid
        show_pps: Whether to show points per shot
        show_ppp: Whether to show points per possession
        figsize: Figure size
        title: Chart title
    """
    # Create matrices for both metrics
    pps_matrix = np.zeros((grid_rows, grid_cols))
    ppp_matrix = np.zeros((grid_rows, grid_cols))
    shot_count_matrix = np.zeros((grid_rows, grid_cols))
    
    for _, row in stats_df.iterrows():
        r = int(row['Row'])
        c = int(row['Col'])
        pps_matrix[r, c] = row['PointsPerShot']
        ppp_matrix[r, c] = row['PointsPerPossession']
        shot_count_matrix[r, c] = row['TotalShots']
    
    # Create figure with subplots
    if show_pps and show_ppp:
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    else:
        fig, ax = plt.subplots(1, 1, figsize=(figsize[0]//2, figsize[1]))
        axes = [ax]
        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
    
    # Custom colormap (green to red, like a confusion matrix)
    colors = ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
    
    # Plot Points Per Shot
    if show_pps:
        ax1 = axes[0] if show_ppp else axes[0]
        im1 = ax1.imshow(pps_matrix, cmap=cmap, aspect='auto', vmin=0, vmax=max(3, pps_matrix.max()))
        ax1.set_title('Points Per Shot', fontsize=14, fontweight='bold', pad=15)
        ax1.set_xlabel('Court Width (X)', fontsize=12)
        ax1.set_ylabel('Court Length (Y)', fontsize=12)
        
        # Add text annotations
        for i in range(grid_rows):
            for j in range(grid_cols):
                value = pps_matrix[i, j]
                shots = shot_count_matrix[i, j]
                if shots > 0:
                    text = ax1.text(j, i, f'{value:.2f}\n({int(shots)} shots)',
                                  ha="center", va="center", color="black",
                                  fontsize=9, fontweight='bold')
                else:
                    text = ax1.text(j, i, 'No Shots',
                                  ha="center", va="center", color="gray",
                                  fontsize=8, style='italic')
        
        # Add colorbar
        cbar1 = plt.colorbar(im1, ax=ax1, fraction=0.046, pad=0.04)
        cbar1.set_label('Points Per Shot', rotation=270, labelpad=20, fontsize=11)
        
        # Set ticks
        ax1.set_xticks(range(grid_cols))
        ax1.set_yticks(range(grid_rows))
        ax1.set_xticklabels([f'Zone {i+1}' for i in range(grid_cols)])
        ax1.set_yticklabels([f'Zone {i+1}' for i in range(grid_rows)])
    
    # Plot Points Per Possession
    if show_ppp:
        ax2 = axes[1] if show_pps else axes[0]
        im2 = ax2.imshow(ppp_matrix, cmap=cmap, aspect='auto', vmin=0, vmax=max(3, ppp_matrix.max()))
        ax2.set_title('Points Per Possession', fontsize=14, fontweight='bold', pad=15)
        ax2.set_xlabel('Court Width (X)', fontsize=12)
        ax2.set_ylabel('Court Length (Y)', fontsize=12)
        
        # Add text annotations
        for i in range(grid_rows):
            for j in range(grid_cols):
                value = ppp_matrix[i, j]
                shots = shot_count_matrix[i, j]
                if shots > 0:
                    text = ax2.text(j, i, f'{value:.2f}\n({int(shots)} shots)',
                                  ha="center", va="center", color="black",
                                  fontsize=9, fontweight='bold')
                else:
                    text = ax2.text(j, i, 'No Shots',
                                  ha="center", va="center", color="gray",
                                  fontsize=8, style='italic')
        
        # Add colorbar
        cbar2 = plt.colorbar(im2, ax=ax2, fraction=0.046, pad=0.04)
        cbar2.set_label('Points Per Possession', rotation=270, labelpad=20, fontsize=11)
        
        # Set ticks
        ax2.set_xticks(range(grid_cols))
        ax2.set_yticks(range(grid_rows))
        ax2.set_xticklabels([f'Zone {i+1}' for i in range(grid_cols)])
        ax2.set_yticklabels([f'Zone {i+1}' for i in range(grid_rows)])
    
    plt.tight_layout()
    return fig

def create_combined_shot_chart(stats_df, grid_rows=5, grid_cols=5, figsize=(16, 8)):
    """
    Create a combined shot chart with both metrics in a single visualization.
    Each cell shows both PPS and PPP.
    """
    pps_matrix = np.zeros((grid_rows, grid_cols))
    ppp_matrix = np.zeros((grid_rows, grid_cols))
    shot_count_matrix = np.zeros((grid_rows, grid_cols))
    
    for _, row in stats_df.iterrows():
        r = int(row['Row'])
        c = int(row['Col'])
        pps_matrix[r, c] = row['PointsPerShot']
        ppp_matrix[r, c] = row['PointsPerPossession']
        shot_count_matrix[r, c] = row['TotalShots']
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    
    # Use average of both metrics for color
    combined_matrix = (pps_matrix + ppp_matrix) / 2
    
    colors = ['#d73027', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('custom', colors, N=n_bins)
    
    im = ax.imshow(combined_matrix, cmap=cmap, aspect='auto', vmin=0, vmax=max(3, combined_matrix.max()))
    ax.set_title('Shot Chart: Points Per Shot & Points Per Possession', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Court Width (X)', fontsize=12)
    ax.set_ylabel('Court Length (Y)', fontsize=12)
    
    # Add text annotations with both metrics
    for i in range(grid_rows):
        for j in range(grid_cols):
            pps = pps_matrix[i, j]
            ppp = ppp_matrix[i, j]
            shots = shot_count_matrix[i, j]
            if shots > 0:
                text = ax.text(j, i, f'PPS: {pps:.2f}\nPPP: {ppp:.2f}\n({int(shots)} shots)',
                              ha="center", va="center", color="black",
                              fontsize=8, fontweight='bold',
                              bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))
            else:
                text = ax.text(j, i, 'No Shots',
                              ha="center", va="center", color="gray",
                              fontsize=8, style='italic')
    
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label('Average (PPS + PPP) / 2', rotation=270, labelpad=20, fontsize=11)
    
    ax.set_xticks(range(grid_cols))
    ax.set_yticks(range(grid_rows))
    ax.set_xticklabels([f'Zone {i+1}' for i in range(grid_cols)])
    ax.set_yticklabels([f'Zone {i+1}' for i in range(grid_rows)])
    
    plt.tight_layout()
    return fig

