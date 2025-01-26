# NBA Stat Projection API Documentation

## Overview
This API provides various endpoints for analyzing NBA player statistics and performance metrics. It's designed to help with player prop betting analysis by providing detailed statistical breakdowns and performance patterns.

## Base URL
```
http://localhost:8002
```

## Endpoints

### 1. Home/Away Splits
```
GET /player/home-away/{player_id}
```

Analyzes a player's performance splits between home and away games.

**Parameters:**
- `player_id` (path, required): NBA player ID
- `season` (query, optional): Season in format "2023-24". If not provided, uses current season
- `last_n_games` (query, optional): Only analyze the most recent N games

**Response:**
```json
{
    "home_games": {
        "count": 20,
        "stats": {
            "points": {"avg": 25.5, "min": 15, "max": 35},
            "assists": {"avg": 8.2, "min": 4, "max": 12},
            "rebounds": {"avg": 11.3, "min": 6, "max": 16},
            "three_pointers": {"avg": 2.1, "min": 0, "max": 5},
            "steals": {"avg": 1.5, "min": 0, "max": 4},
            "blocks": {"avg": 0.8, "min": 0, "max": 3}
        }
    },
    "away_games": {
        // Similar structure as home_games
    }
}
```

### 2. Rest Day Impact
```
GET /player/rest-impact/{player_id}
```

Analyzes how a player performs based on days of rest between games.

**Parameters:**
- `player_id` (path, required): NBA player ID
- `season` (query, optional): Season in format "2023-24". If not provided, uses current season
- `last_n_games` (query, optional): Only analyze the most recent N games

**Response:**
```json
{
    "zero_days_rest": {
        "games": 10,
        "avg_points": 24.5,
        "avg_efficiency": 0.48
    },
    "one_day_rest": {
        // Similar structure
    },
    "two_plus_days_rest": {
        // Similar structure
    }
}
```

### 3. Matchup History
```
GET /player/matchup-history/{player_id}/{opponent_team_id}
```

Analyzes a player's performance history against specific teams.

**Parameters:**
- `player_id` (path, required): NBA player ID
- `opponent_team_id` (path, required): Team ID to analyze performance against
- `season` (query, optional): Season in format "2023-24". If not provided, analyzes all available seasons
- `last_n_matchups` (query, optional): Number of most recent matchups to analyze (default: 5)

**Response:**
```json
{
    "games_analyzed": 5,
    "avg_points": 26.4,
    "avg_assists": 7.2,
    "avg_rebounds": 10.8,
    "performance_trend": "improving/declining/stable",
    "last_matchup": {
        "date": "2024-01-15",
        "points": 28,
        "assists": 8,
        "rebounds": 12
    }
}
```

### 4. Consistency Score
```
GET /player/consistency/{player_id}/{stat_type}
```

Calculates a consistency score (0-100) for different statistical categories.

**Parameters:**
- `player_id` (path, required): NBA player ID
- `stat_type` (path, required): One of: PTS, AST, REB, FG3M, STL, BLK
- `season` (query, optional): Season in format "2023-24". If not provided, uses current season
- `last_n_games` (query, optional): Number of games to analyze (default: 20)

**Response:**
```json
{
    "consistency_score": 85,
    "stat_type": "PTS",
    "games_analyzed": 20,
    "average": 26.5,
    "standard_deviation": 3.2,
    "hit_rate_above_avg": 0.75,
    "recent_trend": "stable"
}
```

### 5. Pace Impact
```
GET /player/pace-impact/{player_id}
```

Analyzes how a player performs in different game pace scenarios.

**Parameters:**
- `player_id` (path, required): NBA player ID
- `season` (query, optional): Season in format "2023-24". If not provided, uses current season
- `last_n_games` (query, optional): Number of games to analyze (default: 20)

**Response:**
```json
{
    "games_analyzed": 20,
    "pace_categories": {
        "fast": {
            "games": 7,
            "avg_points": 28.5,
            "avg_efficiency": 0.52
        },
        "medium": {
            // Similar structure
        },
        "slow": {
            // Similar structure
        }
    },
    "optimal_pace": "fast"
}
```

## Error Responses
All endpoints may return the following errors:

- `400 Bad Request`: Invalid parameters
- `404 Not Found`: Player or team not found
- `500 Internal Server Error`: Server-side error

## Rate Limiting
Please limit requests to 20 per minute per IP address to ensure API stability.

## Examples

1. Get Nikola Jokić's home/away splits for the last 10 games:
```
GET /player/home-away/203999?last_n_games=10
```

2. Get LeBron James's consistency score in points for the 2023-24 season:
```
GET /player/consistency/2544/PTS?season=2023-24
```

3. Get Steph Curry's last 5 performances against the Lakers:
```
GET /player/matchup-history/201939/1610612747?last_n_matchups=5
```
