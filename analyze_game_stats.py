#!/usr/bin/env python3
"""
Main script to analyze game statistics and generate coach's report.
Usage: python analyze_game_stats.py [team_box_score.csv] [player_stats.csv]
"""

import sys
import os
from analyze_game import GameAnalyzer
from generate_gamma_prompt import GammaPromptGenerator

def main():
    """Main function to run game analysis."""
    
    # Default file paths (can be overridden via command line)
    if len(sys.argv) >= 3:
        team_box_score_path = sys.argv[1]
        player_stats_path = sys.argv[2]
    else:
        # Try to find files in Downloads or current directory
        downloads_path = os.path.expanduser("~/Downloads")
        team_box_score_path = os.path.join(downloads_path, "2025-10-21 Harker vs Aptos -team-box-score.csv")
        player_stats_path = os.path.join(downloads_path, "2025-10-21 Harker vs Aptos stats.csv")
        
        # Check if files exist
        if not os.path.exists(team_box_score_path):
            print("Error: Team box score file not found.")
            print("Usage: python analyze_game_stats.py [team_box_score.csv] [player_stats.csv]")
            print(f"Looking for: {team_box_score_path}")
            return
        
        if not os.path.exists(player_stats_path):
            print("Error: Player stats file not found.")
            print("Usage: python analyze_game_stats.py [team_box_score.csv] [player_stats.csv]")
            print(f"Looking for: {player_stats_path}")
            return
    
    print("=" * 70)
    print("BASKETBALL GAME ANALYSIS SYSTEM")
    print("=" * 70)
    print(f"\nLoading game data...")
    print(f"Team Box Score: {team_box_score_path}")
    print(f"Player Statistics: {player_stats_path}")
    
    try:
        # Initialize analyzer
        analyzer = GameAnalyzer(
            team_box_score_path=team_box_score_path,
            player_stats_path=player_stats_path,
            our_team="Harker",
            opponent_team="Aptos"
        )
        
        print(f"\n✓ Successfully loaded game data")
        print(f"  Our Team: {analyzer.our_team}")
        print(f"  Opponent: {analyzer.opponent_team}")
        print(f"  Our Possessions: {analyzer.our_possessions:.1f}")
        print(f"  Opponent Possessions: {analyzer.opponent_possessions:.1f}")
        
        # Calculate metrics
        print("\n" + "=" * 70)
        print("CALCULATING EFFICIENCY METRICS...")
        print("=" * 70)
        
        efficiency = analyzer.calculate_efficiency_metrics()
        our = efficiency['our_team']
        opp = efficiency['opponent']
        
        print(f"\nPoints Per Possession:")
        print(f"  {analyzer.our_team}: {our['ppp']:.3f}")
        print(f"  {analyzer.opponent_team}: {opp['ppp']:.3f}")
        print(f"  Difference: {our['ppp'] - opp['ppp']:+.3f}")
        
        print(f"\nPoints Per Shot:")
        print(f"  {analyzer.our_team}: {our['pps']:.3f}")
        print(f"  {analyzer.opponent_team}: {opp['pps']:.3f}")
        
        print(f"\nShooting Efficiency:")
        print(f"  Effective FG%: {our['efg']:.1f}% (vs {opp['efg']:.1f}%)")
        print(f"  True Shooting%: {our['ts']:.1f}% (vs {opp['ts']:.1f}%)")
        
        # Turnover analysis
        print("\n" + "=" * 70)
        print("TURNOVER ANALYSIS...")
        print("=" * 70)
        
        turnovers = analyzer.analyze_turnovers()
        print(f"\nTurnover Statistics:")
        print(f"  Our Turnovers: {turnovers['our_turnovers']} (Rate: {turnovers['our_to_rate']:.1f}%)")
        print(f"  Opponent Turnovers: {turnovers['opponent_turnovers']} (Rate: {turnovers['opp_to_rate']:.1f}%)")
        print(f"  Assist-to-Turnover Ratio: {turnovers['our_ast_to_ratio']:.2f}")
        print(f"  Potential Points Lost: {turnovers['potential_points_lost']:.1f}")
        
        if turnovers['top_turnover_players']:
            print(f"\nTop Turnover Contributors:")
            for player in turnovers['top_turnover_players'][:3]:
                print(f"  {player['player']} (#{player['number']}): {player['turnovers']} TOs ({player['to_per_36']:.1f} per 36 min)")
        
        # Rebounding analysis
        print("\n" + "=" * 70)
        print("REBOUNDING ANALYSIS...")
        print("=" * 70)
        
        rebounding = analyzer.analyze_rebounding()
        print(f"\nRebounding Statistics:")
        print(f"  Total Rebound Margin: {rebounding['rebound_margin']:+d}")
        print(f"  Offensive Rebounds: {rebounding['our_team']['offensive_rebounds']} (Opponent: {rebounding['opponent']['offensive_rebounds']})")
        print(f"  Offensive Rebound%: {rebounding['our_team']['orb_pct']:.1f}% (Opponent: {rebounding['opponent']['orb_pct']:.1f}%)")
        print(f"  Defensive Rebound%: {rebounding['our_team']['drb_pct']:.1f}% (Opponent: {rebounding['opponent']['drb_pct']:.1f}%)")
        
        if rebounding['top_rebounders']:
            print(f"\nTop Rebounders:")
            for player in rebounding['top_rebounders'][:3]:
                print(f"  {player['player']} (#{player['number']}): {player['total_reb']} REB ({player['reb_per_36']:.1f} per 36 min)")
        
        # Shot optimization
        print("\n" + "=" * 70)
        print("SHOT SELECTION OPTIMIZATION...")
        print("=" * 70)
        
        shot_selection = analyzer.optimize_shot_selection()
        print(f"\nExpected Values:")
        print(f"  2PT Expected Points Per Shot: {shot_selection['2pt_expected_value']:.3f}")
        print(f"  3PT Expected Points Per Shot: {shot_selection['3pt_expected_value']:.3f}")
        print(f"\nCurrent Distribution:")
        print(f"  2PT Attempts: {shot_selection['current_2pt_rate']:.1f}%")
        print(f"  3PT Attempts: {shot_selection['current_3pt_rate']:.1f}%")
        print(f"\nRecommendation: {shot_selection['optimal_mix']['recommendation']}")
        print(f"  {shot_selection['optimal_mix']['reason']}")
        
        # Generate Gamma prompt
        print("\n" + "=" * 70)
        print("GENERATING GAMMA PROMPT...")
        print("=" * 70)
        
        prompt_generator = GammaPromptGenerator(analyzer)
        
        # Generate detailed Gamma prompt
        gamma_prompt_path = "gamma_report_prompt.txt"
        print(f"\nGenerating Gamma prompt: {gamma_prompt_path}")
        gamma_prompt = prompt_generator.generate_full_prompt()
        with open(gamma_prompt_path, 'w', encoding='utf-8') as f:
            f.write(gamma_prompt)
        print(f"✓ Gamma prompt saved: {gamma_prompt_path}")
        
        # Generate text summary
        summary_path = "game_summary.txt"
        print(f"\nGenerating quick summary: {summary_path}")
        summary = f"""
GAME ANALYSIS SUMMARY
{analyzer.our_team} vs {analyzer.opponent_team}
Final Score: {our['points']} - {opp['points']}

EFFICIENCY METRICS:
• Points Per Possession: {our['ppp']:.3f} (Opponent: {opp['ppp']:.3f})
• Points Per Shot: {our['pps']:.3f} (Opponent: {opp['pps']:.3f})
• Effective FG%: {our['efg']:.1f}% (Opponent: {opp['efg']:.1f}%)

TURNOVERS:
• Our Turnovers: {turnovers['our_turnovers']} (Rate: {turnovers['our_to_rate']:.1f}%)
• Potential Points Lost: {turnovers['potential_points_lost']:.1f}

REBOUNDING:
• Rebound Margin: {rebounding['rebound_margin']:+d}
• Offensive Rebound%: {rebounding['our_team']['orb_pct']:.1f}% vs {rebounding['opponent']['orb_pct']:.1f}%

SHOT OPTIMIZATION:
• 2PT Expected Value: {shot_selection['2pt_expected_value']:.3f}
• 3PT Expected Value: {shot_selection['3pt_expected_value']:.3f}
• Recommendation: {shot_selection['optimal_mix']['recommendation']}
"""
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        print(f"✓ Text summary saved: {summary_path}")
        
        # Print summary to console
        print("\n" + "=" * 70)
        print("QUICK SUMMARY")
        print("=" * 70)
        print(summary)
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE!")
        print("=" * 70)
        print(f"\nFiles generated:")
        print(f"  • {gamma_prompt_path} - Detailed prompt for Gamma (upload to Gamma.app)")
        print(f"  • {summary_path} - Quick text summary")
        print(f"\nNext steps:")
        print(f"  1. Open {gamma_prompt_path}")
        print(f"  2. Copy the content")
        print(f"  3. Go to Gamma.app and create a new presentation")
        print(f"  4. Paste the content to generate a beautiful graphical report")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())

