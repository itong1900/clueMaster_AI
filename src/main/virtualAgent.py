from logging import raiseExceptions
import pandas as pd

from Advisor import Advisor
import sys
sys.path.append("../utils/")
from agentAIUtils import search_in_must_have, myself_turn_players_update, secret_infer_helper, otherAgent_infer_helper, otherAgent_turnUpdate_3cardsCase, otherAgent_turnUpdate_OneTwo_cardsCase, otherAgent_turnUpdate_0cardsCase
from recommenderAIUtils import magnifier_recom_system, turn_recom_system
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card
from analytics import export_csv_helper

sys.path.append("../main/")
from Player import Player
from Player import Secret

class virtualAgent:
    def __init__(self, agentName, opponent_list_hashmap, cards_I_draw, numberOfPlayers):
        self.agentName = agentName
        self.number_of_player = numberOfPlayers

        self.suspects, self.weapons, self.rooms = self.parse_cards_I_draw(cards_I_draw)
        self.numcardsIhave = len(self.suspectse) + len(self.weapons) + len(self.rooms)

        ## init player set and myself agent
        self.players = {"myself": self.initPlayers(self.suspects, self.weapons, self.rooms, self.numcardsIhave)}

        ## init secret agent
        self.init_secret_agent()

        ## init other agent
        self.init_other_agent(opponent_list_hashmap)

        ## init log
        self.log = self.initialize_log()

        ## init every player's score table
        self.add_recent_row_to_all_player("init")

        ## add the hint of myturn, speical for frontend
        self.myhint = turn_recom_system(self.players)

    def parse_cards_I_draw(self, cards_I_draw):
        suspects, weapons, rooms = [], [], []
        for card in cards_I_draw:
            if card in LIST_SUSPECT:
                suspects.append(card)
            elif card in LIST_WEAPON:
                weapons.append(card)
            elif card in LIST_WEAPON:
                rooms.append(card)
        return suspects, weapons, rooms
            

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