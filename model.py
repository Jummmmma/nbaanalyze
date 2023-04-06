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

# Create a linear regression model
# create an object that contains the lenear regression model
# Fit our modeling FGA and PPG
model = linear_model.LinearRegression()
model.fit(x, y)

# Get our r2 value and round it to 2 decimal places. How much of the variance in our data is explained by our model
# Get our predicted values
r2 = round(model.score(x, y), 2)
predicted_y  =model.predict(x)
