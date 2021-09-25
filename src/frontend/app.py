import streamlit as st
from logging import raiseExceptions
from numpy import empty
import pandas as pd

import sys
sys.path.append("../utils/")
from agentAIUtils import search_in_must_have, myself_turn_players_update, secret_infer_helper, otherAgent_infer_helper, otherAgent_turnUpdate_3cardsCase, otherAgent_turnUpdate_OneTwo_cardsCase, otherAgent_turnUpdate_0cardsCase
from recommenderAIUtils import magnifier_recom_system, turn_recom_system
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card
from analytics import export_csv_helper

sys.path.append("../main/")
from Player import Player
from Player import Secret

st.title("""
Welcome to the Game of Clue 
""")

st.sidebar.title(
    "Game Configuration"
)

st.sidebar.text(
    "START HERE(only when in Advisor Mode)"
)

number_of_player = st.sidebar.number_input(
    "Enter number of player:",
    min_value = 2, max_value = 20, value = 4, step=1
)


## TODO: add input validation
suspect_myself_have = st.sidebar.text_area(
    "Enter the suspect card in your hand, seperated by ','"
)


## TODO: add input validation
weapon_myself_have = st.sidebar.text_area(
    "Enter the weapon card in your hand, seperated by ','"
)

## TODO: add input validation
room_myself_have = st.sidebar.text_area(
    "Enter the room card in your hand, seperated by ','"
)

## Enter name and number of cards of your opponents.
# opponent_list = []
# for i in range(number_of_player):



st.sidebar.text(
    "Don't modify this part after game start, and recommend hide this part while playing"
)

game_mode = st.radio('Select Game Mode', ["Advisor", "Simulator"])

st.button('Start the game')

st.selectbox('Select', [1,2,3])
st.select_slider('Slide to select', options=[1,'2'])