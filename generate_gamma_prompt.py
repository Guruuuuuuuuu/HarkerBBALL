"""
Generates a detailed prompt/text for Gamma to create a graphical coaching report.
Gamma is a presentation tool that can create beautiful reports from structured text.
"""

import pandas as pd
from analyze_game import GameAnalyzer
from typing import Dict

class GammaPromptGenerator:
    """Generates detailed prompts for Gamma presentation tool."""
    
    def __init__(self, analyzer: GameAnalyzer):
        self.analyzer = analyzer
        self.efficiency = analyzer.calculate_efficiency_metrics()
        self.turnovers = analyzer.analyze_turnovers()
        self.rebounding = analyzer.analyze_rebounding()
        self.shot_selection = analyzer.optimize_shot_selection()
    
    def generate_full_prompt(self) -> str:
        """Generate a comprehensive prompt for Gamma with all analysis sections."""
        
        our = self.efficiency['our_team']
        opp = self.efficiency['opponent']
        
        prompt = f"""# Basketball Game Analysis Report: {self.analyzer.our_team} vs {self.analyzer.opponent_team}

## Game Overview
**Final Score:** {self.analyzer.our_team} {our['points']} - {opp['points']} {self.analyzer.opponent_team}
**Date:** Game Analysis Report
**Total Possessions:** {our['possessions']:.0f} vs {opp['possessions']:.0f}

---

## 1. Executive Summary

### Key Performance Metrics

**Points Per Possession (PPP)**
- {self.analyzer.our_team}: {our['ppp']:.3f}
- {self.analyzer.opponent_team}: {opp['ppp']:.3f}
- **Difference:** {our['ppp'] - opp['ppp']:+.3f} ({'Advantage: ' + self.analyzer.our_team if our['ppp'] > opp['ppp'] else 'Advantage: ' + self.analyzer.opponent_team})

**Points Per Shot (PPS)**
- {self.analyzer.our_team}: {our['pps']:.3f}
- {self.analyzer.opponent_team}: {opp['pps']:.3f}
- **Difference:** {our['pps'] - opp['pps']:+.3f} ({'Advantage: ' + self.analyzer.our_team if our['pps'] > opp['pps'] else 'Advantage: ' + self.analyzer.opponent_team})

**Shooting Efficiency**
- Effective Field Goal%: {our['efg']:.1f}% vs {opp['efg']:.1f}%
- True Shooting%: {our['ts']:.1f}% vs {opp['ts']:.1f}%

### Win/Loss Factors

{self._generate_win_loss_factors()}

---

## 2. Efficiency Analysis

### Offensive Efficiency Breakdown

**Field Goal Shooting:**
- Total FGM/FGA: {our['2pt_fgm'] + our['3pt_fgm']}/{our['2pt_fga'] + our['3pt_fga']}
- 2PT Shooting: {our['2pt_fgm']}/{our['2pt_fga']} ({our['2pt_pct']:.1f}%)
- 3PT Shooting: {our['3pt_fgm']}/{our['3pt_fga']} ({our['3pt_pct']:.1f}%)
- Free Throws: {self.analyzer.our_team_stats.get('FT Made', 'N/A')}/{self.analyzer.our_team_stats.get('FT Att', 'N/A')} ({self.analyzer.our_team_stats.get('FT%', 0):.1f}%)

**Expected Values (Points Per Shot):**
- 2PT Expected Value: {our['2pt_pps']:.3f} points per shot
- 3PT Expected Value: {our['3pt_pps']:.3f} points per shot
- **Key Insight:** {'3-point shots are more efficient' if our['3pt_pps'] > our['2pt_pps'] else '2-point shots are more efficient'}

### Comparison with Opponent

| Metric | {self.analyzer.our_team} | {self.analyzer.opponent_team} | Advantage |
|--------|--------------------------|-------------------------------|-----------|
| Points Per Possession | {our['ppp']:.3f} | {opp['ppp']:.3f} | {self.analyzer.our_team if our['ppp'] > opp['ppp'] else self.analyzer.opponent_team} |
| Points Per Shot | {our['pps']:.3f} | {opp['pps']:.3f} | {self.analyzer.our_team if our['pps'] > opp['pps'] else self.analyzer.opponent_team} |
| Effective FG% | {our['efg']:.1f}% | {opp['efg']:.1f}% | {self.analyzer.our_team if our['efg'] > opp['efg'] else self.analyzer.opponent_team} |
| True Shooting% | {our['ts']:.1f}% | {opp['ts']:.1f}% | {self.analyzer.our_team if our['ts'] > opp['ts'] else self.analyzer.opponent_team} |

---

## 3. Turnover Analysis & Reduction Strategy

### Turnover Statistics

**Team Turnover Metrics:**
- {self.analyzer.our_team} Turnovers: {self.turnovers['our_turnovers']} (Rate: {self.turnovers['our_to_rate']:.1f}%)
- {self.analyzer.opponent_team} Turnovers: {self.turnovers['opponent_turnovers']} (Rate: {self.turnovers['opp_to_rate']:.1f}%)
- **Turnover Margin:** {self.turnovers['our_turnovers'] - self.turnovers['opponent_turnovers']:+d} ({'Better' if self.turnovers['our_to_rate'] < self.turnovers['opp_to_rate'] else 'Needs Improvement'})

**Ball Security:**
- Assist-to-Turnover Ratio: {self.turnovers['our_ast_to_ratio']:.2f} ({'Good' if self.turnovers['our_ast_to_ratio'] >= 1.0 else 'Needs Improvement'})
- Potential Points Lost from Turnovers: {self.turnovers['potential_points_lost']:.1f} points

### Top Turnover Contributors

{self._format_turnover_players()}

### Turnover Reduction Recommendations

{self._format_turnover_recommendations()}

---

## 4. Rebounding Analysis & Opponent Assessment

### Rebounding Battle

**Total Rebounding:**
- {self.analyzer.our_team}: {self.rebounding['our_team']['total_rebounds']} rebounds
- {self.analyzer.opponent_team}: {self.rebounding['opponent']['total_rebounds']} rebounds
- **Rebound Margin:** {self.rebounding['rebound_margin']:+d} ({'Won the rebounding battle' if self.rebounding['rebound_margin'] > 0 else 'Lost the rebounding battle'})

**Offensive Rebounding:**
- {self.analyzer.our_team} ORB: {self.rebounding['our_team']['offensive_rebounds']} ({self.rebounding['our_team']['orb_pct']:.1f}% of available)
- {self.analyzer.opponent_team} ORB: {self.rebounding['opponent']['offensive_rebounds']} ({self.rebounding['opponent']['orb_pct']:.1f}% of available)
- **Second Chance Opportunities:** {self.rebounding['second_chance_opps']['our_team']} vs {self.rebounding['second_chance_opps']['opponent']}

**Defensive Rebounding:**
- {self.analyzer.our_team} DRB%: {self.rebounding['our_team']['drb_pct']:.1f}%
- {self.analyzer.opponent_team} DRB%: {self.rebounding['opponent']['drb_pct']:.1f}%

### Opponent Rebounding Assessment

**Opponent Strengths:**
- Offensive Rebounding Percentage: {self.rebounding['opponent']['orb_pct']:.1f}% ({'STRONG - Requires defensive focus' if self.rebounding['opponent']['orb_pct'] > 30 else 'Average'})
- Defensive Rebounding Percentage: {self.rebounding['opponent']['drb_pct']:.1f}% ({'Strong on defensive glass' if self.rebounding['opponent']['drb_pct'] > 70 else 'Opportunities available'})

### Top Rebounders

{self._format_rebounding_players()}

### Rebounding Recommendations

{self._format_rebounding_recommendations()}

---

## 5. Shot Selection Optimization

### Current Shot Distribution

**Shot Mix:**
- 2PT Attempts: {self.shot_selection['current_2pt_rate']:.1f}% ({our['2pt_fga']} attempts)
- 3PT Attempts: {self.shot_selection['current_3pt_rate']:.1f}% ({our['3pt_fga']} attempts)

**Expected Values Analysis:**
- 2PT Expected Points Per Shot: {self.shot_selection['2pt_expected_value']:.3f}
- 3PT Expected Points Per Shot: {self.shot_selection['3pt_expected_value']:.3f}
- **Optimal Strategy:** {self.shot_selection['optimal_mix']['recommendation']}
  - *Reason:* {self.shot_selection['optimal_mix']['reason']}

### Top Shooters

{self._format_shooting_players()}

### Shot Selection Recommendations

{self._format_shot_selection_recommendations()}

---

## 6. Player Performance Highlights

### Top Performers

{self._format_top_players()}

---

## 7. Action Items & Next Steps

### Priority Action Items

{self._format_action_items()}

### Summary Statistics for Quick Reference

- **Final Score:** {our['points']} - {opp['points']}
- **Points Per Possession:** {our['ppp']:.3f} (vs {opp['ppp']:.3f})
- **Turnover Rate:** {self.turnovers['our_to_rate']:.1f}%
- **Rebound Margin:** {self.rebounding['rebound_margin']:+d}
- **Shooting Efficiency (eFG%):** {our['efg']:.1f}%
- **Key Strength:** {self._identify_key_strength()}
- **Key Weakness:** {self._identify_key_weakness()}

---

## Visualization Recommendations for Gamma

**Suggested Charts/Graphs to Create:**

1. **Comparison Bar Chart:** Points Per Possession comparison between teams
2. **Efficiency Heatmap:** Shooting efficiency by shot type (2PT vs 3PT)
3. **Turnover Trend Chart:** Turnover rate and impact visualization
4. **Rebounding Comparison:** Side-by-side rebounding percentages
5. **Player Performance Table:** Top 5 players in key categories
6. **Shot Distribution Pie Chart:** Current 2PT vs 3PT shot distribution
7. **Expected Value Comparison:** Bar chart showing 2PT vs 3PT expected values

**Color Coding Suggestions:**
- Green: Areas where we performed better than opponent
- Red: Areas needing improvement
- Blue: Neutral/consistent performance
- Orange: Key focus areas for next game

---

*Report generated from game statistics analysis*
*Use this content in Gamma to create a visually engaging coaching presentation*
"""
        
        return prompt
    
    def _generate_win_loss_factors(self) -> str:
        """Generate win/loss factors summary."""
        our = self.efficiency['our_team']
        opp = self.efficiency['opponent']
        
        factors = []
        if our['ppp'] > opp['ppp']:
            factors.append(f"✓ Higher Points Per Possession (+{our['ppp'] - opp['ppp']:.3f})")
        else:
            factors.append(f"✗ Lower Points Per Possession ({our['ppp'] - opp['ppp']:.3f})")
        
        if self.turnovers['our_to_rate'] < self.turnovers['opp_to_rate']:
            factors.append(f"✓ Better Turnover Control (-{self.turnovers['opp_to_rate'] - self.turnovers['our_to_rate']:.1f}%)")
        else:
            factors.append(f"✗ Higher Turnover Rate (+{self.turnovers['our_to_rate'] - self.turnovers['opp_to_rate']:.1f}%)")
        
        if self.rebounding['rebound_margin'] > 0:
            factors.append(f"✓ Won Rebounding Battle (+{self.rebounding['rebound_margin']})")
        else:
            factors.append(f"✗ Lost Rebounding Battle ({self.rebounding['rebound_margin']})")
        
        if our['efg'] > opp['efg']:
            factors.append(f"✓ Better Shooting Efficiency (+{our['efg'] - opp['efg']:.1f}%)")
        else:
            factors.append(f"✗ Lower Shooting Efficiency ({our['efg'] - opp['efg']:.1f}%)")
        
        return "\n".join(f"- {f}" for f in factors)
    
    def _format_turnover_players(self) -> str:
        """Format top turnover players."""
        if not self.turnovers['top_turnover_players']:
            return "No significant turnover contributors identified."
        
        lines = []
        for i, player in enumerate(self.turnovers['top_turnover_players'][:5], 1):
            lines.append(f"{i}. **{player['player']} (#{player['number']})**: {player['turnovers']} TOs ({player['to_per_36']:.1f} per 36 min, AST/TO: {player['ast_to_ratio']:.2f})")
        
        return "\n".join(lines)
    
    def _format_turnover_recommendations(self) -> str:
        """Format turnover reduction recommendations."""
        if not self.turnovers['recommendations']:
            return "- Turnover control is within acceptable range. Maintain current focus."
        
        return "\n".join(f"- **{rec}**" for rec in self.turnovers['recommendations'])
    
    def _format_rebounding_players(self) -> str:
        """Format top rebounders."""
        if not self.rebounding['top_rebounders']:
            return "No rebounding data available."
        
        lines = []
        for i, player in enumerate(self.rebounding['top_rebounders'][:5], 1):
            lines.append(f"{i}. **{player['player']} (#{player['number']})**: {player['total_reb']} REB ({player['reb_per_36']:.1f} per 36 min) - ORB: {player['orb']}, DRB: {player['drb']}")
        
        return "\n".join(lines)
    
    def _format_rebounding_recommendations(self) -> str:
        """Format rebounding recommendations."""
        if not self.rebounding['recommendations']:
            return "- Rebounding performance is solid. Maintain current effort."
        
        return "\n".join(f"- **{rec}**" for rec in self.rebounding['recommendations'])
    
    def _format_shooting_players(self) -> str:
        """Format top shooters."""
        if not self.shot_selection['top_shooters']:
            return "No shooting data available."
        
        lines = []
        for i, player in enumerate(self.shot_selection['top_shooters'][:5], 1):
            lines.append(f"{i}. **{player['player']} (#{player['number']})**: {player['fga']} FGA, {player['fgm']} FGM ({player['fg_pct']:.1f}% FG, {player['efg']:.1f}% eFG, TS%: {player['ts']:.1f}%)")
        
        return "\n".join(lines)
    
    def _format_shot_selection_recommendations(self) -> str:
        """Format shot selection recommendations."""
        if not self.shot_selection['recommendations']:
            return "- Shot selection is well-balanced. Continue current approach."
        
        return "\n".join(f"- **{rec}**" for rec in self.shot_selection['recommendations'])
    
    def _format_top_players(self) -> str:
        """Format top performers table."""
        players_data = []
        for _, player in self.analyzer.our_players.iterrows():
            if pd.notna(player.get('Basic:MP', None)):
                minutes = self.analyzer._parse_minutes(player['Basic:MP'])
                if minutes > 0:
                    # Safely get values
                    def safe_get(key, default=0):
                        val = player.get(key, default)
                        if pd.isna(val) or val == '—' or val == '':
                            return default
                        try:
                            return float(val) if isinstance(val, (int, float, str)) and val != '—' else default
                        except:
                            return default
                    
                    players_data.append({
                        'name': player.get('Athlete', 'Unknown'),
                        'number': player.get('#', ''),
                        'minutes': minutes,
                        'points': safe_get('Basic:PTS', 0),
                        'rebounds': safe_get('Basic:TRB', 0),
                        'assists': safe_get('Basic:AST', 0),
                        'fg_pct': safe_get('Basic:FG%', 0) * 100,
                        'efg': safe_get('Shooting:eFG%', 0),
                    })
        
        players_data.sort(key=lambda x: x['points'], reverse=True)
        
        lines = ["| Player | # | MIN | PTS | REB | AST | FG% | eFG% |"]
        lines.append("|--------|---|-----|-----|-----|-----|-----|------|")
        
        for p in players_data[:8]:
            lines.append(f"| {p['name']} | {p['number']} | {p['minutes']:.1f} | {p['points']:.0f} | {p['rebounds']:.0f} | {p['assists']:.0f} | {p['fg_pct']:.1f}% | {p['efg']:.1f}% |")
        
        return "\n".join(lines)
    
    def _format_action_items(self) -> str:
        """Format action items."""
        all_recommendations = []
        
        # Efficiency recommendations
        our = self.efficiency['our_team']
        opp = self.efficiency['opponent']
        if our['ppp'] < opp['ppp']:
            all_recommendations.append(("HIGH PRIORITY", 
                f"Improve offensive efficiency: PPP {our['ppp']:.3f} vs opponent {opp['ppp']:.3f}"))
        
        # Turnover recommendations
        if self.turnovers['our_to_rate'] > 15:
            all_recommendations.append(("HIGH PRIORITY",
                f"Reduce turnovers: Current rate {self.turnovers['our_to_rate']:.1f}%"))
        all_recommendations.extend([("TURNOVERS", rec) for rec in self.turnovers['recommendations']])
        
        # Rebounding recommendations
        all_recommendations.extend([("REBOUNDING", rec) for rec in self.rebounding['recommendations']])
        
        # Shot selection recommendations
        all_recommendations.extend([("SHOT SELECTION", rec) for rec in self.shot_selection['recommendations']])
        
        lines = []
        for priority, item in all_recommendations[:15]:  # Top 15 items
            lines.append(f"- **[{priority}]** {item}")
        
        return "\n".join(lines)
    
    def _identify_key_strength(self) -> str:
        """Identify key strength."""
        our = self.efficiency['our_team']
        opp = self.efficiency['opponent']
        
        if our['efg'] > opp['efg']:
            return f"Better shooting efficiency ({our['efg']:.1f}% vs {opp['efg']:.1f}%)"
        elif self.turnovers['our_to_rate'] < self.turnovers['opp_to_rate']:
            return "Better turnover control"
        elif self.rebounding['rebound_margin'] > 0:
            return "Strong rebounding"
        else:
            return "Consistent performance across metrics"
    
    def _identify_key_weakness(self) -> str:
        """Identify key weakness."""
        our = self.efficiency['our_team']
        opp = self.efficiency['opponent']
        
        if self.rebounding['rebound_margin'] < -5:
            return f"Rebounding deficit ({self.rebounding['rebound_margin']:+d})"
        elif self.turnovers['our_to_rate'] > 20:
            return f"High turnover rate ({self.turnovers['our_to_rate']:.1f}%)"
        elif our['ppp'] < opp['ppp']:
            return f"Lower offensive efficiency ({our['ppp']:.3f} vs {opp['ppp']:.3f} PPP)"
        else:
            return "Minor areas for improvement across all metrics"

