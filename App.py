import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import preprocessor, medal
from medal import medal_tally
from medal import country_year_list
from medal import data_over_time
from medal import most_successful_athlete
from medal import year_wise_medal_tally
from medal import country_event_heatmap
from medal import most_successful_athlete_country_wise

data = pd.read_csv("C:/Users/prata/OneDrive/Documents/athlete_events.csv")
region = pd.read_csv("C:/Users/prata/OneDrive/Documents/noc_regions.csv")
data = preprocessor.preprocess(data, region)

st.sidebar.title("Olympics Analysis")
option = st.sidebar.radio(
    'Select An Option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis')
)

if option == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    year, country = medal.country_year_list(data)
    selected_year = st.sidebar.selectbox("Select Year", year)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = medal.fetch_medal_tally(data, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(str(selected_country) + " Overall Performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(str(selected_country) + " Performance in " + str(selected_year))
    st.table(medal_tally)

if option == 'Overall Analysis':
    # Number of olympics edition
    edition = data['Year'].unique().shape[0] - 1

    # Number of cities
    cities = data['City'].unique().shape[0]

    # Number of sports and events
    sport = data['Sport'].unique().shape[0]
    event = data['Event'].unique().shape[0]

    # Number of athlete
    athlete = data['Name'].unique().shape[0]

    # Number of country
    nation = data['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.title("Editions")
        st.title(edition)
    with col2:
        st.title("Hosts")
        st.title(cities)
    with col3:
        st.title("Sports")
        st.title(sport)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.title("Events")
        st.title(event)
    with col2:
        st.title("Athletes")
        st.title(athlete)
    with col3:
        st.title("Nations")
        st.title(nation)

    nations_over_time = medal.data_over_time(data,'region')
    fig = px.line(nations_over_time, x="Year", y="region")
    st.title("Participation Nation Over The Years")
    st.plotly_chart(fig)

    events_over_time = medal.data_over_time(data,'Event')
    fig = px.line(events_over_time, x="Year", y="Event")
    st.title("Events Over The Years")
    st.plotly_chart(fig)

    athlete_over_time = medal.data_over_time(data, 'Name')
    fig = px.line(athlete_over_time, x="Year", y="Name")
    st.title("Athletes Over The Years")
    st.plotly_chart(fig)

    st.title("Numbers Of Event Over Time")
    fig,ax = plt.subplots(figsize=(25,25))
    y = data.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(y.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("Most Successful Athletes")
    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select A Sport',sport_list)
    z = medal.most_successful_athlete(data,selected_sport)
    st.table(z)

if option == "Country Wise Analysis":
    st.sidebar.title("Country Wise Analysis")
    country_list = data['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select A Country',country_list)
    country_data = medal.year_wise_medal_tally(data,selected_country)
    fig = px.line(country_data, x="Year", y="Medal")
    st.title(selected_country + " Medal Tally Over The Years")
    st.plotly_chart(fig)

    st.title(selected_country + " Excels In The Following Sports")
    pt = medal.country_event_heatmap(data,selected_country)
    fig, ax = plt.subplots(figsize=(25, 25))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title("Top 10 Athletes Of "+ selected_country)
    top_athlete_data = medal.most_successful_athlete_country_wise(data,selected_country)
    st.table(top_athlete_data)

if option == 'Athlete Wise Analysis':
    athlete_data = data.dropna(subset=['Name', 'region'])
    x1 = athlete_data['Age'].dropna()
    x2 = athlete_data[athlete_data['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_data[athlete_data['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_data[athlete_data['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                       show_hist=False, show_rug=False)
    st.title("Distribution Of Age")
    st.plotly_chart(fig)

    st.title("Men VS Women Participation Over The Years")
    final = medal.men_vs_women(data)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    st.plotly_chart(fig)















