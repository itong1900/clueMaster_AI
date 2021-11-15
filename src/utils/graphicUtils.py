

class locationObject:
    def __int__(self):
        self.distance_others = None

class Cloak_Room_Entry(locationObject):
    def __init__(self):
        self.name = "Cloak_Room_Entry"
        self.willStop = True
        self.distance_others = {"Trophy_Room": 6, "Magnifier_1": 6, "Kitchen": 8, "Magnifier_2": 7, "Dinning_Room": 6, "Magnifier_3": 8, "Magnifier_8": 3,
        "Courtyard": 6, "Library": 12, "Magnifier_7": 3, "Billiard_Room": 7, "Studio": 7, "Magnifier_9": 12, "Conservatory": 9}

class Carriage_House(locationObject):
    def __init__(self):
        self.name = "Carriage_House"
        self.willStop = True
        self.distance_others = {"Trophy_Room": 2}

class Kitchen(locationObject):
    def __init__(self):
        self.name = "Kitchen"
        self.willStop = True
        self.distance_others = {"Trophy_Room": 8, "Magnifier_1": 4, "Magnifier_2": 5, "Cloak_Room_Entry": 8, "Library": 0}

class Trophy_Room(locationObject):
    def __init__(self):
        self.name = "Trophy_Room"
        self.willStop = True
        self.distance_others = {"Carriage_House": 2, "Kitchen": 2, "Magnifier_1": 4, "Cloak_Room_Entry": 6, "Studio": 7, "Conservatory": 6, "Magnifier_9": 4}

class Dinning_Room(locationObject):
    def __init__(self):
        self.name = "Dinning_Room"
        self.willStop = True
        self.distance_others = {"Magnifier_2": 2, "Magnifier_3": 6, "Cloak_Room_Entry": 6}

class Drawing_Room(locationObject):
    def __init__(self):
        self.name = "Drawing_Room"
        self.willStop = True
        self.distance_others = {"Conservatory":0, "Magnifier_3": 4, "Courtyard": 8, "Magnifier_4": 7}

class Gazebo(locationObject):
    def __init__(self):
        self.name = "Gazebo"
        self.willStop = True
        self.distance_others = {"Magnifier_8": 3, "Courtyard": 5}

class Fountain(locationObject):
    def __init__(self):
        self.name = "Fountain"
        self.willStop = True
        self.distance_others = {"Magnifier_7": 3, "Courtyard": 5}

class Library(locationObject):
    def __init__(self):
        self.name = "Library"
        self.willStop = True
        self.distance_others = {"Kitchen": 0, "Magnifier_6": 5, "Billiard_Room": 7, "Cloak_Room_Entry": 12, "Magnifier_5": 4}

class Billiard_Room(locationObject):
    def __init__(self):
        self.name = "Billiard_Room"
        self.willStop = True
        self.distance_others = {"Studio": 4, "Cloak_Room_Entry": 7, "Library": 7, "Billiard_Room": 3}

class Studio(locationObject):
    def __init__(self):
        self.name = "Studio"
        self.willStop = True
        self.distance_others = {"Magnifier_9": 4,"Trophy_Room": 7, "Cloak_Room_Entry": 7, "Billiard_Room": 4}

class Conservatory(locationObject):
    def __init__(self):
        self.name = "Conservatory"
        self.willStop = True
        self.distance_others = {"Drawing_Room": 0, "Trophy_Room": 6, "Cloak_Room_Entry": 12, "Magnifier_9": 4}

class Magnifier_1(locationObject):
    def __init__(self):
        self.name = "Magnifier_1"
        self.willStop = False
        self.distance_others = {"Kitchen": 4, "Trophy_Room": 4, "Magnifier_2":7, "Cloak_Room_Entry": 6}


class Magnifier_2(locationObject):
    def __init__(self):
        self.name = "Magnifier_2"
        self.willStop = False
        self.distance_others = {"Kitchen": 5, "Magnifier_1": 7, "Cloak_Room_Entry": 7, "Dinning_Room": 2}


class Magnifier_3(locationObject):
    def __init__(self):
        self.name = "Magnifier_3"
        self.willStop = False
        self.distance_others = {"Drawing_Room": 4, "Cloak_Room_Entry": 8, "Dinning_Room": 6}

class Magnifier_4(locationObject):
    def __init__(self):
        self.name = "Magnifier_4"
        self.willStop = False
        self.distance_others = {"Drawing_Room": 7, "Courtyard": 4}

class Magnifier_5(locationObject):
    def __init__(self):
        self.name = "Magnifier_5"
        self.willStop = False
        self.distance_others = {"Library": 4, "Courtyard": 4}

class Magnifier_6(locationObject):
    def __init__(self):
        self.name = "Magnifier_6"
        self.willStop = False
        self.distance_others = {"Library": 5, "Billiard_Room": 3}

class Magnifier_7(locationObject):
    def __init__(self):
        self.name = "Magnifier_7"
        self.willStop = False
        self.distance_others = {"Fountain": 3, "Courtyard": 4}

class Magnifier_8(locationObject):
    def __init__(self):
        self.name = "Magnifier_8"
        self.willStop = False
        self.distance_others = {"Gazebo": 3, "Courtyard": 4}

class Magnifier_9(locationObject):
    def __init__(self):
        self.name = "Magnifier_9"
        self.willStop = False
        self.distance_others = {"Studio": 4, "Conservatory": 4, "Cloak_Room_Entry": 12}


