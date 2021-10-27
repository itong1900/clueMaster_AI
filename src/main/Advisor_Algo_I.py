from logging import raiseExceptions

from numpy import empty
from Player import Player
from Player import Secret
import pandas as pd


from Advisor_interface import Advisor_interface


import sys

sys.path.append("../utils/")
from agentAIUtils import search_in_must_have, myself_turn_players_update, secret_infer_helper, otherAgent_infer_helper, otherAgent_turnUpdate_3cardsCase, otherAgent_turnUpdate_OneTwo_cardsCase, otherAgent_turnUpdate_0cardsCase
from recommenderAIUtils import magnifier_recom_system, turn_recom_system
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card
from analytics import export_csv_helper

class Advisor_Algo_I(Advisor_interface):

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
        secret_infer_helper("suspect", LIST_SUSPECT, self.players, self.number_of_player)
        secret_infer_helper("weapon", LIST_WEAPON, self.players, self.number_of_player)
        secret_infer_helper("room", LIST_ROOM, self.players, self.number_of_player)

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
            otherAgent_infer_helper("suspect", self.players, otherAgent, self.number_of_player)
            otherAgent_infer_helper("weapon", self.players, otherAgent, self.number_of_player)
            otherAgent_infer_helper("room", self.players, otherAgent, self.number_of_player)

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


    def turn_recommendation(self):
        """
        Given recommendation when it's ur turn of moving 
        """
        return turn_recom_system(self.players)



