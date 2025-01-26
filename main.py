from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import os
from dotenv import load_dotenv
from data.data_loader import NBADataLoader
from utils.hit_rate_calculator import HitRateCalculator
from utils.prop_analyzer import PropAnalyzer

# Load environment variables
load_dotenv()

app = FastAPI(
    title="NBA Stats API",
    description="API for retrieving NBA player statistics for projection modeling",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def root():
    return {"message": "Welcome to the NBA Stats API"}

@app.get("/player/career/{player_id}")
async def get_player_career_stats(player_id: str):
    """Get career statistics for a specific player"""
    try:
        return NBADataLoader.get_player_career_stats(player_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/games/{player_id}")
async def get_player_game_logs(player_id: str, season: Optional[str] = None):
    """Get game logs for a specific player"""
    try:
        return NBADataLoader.get_player_game_logs(player_id, season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/advanced/{player_id}")
async def get_player_advanced_stats(player_id: str):
    """Get advanced statistics for a specific player"""
    try:
        return NBADataLoader.get_player_advanced_stats(player_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/team/games/{team_id}")
async def get_team_game_logs(team_id: str, season: Optional[str] = None):
    """Get game logs for a specific team"""
    try:
        return NBADataLoader.get_team_game_logs(team_id, season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/league/players")
async def get_league_player_stats(season: Optional[str] = None):
    """Get league-wide player statistics"""
    try:
        return NBADataLoader.get_league_player_stats(season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/find-games/{player_id}")
async def find_games_by_player(player_id: str, season: Optional[str] = None):
    """Find all games played by a specific player"""
    try:
        return NBADataLoader.find_games_by_player(player_id, season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/info/{player_id}")
async def get_player_info(player_id: str):
    """Get detailed player information"""
    try:
        return NBADataLoader.get_player_info(player_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/shots/{player_id}")
async def get_player_shot_dashboard(player_id: str, season: Optional[str] = None):
    """Get detailed shot statistics for a player"""
    try:
        return NBADataLoader.get_player_shot_dashboard(player_id, season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/hustle/{game_id}")
async def get_player_hustle_stats(game_id: str):
    """Get hustle statistics for players in a specific game"""
    try:
        return NBADataLoader.get_player_hustle_stats(game_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/game/tracking/{game_id}")
async def get_player_tracking_stats(game_id: str):
    """Get player tracking statistics for a specific game"""
    try:
        return NBADataLoader.get_player_tracking_stats(game_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/game/advanced/{game_id}")
async def get_advanced_box_score(game_id: str):
    """Get advanced box score statistics for a specific game"""
    try:
        return NBADataLoader.get_advanced_box_score(game_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/vs/{player_id}/{vs_player_id}")
async def get_player_vs_player_stats(player_id: str, vs_player_id: str):
    """Get head-to-head statistics between two players"""
    try:
        return NBADataLoader.get_player_vs_player_stats(player_id, vs_player_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/team/stats")
async def get_team_stats(season: Optional[str] = None):
    """Get comprehensive team statistics"""
    try:
        return NBADataLoader.get_team_stats(season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/league/hustle")
async def get_league_hustle_stats(season: Optional[str] = None):
    """Get league-wide hustle statistics"""
    try:
        return NBADataLoader.get_league_hustle_stats(season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/hit-rates/{player_id}")
async def get_player_hit_rates(
    player_id: str,
    num_games: Optional[int] = 10,
    season: Optional[str] = None
):
    """
    Get hit rates for various statistical thresholds over the last N games
    
    Parameters:
    - player_id: NBA player ID
    - num_games: Number of most recent games to analyze (default: 10)
    - season: NBA season in format '2023-24' (optional)
    
    Returns:
    Hit rates for points, assists, rebounds, three-pointers, steals, and blocks
    """
    try:
        return HitRateCalculator.get_player_hit_rates(player_id, num_games, season)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/home-away/{player_id}")
async def get_home_away_splits(
    player_id: str,
    season: Optional[str] = None,
    last_n_games: Optional[int] = None
):
    """
    Get performance splits between home and away games
    
    - If season is provided, analyzes games from that season only
    - If last_n_games is provided, analyzes only the most recent N games
    - If neither is provided, analyzes all games from the current season
    """
    try:
        return PropAnalyzer.calculate_home_away_splits(player_id, season, last_n_games)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/rest-impact/{player_id}")
async def get_rest_day_impact(
    player_id: str,
    season: Optional[str] = None,
    last_n_games: Optional[int] = None
):
    """
    Get performance analysis based on days of rest
    
    - If season is provided, analyzes games from that season only
    - If last_n_games is provided, analyzes only the most recent N games
    - If neither is provided, analyzes all games from the current season
    """
    try:
        return PropAnalyzer.calculate_rest_day_impact(player_id, season, last_n_games)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/matchup-history/{player_id}/{opponent_team_id}")
async def get_matchup_history(
    player_id: str,
    opponent_team_id: str,
    season: Optional[str] = None,
    last_n_matchups: Optional[int] = 5
):
    """
    Get player's performance history against specific teams
    
    - If season is provided, analyzes matchups from that season only
    - last_n_matchups determines how many recent matchups to analyze (default: 5)
    - If season is not provided, analyzes matchups across all available seasons
    """
    try:
        return PropAnalyzer.analyze_matchup_history(player_id, opponent_team_id, season, last_n_matchups)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/consistency/{player_id}/{stat_type}")
async def get_consistency_score(
    player_id: str,
    stat_type: str,
    season: Optional[str] = None,
    last_n_games: int = 20
):
    """
    Get consistency score and analysis for a specific statistical category
    
    - stat_type must be one of: PTS, AST, REB, FG3M, STL, BLK
    - If season is provided, analyzes games from that season only
    - last_n_games determines how many recent games to analyze (default: 20)
    - If season is not provided, analyzes games from the current season
    """
    try:
        return PropAnalyzer.calculate_consistency_score(player_id, stat_type, season, last_n_games)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/player/pace-impact/{player_id}")
async def get_pace_impact(
    player_id: str,
    season: Optional[str] = None,
    last_n_games: int = 20
):
    """
    Get analysis of performance in different pace scenarios
    
    - If season is provided, analyzes games from that season only
    - last_n_games determines how many recent games to analyze (default: 20)
    - If season is not provided, analyzes games from the current season
    """
    try:
        return PropAnalyzer.analyze_pace_impact(player_id, season, last_n_games)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
