import pandas as pd
import numpy as np
from typing import Dict, Tuple, List

class GameAnalyzer:
    """Analyzes basketball game statistics for coaching insights."""
    
    def __init__(self, team_box_score_path: str, player_stats_path: str, 
                 our_team: str = "Harker", opponent_team: str = "Aptos"):
        """
        Initialize the game analyzer.
        
        Args:
            team_box_score_path: Path to team box score CSV
            player_stats_path: Path to player statistics CSV
            our_team: Name of our team
            opponent_team: Name of opponent team
        """
        self.our_team = our_team
        self.opponent_team = opponent_team
        self.team_df = pd.read_csv(team_box_score_path)
        self.player_df = pd.read_csv(player_stats_path)
        
        # Filter our team and opponent data
        self.our_team_stats = self.team_df[self.team_df['Team'] == our_team].iloc[0]
        self.opponent_stats = self.team_df[self.team_df['Team'] == opponent_team].iloc[0]
        self.our_players = self.player_df[self.player_df['Team'] == 'home'].copy()
        
        # Calculate possessions
        self.our_possessions = self._calculate_possessions(self.our_team_stats)
        self.opponent_possessions = self._calculate_possessions(self.opponent_stats)
    
    def _calculate_possessions(self, team_stats: pd.Series) -> float:
        """
        Calculate total possessions using the standard formula:
        Possessions = FGA - ORB + TO + (0.44 * FTA)
        """
        fga = team_stats['FG Attempts']
        orb = team_stats['Offensive Rebounds']
        to = team_stats['Turnovers']
        fta = team_stats['FT Att']
        
        possessions = fga - orb + to + (0.44 * fta)
        return possessions
    
    def calculate_efficiency_metrics(self) -> Dict:
        """Calculate comprehensive efficiency metrics."""
        our = self.our_team_stats
        opp = self.opponent_stats
        
        # Points per possession (already in data, but recalculate for consistency)
        our_ppp = our['Points'] / self.our_possessions if self.our_possessions > 0 else 0
        opp_ppp = opp['Points'] / self.opponent_possessions if self.opponent_possessions > 0 else 0
        
        # Points per shot
        our_pps = our['Points'] / our['FG Attempts'] if our['FG Attempts'] > 0 else 0
        opp_pps = opp['Points'] / opp['FG Attempts'] if opp['FG Attempts'] > 0 else 0
        
        # Effective field goal percentage
        our_efg = our['Effective Field Goal%'] / 100 if pd.notna(our['Effective Field Goal%']) else 0
        opp_efg = opp['Effective Field Goal%'] / 100 if pd.notna(opp['Effective Field Goal%']) else 0
        
        # True shooting percentage
        our_ts = our['True Shooting%'] / 100 if pd.notna(our['True Shooting%']) else 0
        opp_ts = opp['True Shooting%'] / 100 if pd.notna(opp['True Shooting%']) else 0
        
        # 2PT vs 3PT efficiency
        our_2pt_fgm = our['2FG Made']
        our_2pt_fga = our['2FG Attempts']
        our_3pt_fgm = our['3FG Made']
        our_3pt_fga = our['3FG Attempts']
        
        our_2pt_pct = (our_2pt_fgm / our_2pt_fga * 100) if our_2pt_fga > 0 else 0
        our_3pt_pct = (our_3pt_fgm / our_3pt_fga * 100) if our_3pt_fga > 0 else 0
        
        # Expected points per shot
        our_2pt_pps = our_2pt_pct / 100 * 2  # Expected value of a 2PT shot
        our_3pt_pps = our_3pt_pct / 100 * 3  # Expected value of a 3PT shot
        
        return {
            'our_team': {
                'points': our['Points'],
                'possessions': round(self.our_possessions, 2),
                'ppp': round(our_ppp, 3),
                'pps': round(our_pps, 3),
                'efg': round(our_efg * 100, 2),
                'ts': round(our_ts * 100, 2),
                '2pt_fgm': our_2pt_fgm,
                '2pt_fga': our_2pt_fga,
                '2pt_pct': round(our_2pt_pct, 2),
                '2pt_pps': round(our_2pt_pps, 3),
                '3pt_fgm': our_3pt_fgm,
                '3pt_fga': our_3pt_fga,
                '3pt_pct': round(our_3pt_pct, 2),
                '3pt_pps': round(our_3pt_pps, 3),
            },
            'opponent': {
                'points': opp['Points'],
                'possessions': round(self.opponent_possessions, 2),
                'ppp': round(opp_ppp, 3),
                'pps': round(opp_pps, 3),
                'efg': round(opp_efg * 100, 2),
                'ts': round(opp_ts * 100, 2),
            }
        }
    
    def analyze_turnovers(self) -> Dict:
        """Analyze turnovers and provide reduction strategies."""
        our_to = self.our_team_stats['Turnovers']
        opp_to = self.opponent_stats['Turnovers']
        our_ast_to_ratio = self.our_team_stats['AST-TO Ratio']
        our_turnover_pct = self.our_team_stats['Turnover%']
        
        # Turnover rate per possession
        our_to_rate = (our_to / self.our_possessions * 100) if self.our_possessions > 0 else 0
        opp_to_rate = (opp_to / self.opponent_possessions * 100) if self.opponent_possessions > 0 else 0
        
        # Player turnover analysis
        player_turnovers = []
        for _, player in self.our_players.iterrows():
            if pd.notna(player['Basic:TO']) and player['Basic:TO'] > 0:
                minutes = self._parse_minutes(player['Basic:MP'])
                to_per_36 = (player['Basic:TO'] / minutes * 36) if minutes > 0 else 0
                ast_to = player['Advanced:AST/TO'] if pd.notna(player['Advanced:AST/TO']) else 0
                usage = player['Advanced:USG%'] if pd.notna(player['Advanced:USG%']) else 0
                
                player_turnovers.append({
                    'player': player['Athlete'],
                    'number': player['#'],
                    'turnovers': player['Basic:TO'],
                    'to_per_36': round(to_per_36, 2),
                    'ast_to_ratio': round(ast_to, 2),
                    'usage': round(usage, 2),
                    'minutes': minutes
                })
        
        player_turnovers.sort(key=lambda x: x['turnovers'], reverse=True)
        
        # Calculate potential points lost from turnovers
        # Average possession value = PPP
        our_ppp = self.our_team_stats['Points Per Possession']
        potential_points_lost = our_to * our_ppp
        
        # Recommendations
        recommendations = []
        if our_to_rate > 20:
            recommendations.append("CRITICAL: Turnover rate is very high (>20%). Focus on ball security.")
        elif our_to_rate > 15:
            recommendations.append("WARNING: Turnover rate is elevated (>15%). Improve decision-making.")
        
        if our_ast_to_ratio < 1.0:
            recommendations.append("Low assist-to-turnover ratio. Focus on better passing and court vision.")
        
        if len(player_turnovers) > 0 and player_turnovers[0]['to_per_36'] > 5:
            top_to_player = player_turnovers[0]
            recommendations.append(f"High turnover rate from {top_to_player['player']} (#{top_to_player['number']}). Provide extra support on ball handling.")
        
        return {
            'our_turnovers': int(our_to),
            'opponent_turnovers': int(opp_to),
            'our_to_rate': round(our_to_rate, 2),
            'opp_to_rate': round(opp_to_rate, 2),
            'our_ast_to_ratio': round(our_ast_to_ratio, 2),
            'our_turnover_pct': round(our_turnover_pct, 2),
            'potential_points_lost': round(potential_points_lost, 2),
            'top_turnover_players': player_turnovers[:5],
            'recommendations': recommendations
        }
    
    def analyze_rebounding(self) -> Dict:
        """Analyze rebounding performance and opponent rebounding ability."""
        our = self.our_team_stats
        opp = self.opponent_stats
        
        # Rebounding percentages
        our_orb_pct = our['Offensive Rebounding%']
        our_drb_pct = our['Defensive Rebounding%']
        opp_orb_pct = opp['Offensive Rebounding%']
        opp_drb_pct = opp['Defensive Rebounding%']
        
        # Total rebounds
        our_reb = our['Rebounds']
        opp_reb = opp['Rebounds']
        our_orb = our['Offensive Rebounds']
        our_drb = our['Defensive Rebounds']
        opp_orb = opp['Offensive Rebounds']
        opp_drb = opp['Defensive Rebounds']
        
        # Second chance opportunities
        # Estimate: offensive rebounds lead to second chance points
        our_second_chance_opps = our_orb
        opp_second_chance_opps = opp_orb
        
        # Rebounding battle
        rebound_margin = our_reb - opp_reb
        orb_margin = our_orb - opp_orb
        
        # Player rebounding analysis
        player_rebounds = []
        for _, player in self.our_players.iterrows():
            if pd.notna(player['Basic:TRB']) and player['Basic:TRB'] > 0:
                minutes = self._parse_minutes(player['Basic:MP'])
                reb_per_36 = (player['Basic:TRB'] / minutes * 36) if minutes > 0 else 0
                orb_pct = player['Advanced:ORB%'] if pd.notna(player['Advanced:ORB%']) else 0
                drb_pct = player['Advanced:DRB%'] if pd.notna(player['Advanced:DRB%']) else 0
                
                player_rebounds.append({
                    'player': player['Athlete'],
                    'number': player['#'],
                    'total_reb': player['Basic:TRB'],
                    'orb': player['Basic:ORB'],
                    'drb': player['Basic:DRB'],
                    'reb_per_36': round(reb_per_36, 2),
                    'orb_pct': round(orb_pct, 2),
                    'drb_pct': round(drb_pct, 2),
                    'minutes': minutes
                })
        
        player_rebounds.sort(key=lambda x: x['total_reb'], reverse=True)
        
        # Recommendations
        recommendations = []
        if our_orb_pct < 25:
            recommendations.append("Offensive rebounding below average (<25%). Focus on boxing out and crashing the boards.")
        
        if opp_orb_pct > 35:
            recommendations.append(f"ALERT: Opponent offensive rebounding is strong ({opp_orb_pct:.1f}%). Defensive box-outs critical.")
        
        if rebound_margin < -5:
            recommendations.append("Losing the rebounding battle significantly. Emphasize rebounding fundamentals.")
        
        if orb_margin < -3:
            recommendations.append("Giving up too many offensive rebounds. Improve defensive positioning.")
        
        return {
            'our_team': {
                'total_rebounds': int(our_reb),
                'offensive_rebounds': int(our_orb),
                'defensive_rebounds': int(our_drb),
                'orb_pct': round(our_orb_pct, 2),
                'drb_pct': round(our_drb_pct, 2),
            },
            'opponent': {
                'total_rebounds': int(opp_reb),
                'offensive_rebounds': int(opp_orb),
                'defensive_rebounds': int(opp_drb),
                'orb_pct': round(opp_orb_pct, 2),
                'drb_pct': round(opp_drb_pct, 2),
            },
            'rebound_margin': int(rebound_margin),
            'orb_margin': int(orb_margin),
            'second_chance_opps': {
                'our_team': int(our_second_chance_opps),
                'opponent': int(opp_second_chance_opps)
            },
            'top_rebounders': player_rebounds[:5],
            'recommendations': recommendations
        }
    
    def optimize_shot_selection(self) -> Dict:
        """Analyze shot selection and identify optimal zones."""
        our = self.our_team_stats
        
        # Calculate expected values
        our_2pt_pct = our['2FG%'] / 100
        our_3pt_pct = our['3FG%'] / 100
        our_2pt_expected = our_2pt_pct * 2
        our_3pt_expected = our_3pt_pct * 3
        
        # Shot distribution
        total_fga = our['FG Attempts']
        our_2pt_rate = our['2FG Attempts'] / total_fga if total_fga > 0 else 0
        our_3pt_rate = our['3FG Att'] / total_fga if total_fga > 0 else 0
        
        # Optimal shot mix (if 3PT expected value > 2PT expected value, shoot more 3s)
        optimal_mix = {}
        if our_3pt_expected > our_2pt_expected:
            optimal_mix['recommendation'] = "Increase 3-point attempts"
            optimal_mix['reason'] = f"3PT expected value ({our_3pt_expected:.2f}) > 2PT expected value ({our_2pt_expected:.2f})"
        else:
            optimal_mix['recommendation'] = "Focus on high-percentage 2-point shots"
            optimal_mix['reason'] = f"2PT expected value ({our_2pt_expected:.2f}) > 3PT expected value ({our_3pt_expected:.2f})"
        
        # Player shot analysis
        player_shots = []
        for _, player in self.our_players.iterrows():
            if pd.notna(player['Basic:FGA']) and player['Basic:FGA'] > 0:
                # Handle potential string values - convert to float safely
                def safe_float(val, default=0):
                    if pd.isna(val) or val == '—' or val == '':
                        return default
                    try:
                        return float(val)
                    except (ValueError, TypeError):
                        return default
                
                fg_pct = safe_float(player.get('Basic:FG%', 0), 0)
                efg = safe_float(player.get('Shooting:eFG%', 0), 0)
                ts = safe_float(player.get('Shooting:TS%', 0), 0)
                usage = safe_float(player.get('Advanced:USG%', 0), 0)
                
                player_shots.append({
                    'player': player['Athlete'],
                    'number': player['#'],
                    'fga': int(player['Basic:FGA']) if pd.notna(player['Basic:FGA']) else 0,
                    'fgm': int(player['Basic:FGM']) if pd.notna(player['Basic:FGM']) else 0,
                    'fg_pct': round(fg_pct * 100, 2) if fg_pct > 0 else 0,
                    'efg': round(efg, 2),
                    'ts': round(ts, 2),
                    'usage': round(usage, 2),
                })
        
        player_shots.sort(key=lambda x: x['fga'], reverse=True)
        
        # Recommendations
        recommendations = []
        if our_3pt_pct < 0.30 and our_3pt_rate > 0.50:
            recommendations.append("3-point shooting is inefficient (<30%) but high volume (>50%). Reduce 3PT attempts or improve shooters.")
        
        if our_2pt_pct < 0.40:
            recommendations.append("2-point shooting below 40%. Focus on shot selection and quality looks.")
        
        return {
            '2pt_expected_value': round(our_2pt_expected, 3),
            '3pt_expected_value': round(our_3pt_expected, 3),
            'current_2pt_rate': round(our_2pt_rate * 100, 2),
            'current_3pt_rate': round(our_3pt_rate * 100, 2),
            'optimal_mix': optimal_mix,
            'top_shooters': player_shots[:5],
            'recommendations': recommendations
        }
    
    def _parse_minutes(self, time_str: str) -> float:
        """Parse minutes from MM:SS format."""
        if pd.isna(time_str) or time_str == '—':
            return 0.0
        try:
            parts = str(time_str).split(':')
            if len(parts) == 2:
                minutes = int(parts[0])
                seconds = int(parts[1])
                return minutes + seconds / 60.0
            return 0.0
        except:
            return 0.0

