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
x, y = df.FGA / df.GP, df.PTS / df.GP

# We have to reshape our data from 1D to 2D
# The proper shaped array is an input requirement for the linear regression model
x = np.array(x).reshape(-1, 1)
y = np.array(y).reshape(-1, 1)
x1 = np.array([])
y1 = np.array([])
for i in range(len(x)):
    if x[i]>18:
        x1 =np.append(x1,x[i])
        y1 =np.append(y1,y[i])
a = np.round(y1/x1,2)

for m in range(len(x1)):
    for n in range(len(x1)):
        if y1[m] > y1[n]:
            temp = y1[m]
            y1[m] = y1[n]
            y1[n] = temp
            temp = x1[m]
            x1[m] = x1[n]
            x1[n] = temp

for i in range(len(x)):
    if x[i] == x1[2] and y[i] == y1[2]:
        player1 = i

# for i in range(len(x)):
#     if x[i] == x1[np.argmax(a)] and y[i] == y1[np.argmax(a)]:
#         player1 = i
#     if x[i] == x1[np.argmin(a)] and y[i] == y1[np.argmin(a)]: 
#         player2 = i


# Create a linear regression model
# create an object that contains the lenear regression model
# Fit our modeling FGA and PPG
model = linear_model.LinearRegression()
model.fit(x, y)

# Get our r2 value and round it to 2 decimal places. How much of the variance in our data is explained by our model
# Get our predicted values
r2 = round(model.score(x, y), 2)
predicted_y  =model.predict(x)

# Now, lets make a plot with matplot lib using a iterative approach (which is easy to read)
plt.scatter(x, y, s=15, alpha=.5)                            # Scatterplot:  Specfiy size(s) and transparency(alpha) of dots
plt.plot(x, predicted_y, color = 'black')                    # line: Add line for regression line w/ predicted values
plt.title('NBA - Relationship Between FGA and PPG')          # Give it a title
plt.xlabel('FGA per Game')                                   # Label x-axis
plt.ylabel('Points Per Game')                                # Label y-axis
plt.text(10,25, f'R2={r2}')
plt.annotate(df.PLAYER[player1],                       # This the name of the top scoring player. Refer to the .head() from earlier
             (x[player1], y[player1]),                       # This is the point we want to annotate.  
             (x[player1]-7,y[player1]-2),                    # These are coords for the text
             arrowprops=dict(arrowstyle='-'))    # Here we use a flat line for the arrow '-'
# plt.annotate(df.PLAYER[player2],                       # This the name of the top scoring player. Refer to the .head() from earlier
#              (x[player2], y[player2]),                       # This is the point we want to annotate.  
#              (x[player2]-7,y[player2]-2),                    # These are coords for the text
#              arrowprops=dict(arrowstyle='-'))   

# Finally, let's save an image called 'graph.png'. 
# We'll set the dpi (dots per inch) to 300, so we have a nice looking picture.
plt.savefig('graph.png', dpi=300)