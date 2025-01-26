# NBA Stats and Projections API

A comprehensive FastAPI-based application that provides NBA player statistics and hit rate calculations for player prop projections. This API integrates with the official NBA API to provide detailed player statistics, game logs, and statistical threshold analysis.

## Features

### Player Statistics
- Career statistics
- Game logs with filtering by season
- Advanced player metrics
- Shot dashboard and analytics
- Player vs player comparisons
- Hustle stats and tracking data

### Hit Rate Analysis
Calculates success rates for various statistical thresholds over a specified number of games:

**Points**
- 10+, 15+, 20+, 25+, 30+, 35+ points

**Assists**
- 2+, 4+, 6+, 8+, 10+ assists

**Rebounds**
- 4+, 6+, 8+, 10+, 12+, 14+, 16+ rebounds

**Three-Pointers**
- 1+, 2+, 3+, 4+, 5+, 6+, 7+, 8+ three-pointers made

**Defensive Stats**
- Steals: 1+, 2+, 3+, 4+
- Blocks: 1+, 2+, 3+, 4+

## Setup

### Prerequisites
- Python 3.13+
- Windows 10 (for these instructions)

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd nba_stat_projection
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8002`

## API Endpoints

### Basic Player Stats
- `GET /player/career/{player_id}` - Get career statistics
- `GET /player/games/{player_id}` - Get game logs (optional season parameter)
- `GET /player/advanced/{player_id}` - Get advanced statistics
- `GET /player/info/{player_id}` - Get detailed player information

### Hit Rate Analysis
- `GET /player/hit-rates/{player_id}`
  - Parameters:
    - `num_games` (optional, default=10): Number of recent games to analyze
    - `season` (optional): NBA season in format '2023-24'
  - Returns hit rates for all statistical categories

### Team and League Stats
- `GET /team/games/{team_id}` - Get team game logs
- `GET /team/stats` - Get comprehensive team statistics
- `GET /league/players` - Get league-wide player statistics
- `GET /league/hustle` - Get league-wide hustle statistics

### Advanced Analytics
- `GET /player/shots/{player_id}` - Get shot dashboard
- `GET /player/hustle/{game_id}` - Get hustle stats for a game
- `GET /game/tracking/{game_id}` - Get player tracking stats
- `GET /game/advanced/{game_id}` - Get advanced box score
- `GET /player/vs/{player_id}/{vs_player_id}` - Get head-to-head stats

## Usage Examples

1. Get Nikola Jokić's hit rates for the last 10 games:
```
GET http://localhost:8002/player/hit-rates/203999
```

2. Get hit rates for specific number of games:
```
GET http://localhost:8002/player/hit-rates/203999?num_games=5
```

3. Get hit rates for current season:
```
GET http://localhost:8002/player/hit-rates/203999?season=2023-24
```

Example Response:
```json
{
  "points": {
    "20+": {
      "fraction": "8/10",
      "percentage": 80.0
    }
  },
  "assists": {
    "6+": {
      "fraction": "7/10",
      "percentage": 70.0
    }
  }
  // ... other categories
}
```

## Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8002/docs`
- ReDoc: `http://localhost:8002/redoc`

## Common Player IDs
- Nikola Jokić: 203999
- Joel Embiid: 203954
- Stephen Curry: 201939
- LeBron James: 2544
- Giannis Antetokounmpo: 203507

## Error Handling

The API includes comprehensive error handling and logging:
- Invalid player IDs return appropriate error messages
- Network issues with the NBA API are properly handled
- Data processing errors include detailed error messages

## Development

The project structure:
```
nba_stat_projection/
├── data/
│   └── data_loader.py      # NBA API integration
├── utils/
│   └── hit_rate_calculator.py  # Hit rate calculations
├── main.py                 # FastAPI application
└── requirements.txt        # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
