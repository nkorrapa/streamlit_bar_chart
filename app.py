import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def load_data(csv):
    df=pd.read_csv(csv)
    return df

st.header("Hockey Analysis")
st.write("This graph will allow you to view the number of shots the selected player has made, comparing their home vs away stats!")

pbp = load_data("data/2023pbp.csv")

st.dataframe(pbp)

pbp = pbp.sort_values("event_player_1_name", ascending=True)
players = pbp['event_player_1_name']
players = players.drop_duplicates(ignore_index=True)

player_name = st.selectbox("Pick a player", players.to_list(),index=None,
   placeholder="Select a player from the list to checkout stats!!")

player_shots = pbp[(pbp.event_player_1_name == player_name) & (pbp.event_type == 'SHOT')]

player_counts = player_shots.groupby('event_team_type', as_index=False).count()
player_counts = pd.DataFrame(player_counts)
player_counts = player_counts[['event_team_type','event']]

fig, ax = plt.subplots()
bar_colors = ['tab:red', 'tab:blue']
ax.bar(player_counts.event_team_type, player_counts.event, color = bar_colors)
ax.set_ylabel('Shots')
ax.set_title(player_name)
st.pyplot(fig= fig)
