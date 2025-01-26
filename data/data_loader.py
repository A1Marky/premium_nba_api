from nba_api.stats.endpoints import (
    playercareerstats,
    playergamelog,
    teamgamelog,
    leaguegamelog,
    playerprofilev2,
    leaguedashplayerstats,
    leaguedashteamstats,
    leaguehustlestatsplayer,
    playerdashptshots,
    hustlestatsboxscore,
    boxscoreplayertrackv2,
    boxscoreadvancedv2,
    playervsplayer,
    commonplayerinfo
)
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import players
import pandas as pd
from typing import Dict, List, Optional
import logging
import json
import time
from requests.exceptions import Timeout, RequestException

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# NBA API Configuration
NBA_REQUEST_TIMEOUT = 60  # Increased timeout to 60 seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds between retries

class NBADataLoader:
    @staticmethod
    def _make_api_request(request_func, *args, **kwargs):
        """Helper method to make NBA API requests with retries"""
        for attempt in range(MAX_RETRIES):
            try:
                return request_func(*args, timeout=NBA_REQUEST_TIMEOUT, **kwargs)
            except Timeout:
                logger.warning(f"Request timed out (attempt {attempt + 1}/{MAX_RETRIES})")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
                else:
                    raise ValueError("NBA API request timed out after multiple attempts. Please try again later.")
            except RequestException as e:
                logger.error(f"NBA API request failed: {str(e)}")
                raise ValueError(f"Failed to fetch data from NBA API: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during NBA API request: {str(e)}")
                raise

    @staticmethod
    def get_player_career_stats(player_id: str) -> Dict:
        """Get career statistics for a specific player."""
        try:
            logger.info(f"Fetching career stats for player {player_id}")
            
            # Verify player exists
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid player ID: {player_id}")
            
            career = NBADataLoader._make_api_request(
                playercareerstats.PlayerCareerStats,
                player_id=player_id
            )
            
            data = career.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No career stats found for player {player_id}")
            
            logger.info(f"Successfully retrieved career stats. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching career stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching career stats: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching career stats. Please try again later.")

    @staticmethod
    def get_player_game_logs(player_id: str, season: Optional[str] = None) -> Dict:
        """Get game logs for a specific player."""
        try:
            logger.info(f"Fetching game logs for player {player_id}, season {season}")
            
            # Verify player exists
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid player ID: {player_id}")
            
            if season:
                game_logs = NBADataLoader._make_api_request(
                    playergamelog.PlayerGameLog,
                    player_id=player_id,
                    season=season
                )
            else:
                game_logs = NBADataLoader._make_api_request(
                    playergamelog.PlayerGameLog,
                    player_id=player_id
                )
            
            data = game_logs.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No game logs found for player {player_id} {'for season ' + season if season else ''}")
            
            logger.info(f"Successfully retrieved game logs. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching game logs: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching game logs: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching game logs. Please try again later.")

    @staticmethod
    def get_player_advanced_stats(player_id: str) -> Dict:
        """Get advanced statistics for a specific player."""
        try:
            logger.info(f"Fetching advanced stats for player {player_id}")
            
            # Verify player exists
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid player ID: {player_id}")
            
            profile = NBADataLoader._make_api_request(
                playerprofilev2.PlayerProfileV2,
                player_id=player_id
            )
            
            data = profile.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No advanced stats found for player {player_id}")
            
            logger.info(f"Successfully retrieved advanced stats. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching advanced stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching advanced stats: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching advanced stats. Please try again later.")

    @staticmethod
    def get_team_game_logs(team_id: str, season: Optional[str] = None) -> Dict:
        """Get game logs for a specific team."""
        try:
            logger.info(f"Fetching game logs for team {team_id}, season {season}")
            
            if season:
                team_logs = NBADataLoader._make_api_request(
                    teamgamelog.TeamGameLog,
                    team_id=team_id,
                    season=season
                )
            else:
                team_logs = NBADataLoader._make_api_request(
                    teamgamelog.TeamGameLog,
                    team_id=team_id
                )
            
            data = team_logs.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No game logs found for team {team_id} {'for season ' + season if season else ''}")
            
            logger.info(f"Successfully retrieved team game logs. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching team game logs: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching team game logs: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching team game logs. Please try again later.")

    @staticmethod
    def get_league_player_stats(season: Optional[str] = None) -> Dict:
        """Get league-wide player statistics."""
        try:
            logger.info(f"Fetching league player stats for season {season}")
            
            if season:
                league_stats = NBADataLoader._make_api_request(
                    leaguedashplayerstats.LeagueDashPlayerStats,
                    season=season
                )
            else:
                league_stats = NBADataLoader._make_api_request(
                    leaguedashplayerstats.LeagueDashPlayerStats
                )
            
            data = league_stats.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No league player stats found {'for season ' + season if season else ''}")
            
            logger.info(f"Successfully retrieved league player stats. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching league player stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching league player stats: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching league player stats. Please try again later.")

    @staticmethod
    def find_games_by_player(player_id: str, season: Optional[str] = None) -> Dict:
        """Find all games played by a specific player."""
        try:
            logger.info(f"Finding games for player {player_id}, season {season}")
            
            # Verify player exists
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid player ID: {player_id}")
            
            if season:
                game_finder = NBADataLoader._make_api_request(
                    leaguegamelog.LeagueGameLog,
                    player_id_nullable=player_id,
                    season_nullable=season
                )
            else:
                game_finder = NBADataLoader._make_api_request(
                    leaguegamelog.LeagueGameLog,
                    player_id_nullable=player_id
                )
            
            data = game_finder.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No games found for player {player_id} {'for season ' + season if season else ''}")
            
            logger.info(f"Successfully retrieved games. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error finding games: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error finding games: {str(e)}")
            raise ValueError("An unexpected error occurred while finding games. Please try again later.")

    @staticmethod
    def get_player_info(player_id: str) -> Dict:
        """Get detailed player information including physical stats and experience."""
        try:
            logger.info(f"Fetching player info for player {player_id}")
            
            # Verify player exists
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid player ID: {player_id}")
            
            info = NBADataLoader._make_api_request(
                commonplayerinfo.CommonPlayerInfo,
                player_id=player_id
            )
            
            data = info.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No player info found for player {player_id}")
            
            logger.info(f"Successfully retrieved player info. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching player info: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching player info: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching player info. Please try again later.")

    @staticmethod
    def get_player_shot_dashboard(player_id: str, season: Optional[str] = None) -> Dict:
        """Get detailed shot statistics for a player."""
        try:
            logger.info(f"Fetching shot dashboard for player {player_id}, season {season}")
            
            # Verify player exists
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid player ID: {player_id}")
            
            if season:
                shots = NBADataLoader._make_api_request(
                    playerdashptshots.PlayerDashPtShots,
                    player_id=player_id,
                    season_nullable=season
                )
            else:
                shots = NBADataLoader._make_api_request(
                    playerdashptshots.PlayerDashPtShots,
                    player_id=player_id
                )
            
            data = shots.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No shot dashboard found for player {player_id} {'for season ' + season if season else ''}")
            
            logger.info(f"Successfully retrieved shot dashboard. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching shot dashboard: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching shot dashboard: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching shot dashboard. Please try again later.")

    @staticmethod
    def get_player_hustle_stats(player_id: str, game_id: str) -> Dict:
        """Get hustle statistics for a player in a specific game."""
        try:
            logger.info(f"Fetching hustle stats for player {player_id}, game {game_id}")
            
            # Verify player exists
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid player ID: {player_id}")
            
            hustle = NBADataLoader._make_api_request(
                hustlestatsboxscore.HustleStatsBoxScore,
                game_id=game_id
            )
            
            data = hustle.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No hustle stats found for player {player_id} in game {game_id}")
            
            logger.info(f"Successfully retrieved hustle stats. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching hustle stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching hustle stats: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching hustle stats. Please try again later.")

    @staticmethod
    def get_player_tracking_stats(game_id: str) -> Dict:
        """Get player tracking statistics for a specific game."""
        try:
            logger.info(f"Fetching tracking stats for game {game_id}")
            
            tracking = NBADataLoader._make_api_request(
                boxscoreplayertrackv2.BoxScorePlayerTrackV2,
                game_id=game_id
            )
            
            data = tracking.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No tracking stats found for game {game_id}")
            
            logger.info(f"Successfully retrieved tracking stats. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching tracking stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching tracking stats: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching tracking stats. Please try again later.")

    @staticmethod
    def get_advanced_box_score(game_id: str) -> Dict:
        """Get advanced box score statistics for a specific game."""
        try:
            logger.info(f"Fetching advanced box score for game {game_id}")
            
            box_score = NBADataLoader._make_api_request(
                boxscoreadvancedv2.BoxScoreAdvancedV2,
                game_id=game_id
            )
            
            data = box_score.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No advanced box score found for game {game_id}")
            
            logger.info(f"Successfully retrieved advanced box score. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching advanced box score: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching advanced box score: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching advanced box score. Please try again later.")

    @staticmethod
    def get_player_vs_player_stats(player_id: str, vs_player_id: str) -> Dict:
        """Get head-to-head statistics between two players."""
        try:
            logger.info(f"Fetching vs player stats for player {player_id} vs {vs_player_id}")
            
            # Verify players exist
            try:
                player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
                player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid player ID: {player_id}")
            
            try:
                vs_player_info = commonplayerinfo.CommonPlayerInfo(player_id=vs_player_id)
                vs_player_info.get_dict()
            except Exception:
                raise ValueError(f"Invalid vs player ID: {vs_player_id}")
            
            vs_stats = NBADataLoader._make_api_request(
                playervsplayer.PlayerVsPlayer,
                player_id=player_id,
                vs_player_id=vs_player_id
            )
            
            data = vs_stats.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No vs player stats found for player {player_id} vs {vs_player_id}")
            
            logger.info(f"Successfully retrieved vs player stats. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching vs player stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching vs player stats: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching vs player stats. Please try again later.")

    @staticmethod
    def get_team_stats(season: Optional[str] = None) -> Dict:
        """Get comprehensive team statistics."""
        try:
            logger.info(f"Fetching team stats for season {season}")
            
            if season:
                team_stats = NBADataLoader._make_api_request(
                    leaguedashteamstats.LeagueDashTeamStats,
                    season=season
                )
            else:
                team_stats = NBADataLoader._make_api_request(
                    leaguedashteamstats.LeagueDashTeamStats
                )
            
            data = team_stats.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No team stats found {'for season ' + season if season else ''}")
            
            logger.info(f"Successfully retrieved team stats. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching team stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching team stats: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching team stats. Please try again later.")

    @staticmethod
    def get_league_hustle_stats(season: Optional[str] = None) -> Dict:
        """Get league-wide hustle statistics."""
        try:
            logger.info(f"Fetching league hustle stats for season {season}")
            
            if season:
                hustle_stats = NBADataLoader._make_api_request(
                    leaguehustlestatsplayer.LeagueHustleStatsPlayer,
                    season=season
                )
            else:
                hustle_stats = NBADataLoader._make_api_request(
                    leaguehustlestatsplayer.LeagueHustleStatsPlayer
                )
            
            data = hustle_stats.get_dict()
            
            if not data or 'resultSets' not in data or not data['resultSets'][0]['rowSet']:
                raise ValueError(f"No league hustle stats found {'for season ' + season if season else ''}")
            
            logger.info(f"Successfully retrieved league hustle stats. Data keys: {list(data.keys())}")
            return data
            
        except ValueError as e:
            logger.error(f"Error fetching league hustle stats: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error fetching league hustle stats: {str(e)}")
            raise ValueError("An unexpected error occurred while fetching league hustle stats. Please try again later.")
