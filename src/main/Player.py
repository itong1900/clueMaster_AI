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
            self.suspect_possibly_have[ele] = points_added
        else:
            self.suspect_possibly_have[ele] += points_added
    
    def update_weapon_possibly_have(self, ele, points_added):
        if ele not in self.weapon_possibly_have:
            self.weapon_possibly_have[ele] = points_added
        else:
            self.weapon_possibly_have[ele] += points_added

    def update_room_possibly_have(self, ele, points_added):
        if ele not in self.room_possibly_have:
            self.room_possibly_have[ele] = points_added
        else:
            self.room_possibly_have[ele] += points_added

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