
from logging import raiseExceptions
import pandas as pd


import sys
sys.path.append("../utils/")
from agentAIUtils import search_in_must_have, myself_turn_players_update, secret_infer_helper, otherAgent_infer_helper, otherAgent_turnUpdate_3cardsCase, otherAgent_turnUpdate_OneTwo_cardsCase, otherAgent_turnUpdate_0cardsCase
from recommenderAIUtils import magnifier_recom_system, turn_recom_system
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card
from analytics import export_csv_helper

sys.path.append("../main/")
from Advisor_Algo_I import Advisor_Algo_I
from Player import Player
from Player import Secret

class advisor_modeI_frontend(Advisor_Algo_I):
    def __init__(self, opponents_info, suspect_myself_have, weapon_myself_have, room_myself_have, number_of_player):
        self.number_of_player = number_of_player
        ## get info I entered
        self.suspects, self.weapons, self.rooms = suspect_myself_have, weapon_myself_have, room_myself_have
        self.numcardsIhave = len(suspect_myself_have) + len(weapon_myself_have) + len(room_myself_have)
        ## init player set and myself agent
        self.players = {"myself": self.initPlayers(self.suspects, self.weapons, self.rooms, self.numcardsIhave)}
        ## init secret agent
        self.init_secret_agent()
        # parse other players inputs, and init other players 
        opponent_list_hashmap = self.parse_input_helper(opponents_info)
        self.init_other_agent(opponent_list_hashmap)
        ## init log
        self.log = self.initialize_log()
        ## init every player's score table
        self.add_recent_row_to_all_player("init")
        ## add the hint of myturn, speical for frontend
        self.myhint = turn_recom_system(self.players)


    def parse_input_helper(self, opponents_info):
        opponent_list_hashmap = {}
        for single_input in opponents_info:
            name, card_amount = single_input.split(",")[0].strip(), single_input.split(",")[1].strip()
            opponent_list_hashmap[name] = int(card_amount)
        return opponent_list_hashmap








