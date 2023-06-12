import get_shot_chart
import drawcourt


# Path: show_shot_chart.py
# Show shot chart of specific player

# Shaquille O'Neal
player_id = 406
# 2019-20 season
Season = "1999-00"
# All games
n_games = 0
# All teams
team_id = 0
# All opponents
opponent_id = 0
# All games
game_id = ""

# Get shot chart
shot_df = get_shot_chart.get_shotchart(team_id=team_id,opponent_id=opponent_id,player_id=player_id,Season=Season,game_id=game_id,n_games=n_games)

# Show shot chart
drawcourt.draw_court(outer_lines=True)
drawcourt.draw_shots(shot_df)
