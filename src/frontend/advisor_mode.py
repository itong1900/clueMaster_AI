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

class advisor_mode:
    def __init__(self, opponents_info, suspect_myself_have, weapon_myself_have, room_myself_have, number_of_player):
        self.round_num = 0

        self.numberOfPlayers = number_of_player

        ## get info I entered
        self.suspects, self.weapons, self.rooms = suspect_myself_have, weapon_myself_have, room_myself_have
        self.cardsIhave = len(suspect_myself_have) + len(weapon_myself_have) + len(room_myself_have)

        ## init player set and myself agent
        self.players = {"myself": self.initPlayers(self.suspects, self.weapons, self.rooms, self.cardsIhave)}

        ## init secret agent
        self.init_secret_agent()

        # parse other players inputs, and init other players 
        opponent_list_hashmap = self.parse_input_helper(opponents_info)
        self.init_other_agent(opponent_list_hashmap)

        ## init log
        self.log = self.initialize_log()

        ## init every player's score table
        self.add_recent_row_to_all_player("init")

        ## start the game
        self.turnCycle()
 


    def turnCycle(self):
        """
        The main round structure of the advisor mode.
        """
        while True:
            form = st.form(key="round_" + str(self.round_num))
            turn_container = form.container()
            whose_turn = st.selectbox('Whose turn: ', [x for x in self.players.keys() if x != "secret"], key = "whose_turn_" + str(self.round_num))

            if whose_turn == "myself":
                self.update_myturn(form)
            else:
                self.update_oppoTurn(whose_turn, form)
            self.round_num += 1

            if self.round_num >= 2:
                break
            

        # st.write(st.session_state.count)
        # if st.button("Next Turn"):
            
        #     st.write(st.session_state.count)
        #     whose_turn = st.selectbox('Whose turn: ', [x for x in self.players.keys() if x != "secret"])
        #     if whose_turn == "myself":
        #         self.update_myturn()
        #         self.AI_unit_myselfTurn_update()
        #         self.secret_Infer_Rebalance()
        #         self.otherAgent_Rebalance()
        #         self.add_recent_row_to_all_player("selfTurn")
        #     else:
                # self.update_oppoTurn(whose_turn)
                # self.AI_unit_otherTurn_update()
                # self.secret_Infer_Rebalance()
                # self.otherAgent_Rebalance()
                # self.add_recent_row_to_all_player("otherTurn")
                #pass
        
        # st.write(st.session_state.count)

        st.checkbox('Show Log')
        st.checkbox('Show suggestion')


    def parse_input_helper(self, opponents_info):
        opponent_list_hashmap = {}
        for single_input in opponents_info:
            name, card_amount = single_input.split(",")[0].strip(), single_input.split(",")[1].strip()
            opponent_list_hashmap[name] = int(card_amount)
        return opponent_list_hashmap

    def initPlayers(self, suspect_list, weapon_list, room_list, cardsIhave):
        """
        init myself Player Object
        """
        playerMyself = Player("myself", cardsIhave)
        for ele in suspect_list:
            playerMyself.update_suspect_must_have(ele)
        for ele in weapon_list:
            playerMyself.update_weapon_must_have(ele)
        for ele in room_list:
            playerMyself.update_room_must_have(ele)
        for ele in [x for x in LIST_SUSPECT if x not in suspect_list]:
            playerMyself.update_suspect_must_not_have(ele)
        for ele in [x for x in LIST_WEAPON if x not in weapon_list]:
            playerMyself.update_weapon_must_not_have(ele)
        for ele in [x for x in LIST_ROOM if x not in room_list]:
            playerMyself.update_room_must_not_have(ele)
        return playerMyself

    def init_secret_agent(self):
        """
        init secret and other players' Player Object
        """
        secret_suspect_prob_init = 1/len([x for x in LIST_SUSPECT if x not in self.suspects])
        secret_weapon_prob_init = 1/len([x for x in LIST_WEAPON if x not in self.weapons])
        secret_room_prob_init = 1/len([x for x in LIST_ROOM if x not in self.rooms])

        ## add secret agent
        secret = Secret("secret", 3)
        self.players["secret"] = secret
        for ele in self.suspects:
            self.players["secret"].update_suspect_must_not_have(ele)
        for ele in self.weapons:
            self.players["secret"].update_weapon_must_not_have(ele)
        for ele in self.rooms:
            self.players["secret"].update_room_must_not_have(ele)
        for ele in [x for x in LIST_SUSPECT if x not in self.suspects]:
            self.players["secret"].update_suspect_possibly_have(ele, secret_suspect_prob_init)
        for ele in [x for x in LIST_WEAPON if x not in self.weapons]:
            self.players["secret"].update_weapon_possibly_have(ele, secret_weapon_prob_init)
        for ele in [x for x in LIST_ROOM if x not in self.rooms]:
            self.players["secret"].update_room_possibly_have(ele, secret_room_prob_init)
        self.players["secret"].set_defaultBaseValue(suspect_value=secret_suspect_prob_init, weapon_value=secret_weapon_prob_init, room_value=secret_room_prob_init)

    def init_other_agent(self, opponent_list_hashmap):
        other_prob_init = 1/(Total_Number_of_Card - self.cardsIhave)
        for name in opponent_list_hashmap.keys():
            self.players[name] = Player(name, opponent_list_hashmap[name])
            this_prob_init = other_prob_init * self.players[name].numberOfCards

            for ele in self.suspects:
                self.players[name].update_suspect_must_not_have(ele)
            for ele in self.weapons:
                self.players[name].update_weapon_must_not_have(ele)
            for ele in self.rooms:
                self.players[name].update_room_must_not_have(ele)
            for ele in [x for x in LIST_SUSPECT if x not in self.suspects]:
                self.players[name].update_suspect_possibly_have(ele, this_prob_init)
            for ele in [x for x in LIST_WEAPON if x not in self.weapons]:
                self.players[name].update_weapon_possibly_have(ele, this_prob_init)
            for ele in [x for x in LIST_ROOM if x not in self.rooms]:
                self.players[name].update_room_possibly_have(ele, this_prob_init)

            self.players[name].set_defaultBaseValue(general_value=this_prob_init)


    def initialize_log(self):
        """
        initialize the log and return an empty dataframe with only column name row.
        """
        cols = ["player_makeQuery", 
                "claim_suspect", 
                "claim_weapon", 
                "claim_room", 
                "cards_received", 
                "card_giver(s)"]
        log = pd.DataFrame(index = range(0), columns = cols)
        return log

    def add_recent_row_to_all_player(self, updateEvent):
        """
        updateEvent will always be among {"init", "selfTurn", "otherTurn", "magnifier"}
        """
        if updateEvent not in {"init", "selfTurn", "otherTurn", "magnifier"}:
            raiseExceptions("new row type not valid")

        for player in self.players.keys():
            self.players[player].newScore_append(updateEvent)


    def update_myturn(self, stform):
        """
        With the claim I made, and the cards I collected, update the probability in 
        "myself" and other players' Player Objects. 
        """
        myQuery_suspect = stform.selectbox("My Suspect Claim:  ", LIST_SUSPECT, key = "mySuspect_claim_" + str(self.round_num)) 
        myQuery_weapon = stform.selectbox("My Weapon Claim:  ", LIST_WEAPON, key = "myWeapon_claim_" + str(self.round_num))
        myQuery_room = stform.selectbox("My Room Claim:  ", LIST_ROOM, key = "myRoom_claim_" + str(self.round_num))

        giver_potentials = [x for x in self.players.keys() if x != "secret"] + ["None"]
        suspect_giver = stform.selectbox("Suspect Giver:  ", giver_potentials, key = "mySuspectClaim_get_" + str(self.round_num)) 
        weapon_giver = stform.selectbox("Weapon Giver:  ", giver_potentials, key = "myWeaponClaim_get_" + str(self.round_num))
        room_giver = stform.selectbox("Room Giver:  ", giver_potentials, key = "myRoomClaim_get_" + str(self.round_num))

        stform.form_submit_button("Save Claim")
   
        if st.button("Next round", key = "next_round" + str(self.round_num)):
            listOfGiver = [suspect_giver, weapon_giver, room_giver]
            cardsCollected = 3 - listOfGiver.count("None")
            
            self.update_log("myself", myQuery_suspect, myQuery_weapon, myQuery_room, cardsCollected, listOfGiver)


    def AI_unit_myselfTurn_update(self):
        # Retrieve info from log
        player_makeQuery = self.log.iloc[-1,:]["player_makeQuery"]
        claim_suspect = self.log.iloc[-1,:]["claim_suspect"]
        claim_weapon = self.log.iloc[-1,:]["claim_weapon"]
        claim_room = self.log.iloc[-1,:]["claim_room"]
        cards_received = self.log.iloc[-1,:]["cards_received"]
        card_givers = self.log.iloc[-1,:]["card_giver(s)"]

        if player_makeQuery == "myself":
            ## deal with suspect
            not_in_must_have = search_in_must_have(self.players, claim_suspect, LIST_SUSPECT, LIST_WEAPON, LIST_ROOM) == "None"
            myself_turn_players_update("suspect", not_in_must_have, card_givers[0], card_givers, self.players, claim_suspect, cards_received)
            

            ## deal with weapon
            not_in_must_have = search_in_must_have(self.players, claim_weapon, LIST_SUSPECT, LIST_WEAPON, LIST_ROOM) == "None"
            myself_turn_players_update("weapon", not_in_must_have, card_givers[1], card_givers, self.players, claim_weapon, cards_received)

            ## deal with room
            not_in_must_have = search_in_must_have(self.players, claim_room, LIST_SUSPECT, LIST_WEAPON, LIST_ROOM) == "None"
            myself_turn_players_update("room", not_in_must_have, card_givers[2], card_givers, self.players, claim_room, cards_received)

    def AI_unit_otherTurn_update(self):
        # Retrieve info from log
        player_makeQuery = self.log.iloc[-1,:]["player_makeQuery"]
        claim_suspect = self.log.iloc[-1,:]["claim_suspect"]
        claim_weapon = self.log.iloc[-1,:]["claim_weapon"]
        claim_room = self.log.iloc[-1,:]["claim_room"]
        cards_received = self.log.iloc[-1,:]["cards_received"]
        card_givers = self.log.iloc[-1,:]["card_giver(s)"]

        if cards_received == 3:
            otherAgent_turnUpdate_3cardsCase(player_makeQuery, claim_suspect, claim_weapon, claim_room, card_givers, self.players)
        elif cards_received == 2:
            otherAgent_turnUpdate_OneTwo_cardsCase(player_makeQuery, claim_suspect, claim_weapon, claim_room, card_givers, self.players, "two")
        elif cards_received == 1:
            otherAgent_turnUpdate_OneTwo_cardsCase(player_makeQuery, claim_suspect, claim_weapon, claim_room, card_givers, self.players, "one")
        elif cards_received == 0:
            otherAgent_turnUpdate_0cardsCase(player_makeQuery, claim_suspect, claim_weapon, claim_room, self.players)


    def secret_Infer_Rebalance(self):
        """
        This method make straight forward inferences after each round and rebalance the score of secret agent after each round.
        """
        secret_infer_helper("suspect", LIST_SUSPECT, self.players, self.numberOfPlayers)
        secret_infer_helper("weapon", LIST_WEAPON, self.players, self.numberOfPlayers)
        secret_infer_helper("room", LIST_ROOM, self.players, self.numberOfPlayers)

        ## Rebalance here
        base_value_suspect_secret = self.players["secret"].getSecretBaseValue_suspect()
        for ele in self.players["secret"].suspect_possibly_have.keys():
            self.players["secret"].suspect_possibly_have[ele] = max(self.players["secret"].suspect_possibly_have[ele], base_value_suspect_secret)

        base_value_weapon_secret = self.players["secret"].getSecretBaseValue_weapon()
        for ele in self.players["secret"].weapon_possibly_have.keys():
            self.players["secret"].weapon_possibly_have[ele] = max(self.players["secret"].weapon_possibly_have[ele], base_value_weapon_secret)

        base_value_room_secret = self.players["secret"].getSecretBaseValue_room()
        for ele in self.players["secret"].room_possibly_have.keys():
            self.players["secret"].room_possibly_have[ele] = max(self.players["secret"].room_possibly_have[ele], base_value_room_secret)

        self.players["secret"].set_defaultBaseValue(suspect_value=base_value_suspect_secret,weapon_value=base_value_weapon_secret,room_value=base_value_room_secret)

       
    def otherAgent_Rebalance(self):
        exemptPlayers = {"myself", "secret"}
        for otherAgent in [x for x in self.players.keys() if x not in exemptPlayers]:
            ## Reverse Impact 
            otherAgent_infer_helper("suspect", self.players, otherAgent, self.numberOfPlayers)
            otherAgent_infer_helper("weapon", self.players, otherAgent, self.numberOfPlayers)
            otherAgent_infer_helper("room", self.players, otherAgent, self.numberOfPlayers)

            base_value = self.players[otherAgent].getBaseValue()
            prev_base_value = self.players[otherAgent].base_value_general
            if base_value == 0:
                continue
            ## deal with suspect
            for ele in self.players[otherAgent].suspect_possibly_have.keys():
                if base_value >= prev_base_value:
                    self.players[otherAgent].suspect_possibly_have[ele] = max(self.players[otherAgent].suspect_possibly_have[ele], base_value)
                else:  ## base_value < prev_base_value
                    if self.players[otherAgent].suspect_possibly_have[ele] <= prev_base_value:
                        self.players[otherAgent].suspect_possibly_have[ele] = base_value
                    else:
                        pass
            ## deal with weapon
            for ele in self.players[otherAgent].weapon_possibly_have.keys():
                if base_value >= prev_base_value:
                    self.players[otherAgent].weapon_possibly_have[ele] = max(self.players[otherAgent].weapon_possibly_have[ele], base_value)
                else:  ## base_value < prev_base_value
                    if self.players[otherAgent].weapon_possibly_have[ele] <= prev_base_value:
                        self.players[otherAgent].weapon_possibly_have[ele] = base_value
                    else:
                        pass
            ## deal with room
            for ele in self.players[otherAgent].room_possibly_have.keys():
                if base_value >= prev_base_value:
                    self.players[otherAgent].room_possibly_have[ele] = max(self.players[otherAgent].room_possibly_have[ele], base_value)
                else:  ## base_value < prev_base_value
                    if self.players[otherAgent].room_possibly_have[ele] <= prev_base_value:
                        self.players[otherAgent].room_possibly_have[ele] = base_value
                    else:
                        pass

            self.players[otherAgent].set_defaultBaseValue(general_value=base_value)


    def update_oppoTurn(self, whose_turn, stform):
        """
        Similar to the previous method, but the scenario of other players' turns. 
        """
        oppoQuery_suspect = st.selectbox(whose_turn+"'s"+" Suspect Claim:  ", LIST_SUSPECT)
        oppoQuery_weapon = st.selectbox(whose_turn+"'s"+"My Weapon Claim:  ", LIST_WEAPON)
        oppoQuery_room = st.selectbox(whose_turn+"'s"+"My Room Claim:  ", LIST_ROOM)
        
        giver_potentials = [x for x in self.players.keys() if x != "secret"]
        cardGivers = st.selectbox("Player(s) who give a card(including yourself, Enter None if no ones) : ", giver_potentials)

        stform.form_submit_button("Save Claim")

        cardGivers_list = [] if cardGivers == "None" else [x.strip() for x in cardGivers.split(",")]
        cardNumber = 0 if cardGivers == "None" else len(cardGivers_list)

        self.update_log(whose_turn, oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room, cardNumber, cardGivers_list)


    def update_log(self, playerName, claim_suspect, claim_weapon, claim_room, numberCards, cardGivers):
        """
        Attach the infomation collected in the new round to log table
        """
        self.log = self.log.append({"player_makeQuery": playerName, 
                                    "claim_suspect": claim_suspect,
                                    "claim_weapon": claim_weapon, 
                                    "claim_room": claim_room,
                                    "cards_received": numberCards, 
                                    "card_giver(s)": cardGivers}, ignore_index=True)