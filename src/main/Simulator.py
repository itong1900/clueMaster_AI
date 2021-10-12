from logging import raiseExceptions

from numpy import empty, number
import random

from Player import Player
from Player import Secret

import sys

sys.path.append("../utils/")
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card, SECRET_HOLDING


class Simulator:
    
    def __init__(self):
        ## create the ground truth info of the game

        #self.number_of_players = number_of_players
        
        self.shuffle_distribute_cards()

    ## A helper method to get secret and players cards
    def shuffle_distribute_cards(self):
        deck_of_card = LIST_SUSPECT + LIST_WEAPON + LIST_ROOM
        card_availability = {x: True for x in range(Total_Number_of_Card)}
        
        secret_suspect_index = random.randint(0, len(LIST_SUSPECT) - 1)
        secret_weapon_index = random.randint(len(LIST_SUSPECT), len(LIST_SUSPECT) + len(LIST_WEAPON) - 1)
        secret_room_index = random.randint(len(LIST_SUSPECT) + len(LIST_WEAPON), Total_Number_of_Card - 1)

        card_availability[secret_suspect_index] = False
        card_availability[secret_weapon_index] = False
        card_availability[secret_room_index] = False

        print(deck_of_card[secret_suspect_index])
        print(deck_of_card[secret_weapon_index])
        print(deck_of_card[secret_room_index])
        




