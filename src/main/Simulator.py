from logging import raiseExceptions

from numpy import empty, number
import random


from virtualAgent import virtualAgent
from Player import Player
from Player import Secret

import sys

sys.path.append("../utils/")
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card, SECRET_HOLDING


class Simulator:
    
    def __init__(self, numberOfPlayers):
        ## create the ground truth info of the game

        self.number_of_players = numberOfPlayers
        self.agent_hashmap = {"Player_" + str(x): None for x in range(numberOfPlayers)}
        self.shuffle_distribute_cards()
        self.someone_win = False
        self.turncount = 0
        
        # main turn cycle
        while not self.someone_win and self.turncount < 50:
            pass

    ## A helper method to get secret and players cards
    def shuffle_distribute_cards(self):
        deck_of_card = LIST_SUSPECT + LIST_WEAPON + LIST_ROOM
        #card_availability = {x: True for x in range(Total_Number_of_Card)}
        
        secret_suspect_index = random.randint(0, len(LIST_SUSPECT) - 1)
        secret_weapon_index = random.randint(len(LIST_SUSPECT), len(LIST_SUSPECT) + len(LIST_WEAPON) - 1)
        secret_room_index = random.randint(len(LIST_SUSPECT) + len(LIST_WEAPON), Total_Number_of_Card - 1)

        confidential_room = deck_of_card.pop(secret_room_index)
        confidential_weapon = deck_of_card.pop(secret_weapon_index)
        confidential_suspect = deck_of_card.pop(secret_suspect_index)
        self.secrets = [confidential_suspect, confidential_weapon, confidential_room]

        cardEachUser_base = (Total_Number_of_Card - SECRET_HOLDING) // self.number_of_players  ## 27 // 5 = 5 
        remainders = (Total_Number_of_Card - SECRET_HOLDING) % self.number_of_players  ## 27 % 5 = 2
        actual_card_each_player = [cardEachUser_base if i >= remainders else cardEachUser_base + 1 for i in range(self.number_of_players)]
        
        # distribute the rest of the cards into numberOfPlayers piles.
        for i in range(self.number_of_players):
            cards_player_draw = self.get_hand_of_card(actual_card_each_player[i], deck_of_card)
            opponent_list_hashmap = self.create_opponent_profile(i, actual_card_each_player)
            ## create the virtual Agent object
            self.agent_hashmap["Player_" + str(i)] = virtualAgent("Player_" + str(i), opponent_list_hashmap, cards_player_draw, self.number_of_players)
            

    def get_hand_of_card(self, cardNum, cardAvailable):
        result = []
        while cardNum > 0:
            result.append(cardAvailable.pop(random.randint(0, len(cardAvailable) - 1) ) )
            cardNum -= 1
        return result

    def create_opponent_profile(self, playerIdx, actual_card_each_player):
        result = {}
        for j in range(self.number_of_players):
            if j == playerIdx:
                continue
            result["Player_" + str(j)] = actual_card_each_player[j]
        result


        




