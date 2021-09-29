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

    st.title("""Welcome to the Game of Clue """)
    game_mode = st.radio('START HERE: Select Game Mode', ["Advisor", "Simulator(not Deployed)"])


    if game_mode == "Advisor":    
        st.sidebar.header("Game Configuration")
        st.sidebar.caption("Advisor Mode")
        st.sidebar.caption('Save Configuration and Start the Game')

        ## Unit of showing analytics and prompts
        col1, col2 = st.columns(2)
        show_log = col1.checkbox('Show analytics')
        if show_log:
            col1.dataframe(st.session_state.advisor_obj.log)
        col2.checkbox('show hint')


        number_of_player = st.sidebar.number_input(
            "Enter number of player:",
            min_value = 2, max_value = 20, value = 4, step=1,
        )

        if "advisor_obj" not in st.session_state:
            st.session_state.advisor_obj = None

        def init_advisor():
            ## format inputs
            inputs = []
            for j in range(1, number_of_player):
                keyname = "oppo_" + str(j)
                inputs.append(st.session_state[keyname])
            
            st.session_state.advisor_obj = advisor_mode(inputs, suspect_myself_have, weapon_myself_have, room_myself_have, number_of_player)

        with st.sidebar.form(key = "advisor_mode"):
            container = st.container()

            suspect_myself_have = st.multiselect("Suspect card(s) in your hand", LIST_SUSPECT)
            weapon_myself_have = st.multiselect("Weapon card(s) in your hand", LIST_WEAPON)
            room_myself_have = st.multiselect("Room card(s) in your hand", LIST_ROOM)

            # Enter name and number of cards of your opponents.
            for i in range(1, number_of_player):
                input = st.text_area("Enter the name of the opponent_" + str(i) + " and number of card he/she has, i.e Mia, 6", key = "oppo_" + str(i))

            container.form_submit_button(label='Start Game', on_click = init_advisor)


        def callback_myTurn():
            st.session_state.advisor_obj.update_myturn(st.session_state.mySuspectClaim_get, st.session_state.myWeaponClaim_get, 
                                                      st.session_state.myRoomClaim_get, st.session_state.mySuspect_claim, 
                                                      st.session_state.myWeapon_claim, st.session_state.myRoom_claim)
            st.session_state.advisor_obj.AI_unit_myselfTurn_update()
            st.session_state.advisor_obj.secret_Infer_Rebalance()
            st.session_state.advisor_obj.otherAgent_Rebalance()
            st.session_state.advisor_obj.add_recent_row_to_all_player("selfTurn")

        def callback_oppTurn():
            st.write("save other turn here")

        with st.form(key='my_form'):
            st.subheader("When it's your turn")
            col1, col2, col3, col4 = st.columns(4)
            myQuery_suspect = col1.selectbox("My Suspect Claim:  ", LIST_SUSPECT, key = "mySuspect_claim") 
            myQuery_weapon = col2.selectbox("My Weapon Claim:  ", LIST_WEAPON, key = "myWeapon_claim")
            myQuery_room = col3.selectbox("My Room Claim:  ", LIST_ROOM, key = "myRoom_claim")

            giver_potentials = [] if st.session_state.advisor_obj is None else [x for x in st.session_state.advisor_obj.players.keys() if x != "secret"] + ["None"]
            suspect_giver = col1.selectbox("Suspect Giver:  ", giver_potentials, key = "mySuspectClaim_get") 
            weapon_giver = col2.selectbox("Weapon Giver:  ", giver_potentials, key = "myWeaponClaim_get")
            room_giver = col3.selectbox("Room Giver:  ", giver_potentials, key = "myRoomClaim_get")

            col4.caption("Submit when confirmed")
            col4.form_submit_button(label='Submit', on_click = callback_myTurn)

        with st.form(key='other_form'):
            st.subheader("When it's others' turn")
            col1, col2, col3, col4 = st.columns(4)
            which_oppo = col1.selectbox("Whose turn", [] if st.session_state.advisor_obj is None else [x for x in st.session_state.advisor_obj.players.keys() if x != "secret" and x != "myself"])

            oppoQuery_suspect = col2.selectbox("Opponent's Suspect Claim:  ", LIST_SUSPECT, key = "opponent_sus_claim")
            oppoQuery_weapon = col3.selectbox("Opponent's Weapon Claim:  ", LIST_WEAPON, key = "opponent_wea_claim")
            oppoQuery_room = col2.selectbox("Opponent's Room Claim:  ", LIST_ROOM, key = "opponent_room_claim")

            giver_potentials = [] if st.session_state.advisor_obj is None else [x for x in st.session_state.advisor_obj.players.keys() if x != "secret"]
            cardGivers = col1.multiselect("Player(s) who give a card(including yourself) : ", giver_potentials)
            col4.caption("Submit when confirmed")
            col4.form_submit_button(label='Submit', on_click = callback_oppTurn)
        

        with st.form(key='magnifier'):
            st.subheader("When you have a chance to use Magnifier")
            col1, col2, col3, col4 = st.columns(4)
            person_check = col1.selectbox("who to check", [] if st.session_state.advisor_obj is None else [x for x in st.session_state.advisor_obj.players.keys() if x != "secret" and x != "myself"])
            card_get = col2.selectbox("card you get", LIST_SUSPECT + LIST_ROOM + LIST_WEAPON)
            col4.form_submit_button(label="Confirm")

        

        
    else:
        st.sidebar.header("Game Configuration")
        st.sidebar.caption("Simulation Mode")

if __name__ == '__main__':
    main()



