import matplotlib.pyplot as plt
import pandas as pd
import json
from nba_api.stats.endpoints import shotchartdetail,leaguedashptdefend,leaguedashptteamdefend,teamdashptshots,playerdashptshots
from nba_api.stats.static import players
import numpy as np
from IPython.display import display
import drawcourt

shot_zone_basic = ["Above the Break 3","Right Corner 3","Left Corner 3","Mid-Range","In The Paint (Non-RA)","Restricted Area"]
shot_zone_area = ["Center(C)","Right Side Center(RC)","Left Side Center(LC)","Left Side(L)","Right Side(R)"]

def get_shotchart(team_id=0,opponent_id=0,player_id =0,Season="",game_id="",n_games=0):
    player_shots = shotchartdetail.ShotChartDetail(team_id=team_id,player_id=player_id,opponent_team_id=opponent_id,season_nullable=Season,game_id_nullable=game_id,context_measure_simple="FGA",last_n_games=n_games)
    player_shots = json.loads(player_shots.get_json())
    shots = player_shots["resultSets"][0]["rowSet"]
    headers = player_shots["resultSets"][0]["headers"]
    shot_df = pd.DataFrame(shots, columns=headers)
    all_shots_num = len(shot_df)
    shot_position = pd.DataFrame(columns=["Accuracy","FGM/FGA in this Area","Shot_Type_Ratio","FGA in this Area/All Shots"])
    player_name = players.find_player_by_id(player_id)["full_name"]
    for basic in shot_zone_basic:
        for area in shot_zone_area:
            #各ゾーンでのシュートを絞る
            shots_each_area = shot_df[(shot_df.SHOT_ZONE_AREA == area) & (shot_df.SHOT_ZONE_BASIC == basic)]
            #その中で決まったものだけを絞る
            made_shots = shots_each_area[shots_each_area.SHOT_MADE_FLAG==1]
            #決まった本数
            made_shots_num = len(made_shots)
            #ゾーンの本数
            shots_num = len(shots_each_area)
            if shots_num == 0:
                continue
            shot_position.loc[basic+" and "+area] = [str(round(made_shots_num/shots_num*100,3))+"%",str(made_shots_num)+"/"+str(shots_num),str(round(shots_num/all_shots_num*100,3))+"%",str(shots_num)+"/"+str(all_shots_num)]

    #2P,3PのAccuracyを算出
    df_2pfg = shot_df[shot_df.SHOT_TYPE == "2PT Field Goal"]
    df_2pfg_made = df_2pfg[df_2pfg.SHOT_MADE_FLAG == 1]
    df_3pfg = shot_df[shot_df.SHOT_TYPE == "3PT Field Goal"]
    df_3pfg_made = df_3pfg[df_3pfg.SHOT_MADE_FLAG == 1]
    print("2PFG%" + "     " + str(round(len(df_2pfg_made)/len(df_2pfg)*100,3)) + "%")
    print("3PFG%" + "     " + str(round(len(df_3pfg_made)/len(df_3pfg)*100,3)) + "%")

    #可視化
    made = shot_df[shot_df.SHOT_MADE_FLAG == 1]
    miss = shot_df[shot_df.SHOT_MADE_FLAG == 0]
    plt.figure(figsize=(12,11))
    plt.scatter(made.LOC_X, made.LOC_Y,c="green")
    plt.scatter(miss.LOC_X, miss.LOC_Y,c="red")
    drawcourt.draw_court(outer_lines=True)
    plt.xlim(-250,250)
    plt.ylim(422.5, -47.5)
    # name the title "(Player Name) Shot Chart (Season)"
    plt.title(str(player_name) +" Shot Chart  ("+str(Season) + ")",fontsize=20)
    #コートの向き
#     plt.xlim(-300,300)
#     plt.ylim(-100,500)
    plt.savefig('shotchart.png', dpi=300)
    display(shot_position)