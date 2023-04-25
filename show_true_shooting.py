# First we will import our packages
import pandas as pd
import numpy as np
from sklearn import linear_model
import requests
from nba_api.stats import endpoints
from matplotlib import pyplot as plt

# Here we access the leagueleaders module through endpoints & assign the class to "data"
data = endpoints.leagueleaders.LeagueLeaders() 

# Our "data" variable now has built in functions such as creating a dataframe for our data
df = data.league_leaders.get_data_frame()

# First we need to get per game stats
# We divide each variable bi games played to get per game stats

# We have to reshape our data from 1D to 2D
# The proper shaped array is an input requirement for the linear regression model
def get_efg_graph(num1,num2):
    x, y = df.FGA / df.GP, df.PTS / df.GP
    xa, ya=x,y
    eFG = 100* df.PTS / (2 * (df.FGA + 0.44 * df.FTA))
    for i in range(len(x)):
        if df.GP[i] < 30:
            x[i] = 0
            eFG[i] = np.mean(eFG)
    x = np.array(x).reshape(-1, 1)
    eFG = np.array(eFG).reshape(-1, 1)
    eFG = np.nan_to_num(eFG)
    x1 = np.array([])
    y1 = np.array([])
    player1,player2,player1_1,player2_1 = 0,0,0,0
    # x from a large number to a small number
    zip_list = zip(x,eFG)
    zip_sort = sorted(zip_list,reverse=True)
    x,eFG = zip(*zip_sort)

    for i in range(num1-1,num2):
        x1 =np.append(x1,x[i])
        y1 =np.append(y1,eFG[i])

    for i in range(0,num2-num1+1):
        if y1[i]== np.max(y1):
            player1 = i
        if y1[i]== np.min(y1):
            player2 = i

    for i in range(len(x)):
        if xa[i] == x1[player1]:
            player1_1 = i
            player1 += num1-1
            break
    
    for i in range(len(x)):
        if xa[i] == x1[player2]:
            player2_1 = i
            player2 += num1-1
            break
  


    # Create a linear regression model
    # create an object that contains the lenear regression model
    # Fit our modeling FGA and PPG
    model = linear_model.LinearRegression()
    model.fit(x, eFG)

    # Get our r2 value and round it to 2 decimal places. How much of the variance in our data is explained by our model
    # Get our predicted values
    r2 = round(model.score(x, eFG), 2)
    predicted_y  =model.predict(x)

    # Now, lets make a plot with matplot lib using a iterative approach (which is easy to read)
    plt.scatter(x, eFG, s=15, alpha=.5)                            # Scatterplot:  Specfiy size(s) and transparency(alpha) of dots
    plt.plot(x, predicted_y, color = 'black')                    # line: Add line for regression line w/ predicted values
    plt.title('NBA - Relationship Between FGA and EFG')          # Give it a title
    plt.xlabel('FGA per Game')                                   # Label x-axis
    plt.ylabel('Effective Field Goal Percentage')                                # Label y-axis
    plt.text(10,25, f'R2={r2}')
    plt.annotate(df.PLAYER[player1_1],                       # This the name of the top scoring player. Refer to the .head() from earlier
                (x[player1], eFG[player1]),                       # This is the point we want to annotate.  
                (x[player1]-6,eFG[player1]-5),                    # These are coords for the text
                arrowprops=dict(arrowstyle='-'))    # Here we use a flat line for the arrow '-'
    plt.annotate(df.PLAYER[player2_1],                       # This the name of the top scoring player. Refer to the .head() from earlier
                 (x[player2], eFG[player2]),                       # This is the point we want to annotate.  
                 (x[player2]-5,eFG[player2]-5),                    # These are coords for the text
                 arrowprops=dict(arrowstyle='-'))   

    # Finally, let's save an image called 'graph.png'. 
    # We'll set the dpi (dots per inch) to 300, so we have a nice looking picture.
    plt.savefig('eFG.png', dpi=300)

# Show most and least eFG of Players who are shooting a lot of top num
get_efg_graph(1,60)
