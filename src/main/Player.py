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

    def update_suspect_must_have(self, ele_add):
        self.suspect_must_have.add(ele_add)

    def update_weapon_must_have(self, ele_add):
        self.weapon_must_have.add(ele_add)
    
    def update_room_must_have(self, ele_add):
        self.room_must_have.add(ele_add)
    
    def update_suspect_possibly_have(self, list_add, points_added):
        pass
    
    def update_weapon_possibly_have(self, list_add, points_added):
        pass

    def update_room_possibly_have(self, list_add, points_added):
        pass

    def display_suspect_must_have(self):
        print(self.suspect_must_have)
    
    def display_weapon_must_have(self):
        print(self.weapon_must_have)

    def display_room_must_have(self):
        print(self.room_must_have)