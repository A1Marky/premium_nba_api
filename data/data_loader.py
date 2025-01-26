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
import pandas as pd
from typing import Dict, List, Optional
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NBADataLoader:
    @staticmethod
    def get_player_career_stats(player_id: str) -> Dict:
        """Get career statistics for a specific player."""
        try:
            logger.info(f"Fetching career stats for player {player_id}")
            career = playercareerstats.PlayerCareerStats(player_id=player_id)
            data = career.get_dict()
            logger.info(f"Successfully retrieved career stats. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching career stats: {str(e)}")
            raise

    @staticmethod
    def get_player_game_logs(player_id: str, season: Optional[str] = None) -> Dict:
        """Get game logs for a specific player. Season format: '2023-24'"""
        try:
            logger.info(f"Fetching game logs for player {player_id}, season {season}")
            if season:
                game_logs = playergamelog.PlayerGameLog(player_id=player_id, season=season)
            else:
                game_logs = playergamelog.PlayerGameLog(player_id=player_id)
            
            data = game_logs.get_dict()
            logger.info(f"Successfully retrieved game logs. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching game logs: {str(e)}")
            raise

    @staticmethod
    def get_player_advanced_stats(player_id: str) -> Dict:
        """Get advanced statistics for a specific player."""
        try:
            logger.info(f"Fetching advanced stats for player {player_id}")
            profile = playerprofilev2.PlayerProfileV2(player_id=player_id)
            data = profile.get_dict()
            logger.info(f"Successfully retrieved advanced stats. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching advanced stats: {str(e)}")
            raise

    @staticmethod
    def get_team_game_logs(team_id: str, season: Optional[str] = None) -> Dict:
        """Get game logs for a specific team. Season format: '2023-24'"""
        try:
            logger.info(f"Fetching game logs for team {team_id}, season {season}")
            if season:
                team_logs = teamgamelog.TeamGameLog(team_id=team_id, season=season)
            else:
                team_logs = teamgamelog.TeamGameLog(team_id=team_id)
            
            data = team_logs.get_dict()
            logger.info(f"Successfully retrieved team game logs. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching team game logs: {str(e)}")
            raise

    @staticmethod
    def get_league_player_stats(season: Optional[str] = None) -> Dict:
        """Get league-wide player statistics. Season format: '2023-24'"""
        try:
            logger.info(f"Fetching league player stats for season {season}")
            if season:
                league_stats = leaguedashplayerstats.LeagueDashPlayerStats(season=season)
            else:
                league_stats = leaguedashplayerstats.LeagueDashPlayerStats()
            
            data = league_stats.get_dict()
            logger.info(f"Successfully retrieved league player stats. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching league player stats: {str(e)}")
            raise

    @staticmethod
    def find_games_by_player(player_id: str, season: Optional[str] = None) -> Dict:
        """Find all games played by a specific player. Season format: '2023-24'"""
        try:
            logger.info(f"Finding games for player {player_id}, season {season}")
            if season:
                game_finder = leaguegamelog.LeagueGameLog(
                    player_id_nullable=player_id,
                    season_nullable=season
                )
            else:
                game_finder = leaguegamelog.LeagueGameLog(
                    player_id_nullable=player_id
                )
            
            data = game_finder.get_dict()
            logger.info(f"Successfully retrieved games. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error finding games: {str(e)}")
            raise

    @staticmethod
    def get_player_info(player_id: str) -> Dict:
        """Get detailed player information including physical stats and experience."""
        try:
            logger.info(f"Fetching player info for player {player_id}")
            info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
            data = info.get_dict()
            logger.info(f"Successfully retrieved player info. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching player info: {str(e)}")
            raise

    @staticmethod
    def get_player_shot_dashboard(player_id: str, season: Optional[str] = None) -> Dict:
        """Get detailed shot statistics for a player."""
        try:
            logger.info(f"Fetching shot dashboard for player {player_id}, season {season}")
            if season:
                shots = playerdashptshots.PlayerDashPtShots(
                    player_id=player_id,
                    season_nullable=season
                )
            else:
                shots = playerdashptshots.PlayerDashPtShots(
                    player_id=player_id
                )
            
            data = shots.get_dict()
            logger.info(f"Successfully retrieved shot dashboard. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching shot dashboard: {str(e)}")
            raise

    @staticmethod
    def get_player_hustle_stats(player_id: str, game_id: str) -> Dict:
        """Get hustle statistics for a player in a specific game."""
        try:
            logger.info(f"Fetching hustle stats for player {player_id}, game {game_id}")
            hustle = hustlestatsboxscore.HustleStatsBoxScore(game_id=game_id)
            data = hustle.get_dict()
            logger.info(f"Successfully retrieved hustle stats. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching hustle stats: {str(e)}")
            raise

    @staticmethod
    def get_player_tracking_stats(game_id: str) -> Dict:
        """Get player tracking statistics for a specific game."""
        try:
            logger.info(f"Fetching tracking stats for game {game_id}")
            tracking = boxscoreplayertrackv2.BoxScorePlayerTrackV2(game_id=game_id)
            data = tracking.get_dict()
            logger.info(f"Successfully retrieved tracking stats. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching tracking stats: {str(e)}")
            raise

    @staticmethod
    def get_advanced_box_score(game_id: str) -> Dict:
        """Get advanced box score statistics for a specific game."""
        try:
            logger.info(f"Fetching advanced box score for game {game_id}")
            box_score = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)
            data = box_score.get_dict()
            logger.info(f"Successfully retrieved advanced box score. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching advanced box score: {str(e)}")
            raise

    @staticmethod
    def get_player_vs_player_stats(player_id: str, vs_player_id: str) -> Dict:
        """Get head-to-head statistics between two players."""
        try:
            logger.info(f"Fetching vs player stats for player {player_id} vs {vs_player_id}")
            vs_stats = playervsplayer.PlayerVsPlayer(
                player_id=player_id,
                vs_player_id=vs_player_id
            )
            data = vs_stats.get_dict()
            logger.info(f"Successfully retrieved vs player stats. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching vs player stats: {str(e)}")
            raise

    @staticmethod
    def get_team_stats(season: Optional[str] = None) -> Dict:
        """Get comprehensive team statistics."""
        try:
            logger.info(f"Fetching team stats for season {season}")
            if season:
                team_stats = leaguedashteamstats.LeagueDashTeamStats(season=season)
            else:
                team_stats = leaguedashteamstats.LeagueDashTeamStats()
            
            data = team_stats.get_dict()
            logger.info(f"Successfully retrieved team stats. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching team stats: {str(e)}")
            raise

    @staticmethod
    def get_league_hustle_stats(season: Optional[str] = None) -> Dict:
        """Get league-wide hustle statistics."""
        try:
            logger.info(f"Fetching league hustle stats for season {season}")
            if season:
                hustle_stats = leaguehustlestatsplayer.LeagueHustleStatsPlayer(season=season)
            else:
                hustle_stats = leaguehustlestatsplayer.LeagueHustleStatsPlayer()
            
            data = hustle_stats.get_dict()
            logger.info(f"Successfully retrieved league hustle stats. Data keys: {list(data.keys())}")
            return data
        except Exception as e:
            logger.error(f"Error fetching league hustle stats: {str(e)}")
            raise
