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


def main():
    st.title("""Welcome to the Game of Clue """)
    game_mode = st.radio('START HERE: Select Game Mode', ["Advisor", "Simulator(not Deployed)"])

    if game_mode == "Advisor":    
        st.sidebar.title("Game Configuration")
        st.sidebar.caption("Advisor Mode")

        number_of_player = st.sidebar.number_input(
            "Enter number of player:",
            min_value = 2, max_value = 20, value = 4, step=1
        )

        suspect_myself_have = st.sidebar.multiselect("Suspect card(s) in your hand", LIST_SUSPECT)
        weapon_myself_have = st.sidebar.multiselect("Weapon card(s) in your hand", LIST_WEAPON)
        room_myself_have = st.sidebar.multiselect("Room card(s) in your hand", LIST_ROOM)

        # Enter name and number of cards of your opponents.
        inputs = []
        for i in range(1, number_of_player):
            input = st.sidebar.text_area("Enter the name of the opponent_" + str(i) + " and number of card he/she has, i.e Mia, 6")
            inputs.append(input)

        st.sidebar.text("Don't modify this part after game start, and recommend hide this part while playing")

        st.text('Click start the game when finishing editting configuration')
        if st.button('Start the game'):
            advisor_mode(inputs, suspect_myself_have, weapon_myself_have, room_myself_have, number_of_player)

    else:
        pass


def advisor_mode(opponents_info, suspect_myself_have, weapon_myself_have, room_myself_have, number_of_player):
    #parse input 
    opponent_list_hashmap = {}
    # for single_input in opponents_info:
    #     name, card_amount = single_input.split(",")[0].strip(), single_input.split(",")[1].strip()
    #     opponent_list_hashmap[name] = int(card_amount)

    st.checkbox('Show Log')
    st.checkbox('Show suggestion')

if __name__ == '__main__':
    main()









# st.selectbox('Select', [1,2,3])
# st.select_slider('Slide to select', options=[1,'2'])

