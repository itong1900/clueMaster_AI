from logging import NullHandler, raiseExceptions
import math
import pandas as pd

import sys
sys.path.append("../utils/")
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card


class Player:
    
    def __init__(self, name, numberofCards):
        self.name = name
        self.numberOfCards = numberofCards
        self.suspect_must_have = set()
        self.weapon_must_have = set()
        self.room_must_have = set()
        self.suspect_possibly_have = {}
        self.weapon_possibly_have = {}
        self.room_possibly_have = {}
        self.suspect_must_not_have = set()
        self.weapon_must_not_have = set()
        self.room_must_not_have = set()

        self.base_value_general = None

        self.score_table = pd.DataFrame(index = range(0), columns = ["eventType"]+ LIST_SUSPECT + LIST_WEAPON + LIST_ROOM)


    def set_defaultBaseValue(self, general_value):
        self.base_value_general = general_value

    def update_suspect_must_have(self, ele_add):
        if ele_add in self.suspect_possibly_have.keys():
            del self.suspect_possibly_have[ele_add]
        self.suspect_must_have.add(ele_add)

    def update_weapon_must_have(self, ele_add):
        if ele_add in self.weapon_possibly_have.keys():
            del self.weapon_possibly_have[ele_add]
        self.weapon_must_have.add(ele_add)
    
    def update_room_must_have(self, ele_add):
        if ele_add in self.room_possibly_have.keys():
            del self.room_possibly_have[ele_add]
        self.room_must_have.add(ele_add)

    def update_suspect_must_not_have(self, ele_add):
        if ele_add in self.suspect_possibly_have.keys():
            del self.suspect_possibly_have[ele_add]
        self.suspect_must_not_have.add(ele_add)

    def update_weapon_must_not_have(self, ele_add):
        if ele_add in self.weapon_possibly_have.keys():
            del self.weapon_possibly_have[ele_add]
        self.weapon_must_not_have.add(ele_add)
    
    def update_room_must_not_have(self, ele_add):
        if ele_add in self.room_possibly_have.keys():
            del self.room_possibly_have[ele_add]
        self.room_must_not_have.add(ele_add)
    
    def update_suspect_possibly_have(self, ele, points_added):
        if ele not in self.suspect_possibly_have:
            if (ele not in self.suspect_must_not_have) and (ele not in self.suspect_must_have):
                self.suspect_possibly_have[ele] = points_added
        else:
            if self.suspect_possibly_have[ele] >= 0.5:
                self.suspect_possibly_have[ele] += math.log(1/2 + self.suspect_possibly_have[ele] + points_added, 5)
            else:
                self.suspect_possibly_have[ele] = max(points_added, self.suspect_possibly_have[ele])
    
    def update_weapon_possibly_have(self, ele, points_added):
        if ele not in self.weapon_possibly_have:
            if (ele not in self.weapon_must_not_have) and (ele not in self.weapon_must_have):
                self.weapon_possibly_have[ele] = points_added
        else:
            if self.weapon_possibly_have[ele] >= 0.5:
                self.weapon_possibly_have[ele] += math.log(1/2 + self.weapon_possibly_have[ele] + points_added, 5)
            else:
                self.weapon_possibly_have[ele] = max(points_added, self.weapon_possibly_have[ele])

    def update_room_possibly_have(self, ele, points_added):
        if ele not in self.room_possibly_have:
            if (ele not in self.room_must_not_have) and (ele not in self.room_must_have):
                self.room_possibly_have[ele] = points_added
        else:
            if self.room_possibly_have[ele] >= 0.5:
                self.room_possibly_have[ele] += math.log(1/2 + self.room_possibly_have[ele] + points_added, 5)
            else:
                self.room_possibly_have[ele] = max(points_added, self.room_possibly_have[ele])

    def display_suspect_must_have(self):
        print(self.suspect_must_have)
    
    def display_weapon_must_have(self):
        print(self.weapon_must_have)

    def display_room_must_have(self):
        print(self.room_must_have)

    def display_suspect_possibly_have(self):
        print(self.suspect_possibly_have)
    
    def display_weapon_possibly_have(self):
        print(self.weapon_possibly_have)
    
    def display_room_possibly_have(self):
        print(self.room_possibly_have)

    def display_suspect_must_not_have(self):
        print(self.suspect_must_not_have)
    
    def display_weapon_must_not_have(self):
        print(self.weapon_must_not_have)

    def display_room_must_not_have(self):
        print(self.room_must_not_have)

    def search_suspect_must_have(self, item_searching):
        if item_searching in self.suspect_must_have:
            return True
        return False

    def search_weapon_must_have(self, item_searching):
        if item_searching in self.weapon_must_have:
            return True
        return False

    def search_room_must_have(self, item_searching):
        if item_searching in self.room_must_have:
            return True
        return False

    ## Next 6 Methods to get the base value
    def getTotal_Unknown(self):
        result = len(self.suspect_possibly_have) + len(self.weapon_possibly_have) + len(self.room_possibly_have)
        # 30 - len(self.suspect_must_have) - len(self.room_must_have) - len(self.weapon_must_have) 
        # - len(self.suspect_must_not_have) - len(self.weapon_must_not_have) - len(self.room_must_not_have)
        if result > 0:
            return result
        return 0  ## It means this user has fully been hacked

    def getTotal_Musthave(self):
        return len(self.suspect_must_have) + len(self.room_must_have) + len(self.weapon_must_have)
    
    def getBaseValue(self):
        return (self.numberOfCards - self.getTotal_Musthave())/self.getTotal_Unknown()
        

    ## check if in must_not_have
    def check_in_must_not_have(self, checkItem):
        if checkItem in LIST_SUSPECT:
            return checkItem in self.suspect_must_not_have
        elif checkItem in LIST_WEAPON:
            return checkItem in self.weapon_must_not_have
        elif checkItem in LIST_ROOM:
            return checkItem in self.room_must_not_have

    ## check if in must_have
    def check_in_must_have(self, checkItem):
        if checkItem in LIST_SUSPECT:
            return checkItem in self.suspect_must_have
        elif checkItem in LIST_WEAPON:
            return checkItem in self.weapon_must_have
        elif checkItem in LIST_ROOM:
            return checkItem in self.room_must_have

    ## check if the ele in possibly set, if so, move to must_have
    def move_ele_possibly_to_must_have(self, ele):
        """
        move an ele from possibly-have set to must-have set
        """
        if ele in LIST_SUSPECT:
            if ele in self.suspect_possibly_have.keys():
                del self.suspect_possibly_have[ele]
            self.update_suspect_must_have(ele)
        elif ele in LIST_WEAPON:
            if ele in self.weapon_possibly_have.keys():
                del self.weapon_possibly_have[ele]
            self.update_weapon_must_have(ele)
        else:  ## objectDealing == "room"
            if ele in self.room_possibly_have.keys():
                del self.room_possibly_have[ele]
            self.update_room_must_have(ele)

    ## check if the ele in possibly set, if so, move to must_not_have
    def move_ele_possibly_to_must_not_have(self, ele):
        """
        move an ele from possibly-have set to must-not-have set
        """
        if ele in LIST_SUSPECT:
            if ele in self.suspect_possibly_have.keys():
                del self.suspect_possibly_have[ele]
            self.update_suspect_must_not_have(ele)
        elif ele in LIST_WEAPON:
            if ele in self.weapon_possibly_have.keys():
                del self.weapon_possibly_have[ele]
            self.update_weapon_must_not_have(ele)
        else:  ## objectDealing == "room"
            if ele in self.room_possibly_have.keys():
                del self.room_possibly_have[ele]
            self.update_room_must_not_have(ele)


    ## return How many cards not in must-have yet: CardsHave of the player - total_cards_in_must_have, for magnifier recommendation use.
    def get_not_in_must_have_yet(self):
        return self.numberOfCards - self.getTotal_Musthave()


    ## generate new row of score of this agent
    def newScore_row_generation(self):
        result = {}
        for ele in LIST_SUSPECT:
            if ele in self.suspect_must_have:
                result[ele] = 2
            elif ele in self.suspect_possibly_have.keys():
                result[ele] = self.suspect_possibly_have[ele]
            else:  ## ele in must_have
                result[ele] = 0
        
        for ele in LIST_WEAPON:
            if ele in self.weapon_must_have:
                result[ele] = 2
            elif ele in self.weapon_possibly_have.keys():
                result[ele] = self.weapon_possibly_have[ele]
            else:  ## ele in must_have
                result[ele] = 0

        for ele in LIST_ROOM:
            if ele in self.room_must_have:
                result[ele] = 2
            elif ele in self.room_possibly_have.keys():
                result[ele] = self.room_possibly_have[ele]
            else:  ## ele in must_have
                result[ele] = 0

        return result

    ## append the new row scores along with Type to each Agent
    def newScore_append(self, eventType):
        toAppend = self.newScore_row_generation()
        toAppend["eventType"] = eventType
        self.score_table = self.score_table.append(toAppend, ignore_index=True)
    
        
    def display_score_table(self):
        print(self.score_table)

    
    def display_player_summary(self, player_name):
        print(player_name)
        
        print("\n Base Value: ", self.base_value_general)
        
        print("\n ** suspect must have **:  ")
        self.display_suspect_must_have()
        print("\n suspect probably have:  ")
        self.display_suspect_possibly_have()
        print("\n suspect must not have:  ")
        self.display_suspect_must_not_have()

        print("\n ** weapon must have **:  ")
        self.display_weapon_must_have()
        print("\n weapon probably have:  ")
        self.display_weapon_possibly_have()
        print("\n weapon must not have:  ")
        self.display_weapon_must_not_have()
        
        print("\n ** room must have **:  ")
        self.display_room_must_have()
        print("\n room probably have:  ")
        self.display_room_possibly_have()
        print("\n room must not have:  ")
        self.display_room_must_not_have()



class Secret(Player):
    
    def __init__(self, name, numberofCards):
        """
        override init method
        """
        self.name = name
        self.numberOfCards = numberofCards
        self.suspect_must_have = set()
        self.weapon_must_have = set()
        self.room_must_have = set()
        self.suspect_possibly_have = {}
        self.weapon_possibly_have = {}
        self.room_possibly_have = {}
        self.suspect_must_not_have = set()
        self.weapon_must_not_have = set()
        self.room_must_not_have = set()

        self.base_value_secret_suspect = None
        self.base_value_secret_weapon = None
        self.base_value_secret_room = None

        self.score_table = pd.DataFrame(index = range(0), columns = ["eventType"]+ LIST_SUSPECT + LIST_WEAPON + LIST_ROOM)

    
    def set_defaultBaseValue(self, suspect_value, weapon_value, room_value):
        """
        override set_defaultBaseValue method 
        """
        self.base_value_secret_suspect = suspect_value
        self.base_value_secret_weapon = weapon_value
        self.base_value_secret_room = room_value

    ## Special get base value methods for secret agent
    def getSecretBaseValue_suspect(self):
        if len(self.suspect_possibly_have) != 0:
            return 1/len(self.suspect_possibly_have)
        return 0

    def getSecretBaseValue_weapon(self):
        if len(self.weapon_possibly_have) != 0:
            return 1/len(self.weapon_possibly_have)
        return 0

    def getSecretBaseValue_room(self):
        if len(self.room_possibly_have) != 0:
            return 1/len(self.room_possibly_have)
        return 0

    
    def display_player_summary(self, player_name):
        """override display_player_summary"""
        print(player_name)
        
        print("\n Suspect Base Value: ", self.base_value_secret_suspect)
        print("\n Weapon Base Value: ", self.base_value_secret_weapon)
        print("\n Room Base Value: ", self.base_value_secret_room)
    
        print("\n ** suspect must have **:  ")
        self.display_suspect_must_have()
        print("\n suspect probably have:  ")
        self.display_suspect_possibly_have()
        print("\n suspect must not have:  ")
        self.display_suspect_must_not_have()

        print("\n ** weapon must have **:  ")
        self.display_weapon_must_have()
        print("\n weapon probably have:  ")
        self.display_weapon_possibly_have()
        print("\n weapon must not have:  ")
        self.display_weapon_must_not_have()
        
        print("\n ** room must have **:  ")
        self.display_room_must_have()
        print("\n room probably have:  ")
        self.display_room_possibly_have()
        print("\n room must not have:  ")
        self.display_room_must_not_have()

