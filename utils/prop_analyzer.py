from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from data.data_loader import NBADataLoader
import logging

logger = logging.getLogger(__name__)

class PropAnalyzer:
    @staticmethod
    def calculate_home_away_splits(
        player_id: str, 
        season: Optional[str] = None,
        last_n_games: Optional[int] = None
    ) -> Dict:
        """
        Calculate performance splits between home and away games.
        
        Args:
            player_id: NBA player ID
            season: Optional season in format '2023-24'. If None, uses current season
            last_n_games: Optional, analyze only the last N games. If None, analyzes all games
        """
        try:
            game_logs = NBADataLoader.get_player_game_logs(player_id, season)
            logger.info(f"Retrieved game logs for player {player_id}")
            
            if not game_logs or 'resultSets' not in game_logs:
                logger.error(f"Invalid game logs format: {game_logs}")
                raise ValueError("Invalid game logs data received from NBA API")
            
            # Extract the actual game data
            try:
                headers = game_logs['resultSets'][0]['headers']
                rows = game_logs['resultSets'][0]['rowSet']
                df = pd.DataFrame(rows, columns=headers)
                df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
                df = df.sort_values('GAME_DATE', ascending=False)
                
                if last_n_games:
                    df = df.head(last_n_games)
                
                logger.info(f"Analyzing {len(df)} games")
            except (KeyError, IndexError) as e:
                logger.error(f"Error processing game logs data: {str(e)}")
                raise ValueError(f"Error extracting game data: {str(e)}")
            
            # Convert numeric columns
            numeric_cols = ['PTS', 'AST', 'REB', 'FG3M', 'STL', 'BLK']
            for col in numeric_cols:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Identify home/away games
            df['is_home'] = df['MATCHUP'].str.contains('vs')
            
            # Calculate splits
            try:
                home_stats = df[df['is_home']].agg({
                    'PTS': ['mean', 'min', 'max'],
                    'AST': ['mean', 'min', 'max'],
                    'REB': ['mean', 'min', 'max'],
                    'FG3M': ['mean', 'min', 'max'],
                    'STL': ['mean', 'min', 'max'],
                    'BLK': ['mean', 'min', 'max']
                }).round(1)
                
                away_stats = df[~df['is_home']].agg({
                    'PTS': ['mean', 'min', 'max'],
                    'AST': ['mean', 'min', 'max'],
                    'REB': ['mean', 'min', 'max'],
                    'FG3M': ['mean', 'min', 'max'],
                    'STL': ['mean', 'min', 'max'],
                    'BLK': ['mean', 'min', 'max']
                }).round(1)
                
                # Format the response
                result = {
                    "home": {
                        "games_played": int(len(df[df['is_home']])),
                        "stats": {
                            "points": {
                                "avg": float(home_stats['PTS']['mean']),
                                "min": int(home_stats['PTS']['min']),
                                "max": int(home_stats['PTS']['max'])
                            },
                            "assists": {
                                "avg": float(home_stats['AST']['mean']),
                                "min": int(home_stats['AST']['min']),
                                "max": int(home_stats['AST']['max'])
                            },
                            "rebounds": {
                                "avg": float(home_stats['REB']['mean']),
                                "min": int(home_stats['REB']['min']),
                                "max": int(home_stats['REB']['max'])
                            },
                            "threes": {
                                "avg": float(home_stats['FG3M']['mean']),
                                "min": int(home_stats['FG3M']['min']),
                                "max": int(home_stats['FG3M']['max'])
                            },
                            "steals": {
                                "avg": float(home_stats['STL']['mean']),
                                "min": int(home_stats['STL']['min']),
                                "max": int(home_stats['STL']['max'])
                            },
                            "blocks": {
                                "avg": float(home_stats['BLK']['mean']),
                                "min": int(home_stats['BLK']['min']),
                                "max": int(home_stats['BLK']['max'])
                            }
                        }
                    },
                    "away": {
                        "games_played": int(len(df[~df['is_home']])),
                        "stats": {
                            "points": {
                                "avg": float(away_stats['PTS']['mean']),
                                "min": int(away_stats['PTS']['min']),
                                "max": int(away_stats['PTS']['max'])
                            },
                            "assists": {
                                "avg": float(away_stats['AST']['mean']),
                                "min": int(away_stats['AST']['min']),
                                "max": int(away_stats['AST']['max'])
                            },
                            "rebounds": {
                                "avg": float(away_stats['REB']['mean']),
                                "min": int(away_stats['REB']['min']),
                                "max": int(away_stats['REB']['max'])
                            },
                            "threes": {
                                "avg": float(away_stats['FG3M']['mean']),
                                "min": int(away_stats['FG3M']['min']),
                                "max": int(away_stats['FG3M']['max'])
                            },
                            "steals": {
                                "avg": float(away_stats['STL']['mean']),
                                "min": int(away_stats['STL']['min']),
                                "max": int(away_stats['STL']['max'])
                            },
                            "blocks": {
                                "avg": float(away_stats['BLK']['mean']),
                                "min": int(away_stats['BLK']['min']),
                                "max": int(away_stats['BLK']['max'])
                            }
                        }
                    }
                }
                
                logger.info("Successfully calculated home/away splits")
                return result
                
            except Exception as e:
                logger.error(f"Error calculating statistics: {str(e)}")
                raise ValueError(f"Error calculating home/away splits: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error in calculate_home_away_splits: {str(e)}")
            raise

    @staticmethod
    def calculate_rest_day_impact(
        player_id: str, 
        season: Optional[str] = None,
        last_n_games: Optional[int] = None
    ) -> Dict:
        """
        Analyze performance based on days of rest.
        
        Args:
            player_id: NBA player ID
            season: Optional season in format '2023-24'. If None, uses current season
            last_n_games: Optional, analyze only the last N games. If None, analyzes all games
        """
        try:
            game_logs = NBADataLoader.get_player_game_logs(player_id, season)
            df = pd.DataFrame(game_logs['resultSets'][0]['rowSet'], 
                            columns=game_logs['resultSets'][0]['headers'])
            
            # Sort by date
            df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
            df = df.sort_values('GAME_DATE', ascending=False)
            
            if last_n_games:
                df = df.head(last_n_games)
            
            logger.info(f"Analyzing {len(df)} games")
            
            # Calculate days between games
            df['days_rest'] = df['GAME_DATE'].diff().dt.days - 1
            df['days_rest'] = df['days_rest'].fillna(3)  # Assume 3 days rest for first game
            
            # Group by rest days
            rest_groups = {
                "back_to_back": df[df['days_rest'] == 0],
                "one_day_rest": df[df['days_rest'] == 1],
                "two_plus_days_rest": df[df['days_rest'] >= 2]
            }
            
            stats = {}
            for rest_type, group in rest_groups.items():
                if len(group) > 0:
                    stats[rest_type] = {
                        "games_played": len(group),
                        "avg_points": round(group['PTS'].mean(), 1),
                        "avg_assists": round(group['AST'].mean(), 1),
                        "avg_rebounds": round(group['REB'].mean(), 1),
                        "avg_minutes": round(group['MIN'].mean(), 1)
                    }
            
            return stats
        except Exception as e:
            logger.error(f"Error calculating rest day impact: {str(e)}")
            raise

    @staticmethod
    def analyze_matchup_history(
        player_id: str, 
        opponent_team_id: str,
        season: Optional[str] = None,
        last_n_matchups: int = 5
    ) -> Dict:
        """
        Analyze player's performance history against specific teams.
        
        Args:
            player_id: NBA player ID
            opponent_team_id: Team ID to analyze performance against
            season: Optional season in format '2023-24'. If None, analyzes all available seasons
            last_n_matchups: Number of most recent matchups to analyze (default: 5)
        """
        try:
            game_logs = NBADataLoader.get_player_game_logs(player_id, season)
            df = pd.DataFrame(game_logs['resultSets'][0]['rowSet'], 
                            columns=game_logs['resultSets'][0]['headers'])
            
            # Filter games against specific opponent and sort by date
            df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
            opponent_games = df[df['MATCHUP'].str.contains(str(opponent_team_id))]
            recent_games = opponent_games.sort_values('GAME_DATE', ascending=False).head(last_n_matchups)
            
            logger.info(f"Analyzing {len(recent_games)} games against opponent {opponent_team_id}")
            
            performance = {
                "games_analyzed": len(recent_games),
                "averages": {
                    "points": round(recent_games['PTS'].mean(), 1),
                    "assists": round(recent_games['AST'].mean(), 1),
                    "rebounds": round(recent_games['REB'].mean(), 1),
                    "minutes": round(recent_games['MIN'].mean(), 1),
                    "threes": round(recent_games['FG3M'].mean(), 1)
                },
                "ranges": {
                    "points": f"{int(recent_games['PTS'].min())}-{int(recent_games['PTS'].max())}",
                    "assists": f"{int(recent_games['AST'].min())}-{int(recent_games['AST'].max())}",
                    "rebounds": f"{int(recent_games['REB'].min())}-{int(recent_games['REB'].max())}",
                }
            }
            
            return performance
        except Exception as e:
            logger.error(f"Error analyzing matchup history: {str(e)}")
            raise

    @staticmethod
    def calculate_consistency_score(
        player_id: str, 
        stat_type: str,
        season: Optional[str] = None,
        last_n_games: int = 20
    ) -> Dict:
        """
        Calculate a consistency score (0-100) for different statistical categories.
        Higher score means more consistent performance.
        
        Args:
            player_id: NBA player ID
            stat_type: Statistical category to analyze (PTS, AST, REB, FG3M, STL, BLK)
            season: Optional season in format '2023-24'. If None, uses current season
            last_n_games: Number of most recent games to analyze (default: 20)
        """
        try:
            game_logs = NBADataLoader.get_player_game_logs(player_id, season)
            df = pd.DataFrame(game_logs['resultSets'][0]['rowSet'], 
                            columns=game_logs['resultSets'][0]['headers'])
            
            # Sort by date and take last N games
            df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
            recent_games = df.sort_values('GAME_DATE', ascending=False).head(last_n_games)
            
            logger.info(f"Analyzing consistency over {len(recent_games)} games")
            
            if stat_type not in ['PTS', 'AST', 'REB', 'FG3M', 'STL', 'BLK']:
                raise ValueError("Invalid stat type")
            
            values = recent_games[stat_type].astype(float)
            
            # Calculate coefficient of variation (lower means more consistent)
            cv = np.std(values) / np.mean(values) if np.mean(values) > 0 else float('inf')
            
            # Convert to 0-100 score (lower cv = higher score)
            consistency_score = max(0, min(100, 100 * (1 - cv)))
            
            # Calculate additional metrics
            result = {
                "consistency_score": round(consistency_score, 1),
                "average": round(np.mean(values), 1),
                "std_dev": round(np.std(values), 1),
                "median": round(np.median(values), 1),
                "range": f"{int(min(values))}-{int(max(values))}",
                "games_analyzed": len(values)
            }
            
            return result
        except Exception as e:
            logger.error(f"Error calculating consistency score: {str(e)}")
            raise

    @staticmethod
    def analyze_pace_impact(
        player_id: str,
        season: Optional[str] = None,
        last_n_games: int = 20
    ) -> Dict:
        """
        Analyze performance in different pace scenarios.
        
        Args:
            player_id: NBA player ID
            season: Optional season in format '2023-24'. If None, uses current season
            last_n_games: Number of most recent games to analyze (default: 20)
        """
        try:
            game_logs = NBADataLoader.get_player_game_logs(player_id, season)
            df = pd.DataFrame(game_logs['resultSets'][0]['rowSet'], 
                            columns=game_logs['resultSets'][0]['headers'])
            
            # Sort by date and take last N games
            df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
            recent_games = df.sort_values('GAME_DATE', ascending=False).head(last_n_games)
            
            logger.info(f"Analyzing pace impact over {len(recent_games)} games")
            
            # Calculate possessions (rough estimate)
            recent_games['POSS'] = recent_games['FGA'] - recent_games['OREB'] + recent_games['TOV']
            
            # Define pace categories
            pace_threshold_high = recent_games['POSS'].quantile(0.67)
            pace_threshold_low = recent_games['POSS'].quantile(0.33)
            
            pace_groups = {
                "high_pace": recent_games[recent_games['POSS'] >= pace_threshold_high],
                "medium_pace": recent_games[(recent_games['POSS'] < pace_threshold_high) & 
                                         (recent_games['POSS'] > pace_threshold_low)],
                "low_pace": recent_games[recent_games['POSS'] <= pace_threshold_low]
            }
            
            stats = {}
            for pace_type, group in pace_groups.items():
                if len(group) > 0:
                    stats[pace_type] = {
                        "games_played": len(group),
                        "avg_points": round(group['PTS'].mean(), 1),
                        "avg_assists": round(group['AST'].mean(), 1),
                        "avg_rebounds": round(group['REB'].mean(), 1),
                        "avg_minutes": round(group['MIN'].mean(), 1),
                        "avg_possessions": round(group['POSS'].mean(), 1)
                    }
            
            return stats
        except Exception as e:
            logger.error(f"Error analyzing pace impact: {str(e)}")
            raise
