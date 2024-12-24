import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px

df = pd.read_csv('C:/Users/narendra tekale/ML-P1/dataset/athlete_events.csv')
region_df = pd.read_csv('C:/Users/narendra tekale/ML-P1/dataset/noc_regions.csv')

df=preprocessor.preprocess(df,region_df)

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year=st.sidebar.selectbox("Select year",years)
    selected_country = st.sidebar.selectbox("Select country", country)
    medal_tally=helper.fecth_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal tally in " + str(selected_year) + " olympics")
    if selected_year =='Overall' and selected_country != 'Overall':
        st.title("Overall Medal tally of " + selected_country)
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title("Medal tally of " + selected_country + " in "+ str(selected_year))
    st.dataframe(medal_tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Overall Analysis of Olympics ")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(nations_over_time, x='Edition', y='region')
    st.title("Participating Nation over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Edition', y='Event')
    st.title("Events over the years")
    st.plotly_chart(fig)

    athletes_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Edition', y='Name')
    st.title("Athletes over the years")
    st.plotly_chart(fig)

    st.title("Sports wise athlete medal tally")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Cricket')
    selected_sports=st.selectbox("Select a Sports",sport_list)
    x=helper.most_successful(df, selected_sports)
    st.table(x)

if user_menu == 'Country-wise Analysis':
    st.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.selectbox("Select a Country",country_list)
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country+" Medal tally over the year")
    st.plotly_chart(fig)
