import streamlit as st
from logging import raiseExceptions
from numpy import empty
import pandas as pd

from advisor_mode import advisor_mode

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
    container = st.container()

    container.title("""Welcome to the Game of Clue """)
    game_mode = container.radio('START HERE: Select Game Mode', ["Advisor", "Simulator(not Deployed)"])

    if game_mode == "Advisor":    
        st.sidebar.header("Game Configuration")
        st.sidebar.caption("Advisor Mode")


        form1 = st.sidebar.form(key = "advisor_mode")
        button_container = form1.container()
        form1.caption('Save Configuration and Start the Game')
        number_of_player = form1.number_input(
            "Enter number of player:",
            min_value = 2, max_value = 20, value = 4, step=1
        )

        suspect_myself_have = form1.multiselect("Suspect card(s) in your hand", LIST_SUSPECT)
        weapon_myself_have = form1.multiselect("Weapon card(s) in your hand", LIST_WEAPON)
        room_myself_have = form1.multiselect("Room card(s) in your hand", LIST_ROOM)

        # Enter name and number of cards of your opponents.
        inputs = []
        for i in range(1, number_of_player):
            input = form1.text_area("Enter the name of the opponent_" + str(i) + " and number of card he/she has, i.e Mia, 6")
            inputs.append(input)

        form1.caption("Don't modify this part after game start, and recommend hide this part while playing")
        button_container.form_submit_button("Start Game")

        if st.button("Next turn"):
            advisor_mode(inputs, suspect_myself_have, weapon_myself_have, room_myself_have, number_of_player)

    else:
        st.sidebar.header("Game Configuration")
        st.sidebar.caption("Simulation Mode")


    st.selectbox('Select', [1,2,3])
    st.select_slider('Slide to select', options=[1,'2'])


if __name__ == '__main__':
    main()



