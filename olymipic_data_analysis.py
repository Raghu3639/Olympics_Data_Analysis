import pandas as pd
import numpy as np
import plotly.express as px


data = pd.read_csv("C:/Users/prata/OneDrive/Documents/athlete_events.csv")
region = pd.read_csv("C:/Users/prata/OneDrive/Documents/noc_regions.csv")

data.info()
data.shape

# Medal Tally

# Changing the whole olympic data into summer olympic data
data = data[data['Season']=='Summer']
data.shape

# Merging the region column into the data
data = data.merge(region,on='NOC',how='left')

# Number of country participated
data['region'].unique().shape

# Missing values
data.isnull().sum()

# Checking duplicate values and removing 
data.duplicated().sum()
data.drop_duplicates(inplace=True)
data.duplicated().sum()

# Counting the medals and converting them into columns and concatenate into actual data
data['Medal'].value_counts()

data = pd.concat([data,pd.get_dummies(data['Medal'])],axis=1)

# Represinting medals on the behalf of their country
medal_tally = data.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
medal_tally['Total'] = medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']
medal_tally

# Sorting years
year = data['Year'].unique().tolist()
year.sort()
year.insert(0,'Overall')
year

# Sorting regions
country = np.unique(data['region'].dropna().values).tolist()
country.sort()
country.insert(0,'Overall')
country

# Creating a function through which year and country shown according to that
def fetch_medal_tally(data,year,country):
    medal_data = data.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal']) 
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_data = medal_data
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_data = medal_data[medal_data['region']==country]
    if year != 'Overall' and country == 'Overall':
        temp_data = medal_data[medal_data['Year']==int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_data = medal_data[(medal_data['Year']== year) & (medal_data['region']== country)]
        
    if flag ==1:
        x = temp_data.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_data.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
     
    x['Total'] = x['Gold']+x['Silver']+x['Bronze']
    print(x)
    
fetch_medal_tally(year = 'Overall', country = 'Overall')  

# Overall Analysis

# Number of olympics edition
data['Year'].unique().shape[0]-1

# Number of cities
data['City'].unique().shape

# Number of sports and events
data['Sport'].unique().shape
data['Event'].unique().shape

# Number of athelete
data['Name'].unique().shape

# Number of country
data['region'].unique().shape

nations_over_time = data.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('Year')
nations_over_time.rename(columns ={"count":'No of Countries'},inplace=True)
fig = px.line(nations_over_time, x = "Year",y = "No of Countries")
fig.show()
