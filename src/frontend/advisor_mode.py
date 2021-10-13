
from logging import raiseExceptions
import pandas as pd


import sys
sys.path.append("../utils/")
from agentAIUtils import search_in_must_have, myself_turn_players_update, secret_infer_helper, otherAgent_infer_helper, otherAgent_turnUpdate_3cardsCase, otherAgent_turnUpdate_OneTwo_cardsCase, otherAgent_turnUpdate_0cardsCase
from recommenderAIUtils import magnifier_recom_system, turn_recom_system
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card
from analytics import export_csv_helper

sys.path.append("../main/")
from Advisor import Advisor
from Player import Player
from Player import Secret

class advisor_mode(Advisor):
    def __init__(self, opponents_info, suspect_myself_have, weapon_myself_have, room_myself_have, number_of_player):
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

        ## add the hint of myturn, speical for frontend
        self.myhint = turn_recom_system(self.players)
        

    def parse_input_helper(self, opponents_info):
        opponent_list_hashmap = {}
        for single_input in opponents_info:
            name, card_amount = single_input.split(",")[0].strip(), single_input.split(",")[1].strip()
            opponent_list_hashmap[name] = int(card_amount)
        return opponent_list_hashmap



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

    def turn_recommendation(self):
        """
        Given recommendation when it's ur turn of moving 
        """
        return turn_recom_system(self.players)



    def magnifierCheck(self, playerName, cardGot):
        """
        magnifer check by other players doesn't bring extra straightforward info here, we'll skip those cases
        """
        ## determine what card is this
        if cardGot in LIST_SUSPECT:
            if cardGot in self.players[playerName].suspect_possibly_have.keys():
                self.players[playerName].update_suspect_must_have(cardGot)
                #del self.players[playerName].suspect_possibly_have[cardGot]
                ## put the cardGot in must-not-have in other agent, and remove from their possibly have as well
                for other_agent in [x for x in self.players.keys() if x != playerName]:
                    if cardGot in self.players[other_agent].suspect_possibly_have.keys():
                        self.players[other_agent].update_suspect_must_not_have(cardGot)
                        #del self.players[other_agent].suspect_possibly_have[cardGot]
            elif cardGot in self.players[playerName].suspect_must_not_have:
                raiseExceptions("impossible to catch a card in must-not-have class, set up wrong, or someone forgets to give a card")
        elif cardGot in LIST_WEAPON:
            if cardGot in self.players[playerName].weapon_possibly_have.keys():
                self.players[playerName].update_weapon_must_have(cardGot)
                #del self.players[playerName].weapon_possibly_have[cardGot]
                ## put the cardGot in must-not-have in other agent, and remove from their possibly have as well
                for other_agent in [x for x in self.players.keys() if x != playerName]:
                    if cardGot in self.players[other_agent].weapon_possibly_have.keys():
                        self.players[other_agent].update_weapon_must_not_have(cardGot)
                        #del self.players[other_agent].weapon_possibly_have[cardGot]
            elif cardGot in self.players[playerName].weapon_must_not_have:
                raiseExceptions("impossible to catch a card in must-not-have class, set up wrong, or someone forgets to give a card")
        elif cardGot in LIST_ROOM:
            if cardGot in self.players[playerName].room_possibly_have.keys():
                self.players[playerName].update_room_must_have(cardGot)
                #del self.players[playerName].room_possibly_have[cardGot]
                ## put the cardGot in must-not-have in other agent, and remove from their possibly have as well
                for other_agent in [x for x in self.players.keys() if x != playerName]:
                    if cardGot in self.players[other_agent].room_possibly_have.keys():
                        self.players[other_agent].update_room_must_not_have(cardGot)
                        #del self.players[other_agent].room_possibly_have[cardGot]
            elif cardGot in self.players[playerName].room_must_not_have:
                raiseExceptions("impossible to catch a card in must-not-have class, set up wrong, or someone forgets to give a card")
        else:
            raiseExceptions("invalid card type in magnifier method")

    def magnifier_recom(self):
        """
        Give recommendation if a magnifier opportunity is given
        """
        return magnifier_recom_system(self.players)

    def add_recent_row_to_all_player(self, updateEvent):
        """
        updateEvent will always be among {"init", "selfTurn", "otherTurn", "magnifier"}
        """
        if updateEvent not in {"init", "selfTurn", "otherTurn", "magnifier"}:
            raiseExceptions("new row type not valid")

        for player in self.players.keys():
            self.players[player].newScore_append(updateEvent)
        
        ## add the hint of myturn, speical for frontend
        self.myhint = turn_recom_system(self.players)


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






