from typing import Dict, List, Optional, Tuple
import pandas as pd
from data.data_loader import NBADataLoader
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HitRateCalculator:
    POINTS_THRESHOLDS = [10, 15, 20, 25, 30, 35]
    ASSISTS_THRESHOLDS = [2, 4, 6, 8, 10]
    REBOUNDS_THRESHOLDS = [4, 6, 8, 10, 12, 14, 16]
    THREES_THRESHOLDS = [1, 2, 3, 4, 5, 6, 7, 8]
    STEALS_THRESHOLDS = [1, 2, 3, 4]
    BLOCKS_THRESHOLDS = [1, 2, 3, 4]

    @staticmethod
    def calculate_hit_rate(values: List[float], threshold: float) -> Tuple[str, float]:
        """Calculate hit rate for a given threshold."""
        try:
            hits = sum(1 for value in values if value >= threshold)
            total_games = len(values)
            hit_rate = (hits / total_games) * 100 if total_games > 0 else 0
            return f"{hits}/{total_games}", hit_rate
        except Exception as e:
            logger.error(f"Error calculating hit rate: {str(e)}")
            raise

    @staticmethod
    def get_player_hit_rates(player_id: str, num_games: int = 10, season: Optional[str] = None) -> Dict:
        """
        Get hit rates for all statistical categories over the last N games.
        
        Args:
            player_id: NBA player ID
            num_games: Number of most recent games to analyze
            season: NBA season in format '2023-24'. If None, uses current season.
        
        Returns:
            Dictionary containing hit rates for all statistical categories
        """
        try:
            # Get player game logs
            game_logs = NBADataLoader.get_player_game_logs(player_id, season)
            logger.info(f"Retrieved game logs for player {player_id}")
            
            if not game_logs or 'resultSets' not in game_logs:
                logger.error(f"Invalid game logs format: {game_logs}")
                raise ValueError("Invalid game logs data received from NBA API")

            # Convert to pandas DataFrame for easier manipulation
            try:
                df = pd.DataFrame(game_logs['resultSets'][0]['rowSet'], 
                                columns=game_logs['resultSets'][0]['headers'])
                logger.info(f"Created DataFrame with {len(df)} games")
            except Exception as e:
                logger.error(f"Error creating DataFrame: {str(e)}")
                raise ValueError(f"Error processing game logs: {str(e)}")

            # Sort by game date and take last N games
            df = df.sort_values('GAME_DATE', ascending=False).head(num_games)
            logger.info(f"Processing last {len(df)} games")

            hit_rates = {
                "points": {},
                "assists": {},
                "rebounds": {},
                "threes": {},
                "steals": {},
                "blocks": {}
            }

            # Calculate hit rates for each category
            for threshold in HitRateCalculator.POINTS_THRESHOLDS:
                fraction, percentage = HitRateCalculator.calculate_hit_rate(
                    df['PTS'].astype(float).tolist(), threshold
                )
                hit_rates["points"][f"{threshold}+"] = {
                    "fraction": fraction,
                    "percentage": round(percentage, 2)
                }

            for threshold in HitRateCalculator.ASSISTS_THRESHOLDS:
                fraction, percentage = HitRateCalculator.calculate_hit_rate(
                    df['AST'].astype(float).tolist(), threshold
                )
                hit_rates["assists"][f"{threshold}+"] = {
                    "fraction": fraction,
                    "percentage": round(percentage, 2)
                }

            for threshold in HitRateCalculator.REBOUNDS_THRESHOLDS:
                fraction, percentage = HitRateCalculator.calculate_hit_rate(
                    df['REB'].astype(float).tolist(), threshold
                )
                hit_rates["rebounds"][f"{threshold}+"] = {
                    "fraction": fraction,
                    "percentage": round(percentage, 2)
                }

            for threshold in HitRateCalculator.THREES_THRESHOLDS:
                fraction, percentage = HitRateCalculator.calculate_hit_rate(
                    df['FG3M'].astype(float).tolist(), threshold
                )
                hit_rates["threes"][f"{threshold}+"] = {
                    "fraction": fraction,
                    "percentage": round(percentage, 2)
                }

            for threshold in HitRateCalculator.STEALS_THRESHOLDS:
                fraction, percentage = HitRateCalculator.calculate_hit_rate(
                    df['STL'].astype(float).tolist(), threshold
                )
                hit_rates["steals"][f"{threshold}+"] = {
                    "fraction": fraction,
                    "percentage": round(percentage, 2)
                }

            for threshold in HitRateCalculator.BLOCKS_THRESHOLDS:
                fraction, percentage = HitRateCalculator.calculate_hit_rate(
                    df['BLK'].astype(float).tolist(), threshold
                )
                hit_rates["blocks"][f"{threshold}+"] = {
                    "fraction": fraction,
                    "percentage": round(percentage, 2)
                }

            logger.info("Successfully calculated all hit rates")
            return hit_rates

        except Exception as e:
            logger.error(f"Error in get_player_hit_rates: {str(e)}")
            raise
