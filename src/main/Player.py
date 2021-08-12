from logging import raiseExceptions
import math

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

    def update_suspect_must_have(self, ele_add):
        self.suspect_must_have.add(ele_add)

    def update_weapon_must_have(self, ele_add):
        self.weapon_must_have.add(ele_add)
    
    def update_room_must_have(self, ele_add):
        self.room_must_have.add(ele_add)

    def update_suspect_must_not_have(self, ele_add):
        self.suspect_must_not_have.add(ele_add)

    def update_weapon_must_not_have(self, ele_add):
        self.weapon_must_not_have.add(ele_add)
    
    def update_room_must_not_have(self, ele_add):
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
                self.weapon_possibly_have[ele] += math.log(1/2 + self.weapon_possibly_have[ele] + points_added)
            else:
                self.weapon_possibly_have[ele] = max(points_added, self.weapon_possibly_have[ele])

    def update_room_possibly_have(self, ele, points_added):
        if ele not in self.room_possibly_have:
            if (ele not in self.room_must_not_have) and (ele not in self.room_must_have):
                self.room_possibly_have[ele] = points_added
        else:
            if self.room_possibly_have[ele] >= 0.5:
                self.room_possibly_have[ele] += math.log(1/2 + self.room_possibly_have[ele] + points_added)
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
        result = len(self.suspect_possibly_have) + len(self.room_possibly_have) + len(self.weapon_possibly_have) 
        if result > 0:
            return result
        raiseExceptions("This user is fully hacked on this category")

    def getTotal_Musthave(self):
        return len(self.suspect_must_have) + len(self.room_must_have) + len(self.weapon_must_have)
    
    def getBaseValue(self):
        return (self.numberOfCards - self.getTotal_Musthave())/self.getTotal_Unknown()
        
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