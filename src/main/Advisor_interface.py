from logging import raiseExceptions

from numpy import empty
from Player import Player
from Player import Secret
import pandas as pd

import sys

sys.path.append("../utils/")
from agentAIUtils import search_in_must_have, myself_turn_players_update, secret_infer_helper, otherAgent_infer_helper, otherAgent_turnUpdate_3cardsCase, otherAgent_turnUpdate_OneTwo_cardsCase, otherAgent_turnUpdate_0cardsCase
from recommenderAIUtils import magnifier_recom_system, turn_recom_system
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card
from analytics import export_csv_helper

class Advisor_interface:

    def __init__(self, agentName, opponent_list_hashmap, cards_I_draw, numberOfPlayers):
        self.agentName = agentName
        self.number_of_player = numberOfPlayers
        self.suspects, self.weapons, self.rooms = self.parse_cards_I_draw(cards_I_draw)
        self.numcardsIhave = len(self.suspects) + len(self.weapons) + len(self.rooms)
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

    # ===================    
    # methods that collect the basic info of the game
    # ===================

    def parse_cards_I_draw(self, cards_I_draw):
        suspects, weapons, rooms = [], [], []
        for card in cards_I_draw:
            if card in LIST_SUSPECT:
                suspects.append(card)
            elif card in LIST_WEAPON:
                weapons.append(card)
            elif card in LIST_ROOM:
                rooms.append(card)
        return suspects, weapons, rooms

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
        other_prob_init = 1/(Total_Number_of_Card - self.numcardsIhave)
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

    def update_myturn(self, suspect_giver, weapon_giver, room_giver, myQuery_suspect, myQuery_weapon, myQuery_room):
        """
        With the claim I made, and the cards I collected, update the probability in 
        "myself" and other players' Player Objects. 
        """
        listOfGiver = [suspect_giver, weapon_giver, room_giver]
        cardsCollected = 3 - listOfGiver.count("None")
            
        self.update_log("myself", myQuery_suspect, myQuery_weapon, myQuery_room, cardsCollected, listOfGiver)
    
    def update_oppoTurn(self, whose_turn, cardGivers, oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room):
        """
        Similar to the previous method, but the scenario of other players' turns. 
        """
        #cardGivers_list = [] if cardGivers == "None" else [x.strip() for x in cardGivers.split(",")]
        cardNumber = len(cardGivers) ## 0 if cardGivers == "None" else len(cardGivers_list)

        self.update_log(whose_turn, oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room, cardNumber, cardGivers)

    def alertWin(self):
        """
        A method to alert the user when a winning condition is met.
        """
        if len(self.players["secret"].suspect_must_have) and len(self.players["secret"].weapon_must_have) and len(self.players["secret"].room_must_have):
            return True


    def exportAllTables(self):
        nameOfGame = input("Enter the name id of the Game")
        export_csv_helper(self.players, nameOfGame)
    # ===================    
    # abstract functions
    # ===================
    def AI_unit_myselfTurn_update(self):
        pass

    def AI_unit_otherTurn_update(self):
        pass

    def secret_Infer_Rebalance(self):
        pass

    def otherAgent_Rebalance(self):
        pass

    def magnifierCheck(self):
        pass

    def magnifier_recom(self):
        pass

    def turn_recommendation(self):
        pass




    


