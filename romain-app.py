#import modules
import pandas as pd
import numpy as np
import streamlit as st

#our data
df = pd.read_csv('fpldata.csv')

#create metrics by 90
df["90s"] = df["minutes"]/90
calc_elements = ["goals", "assists", "points"]
for each in calc_elements:
    df[f"{each}_p90"] = df[each] / df["90s"]

#get distinct positions and teams
positions = list(df["position"].drop_duplicates())
teams = list(df["team"].drop_duplicates())

#create multi select filter for positions
position_choice = st.sidebar.multiselect(
    'Choose position:', positions, default=positions)

#create single select filter for teams
teams_choice = st.sidebar.selectbox(
    "Teams:", options=teams)

#create slider filter for price
price_choice = st.sidebar.slider(
    'Max Price:', min_value=4.0, max_value=15.0, step=.5, value=15.0)

#Make the filters we chose update the data when seleted
df = df[df['position'].isin(position_choice)]
df = df[df['team']==(teams_choice)]
df = df[df['cost'] < price_choice]

#formatting
st.title(f"Fantasy Football Analysis")
st.markdown("### Player Dataframe")

#display dataframe and sort it by point
st.dataframe(df.sort_values('points',
             ascending=False).reset_index(drop=True))

#This is our header
st.markdown('### Cost vs 20/21 Points')
#This is our plot
st.vega_lite_chart(df, {
     'mark': {'type': 'circle', 'tooltip': True},
     'encoding': {
         'x': {'field': 'cost', 'type': 'quantitative'},
         'y': {'field': 'points', 'type': 'quantitative'},
         'color': {'field': 'position', 'type': 'nominal'},
         'tooltip': [{"field": 'name', 'type': 'nominal'}, {'field': 'cost', 'type': 'quantitative'}, {'field': 'points', 'type': 'quantitative'}],
     },
     'width': 700,
     'height': 400,
 })
