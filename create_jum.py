# First we will import our packages
import pandas as pd
import numpy as np
from sklearn import linear_model,preprocessing
import requests
from nba_api.stats import endpoints
from matplotlib import pyplot as plt
import seaborn as sns

# Here we access the leagueleaders module through endpoints & assign the class to "data"
data = endpoints.leagueleaders.LeagueLeaders() 

# Our "data" variable now has built in functions such as creating a dataframe for our data
df = data.league_leaders.get_data_frame()
nba_df = pd.DataFrame(df)
graph = sns.pairplot(nba_df)
graph.savefig("pairplot.png")
plt.show()
# normalize each stats
sscaler = preprocessing.StandardScaler()
for x in nba_df.columns:
    sscaler.fit(x)
