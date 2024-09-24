import numpy as np
import pandas as pd


def fetch_medal_tally(data, year, country):
    medal_data = data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_data = medal_data
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_data = medal_data[medal_data['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_data = medal_data[medal_data['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_data = medal_data[(medal_data['Year'] == year) & (medal_data['region'] == country)]

    if flag == 1:
        x = temp_data.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_data.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                        ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x


def medal_tally(data):
    medal_tally = data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally


def country_year_list(data):
    year = data['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = np.unique(data['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year, country


def data_over_time(data, col):
    nations_over_time = data.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values(
        'Year')
    nations_over_time.rename(columns={"count": col}, inplace=True)
    return nations_over_time


def most_successful_athlete(data, sport):
    temp_data =data.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_data = temp_data[temp_data['Sport'] == sport]

    z = temp_data['Name'].value_counts().reset_index()
    z.columns = ['Name', 'Medals']
    z['Medals'] = z['Medals'].astype(str)

    merged = pd.merge(z,data, left_on='Name', right_on='Name', how='left').drop_duplicates(subset='Name')
    result= merged[['Name', 'Medals', 'Sport', 'region']]
    result.rename(columns={'Name': 'Athlete'}, inplace=True)
    return result


def year_wise_medal_tally(data,country):
    temp_data = data.dropna(subset=['Medal'])
    temp_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_data = temp_data[temp_data['region'] == country]
    final_data = new_data.groupby('Year').count()['Medal'].reset_index()
    return final_data

def country_event_heatmap(data,country):
    temp_data = data.dropna(subset=['Medal'])
    temp_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_data = temp_data[temp_data['region'] == country]
    pt = new_data.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_athlete_country_wise(data, country):
    temp_data =data.dropna(subset=['Medal'])
    temp_data = temp_data[temp_data['region'] == country]
    z = temp_data['Name'].value_counts().reset_index().head(10)
    z.columns = ['Name', 'Medals']
    z['Medals'] = z['Medals'].astype(str)
    merged = pd.merge(z,data, left_on='Name', right_on='Name', how='left').drop_duplicates(subset='Name')
    result= merged[['Name', 'Medals', 'Sport']]
    result.rename(columns={'Name': 'Athlete'}, inplace=True)
    return result

def men_vs_women(data):
    athlete_data = data.dropna(subset=['Name', 'region'])
    men = athlete_data[athlete_data['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_data[athlete_data['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)
    return final
