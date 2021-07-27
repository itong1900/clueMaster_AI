import pandas as pd
import numpy as np

class Advisor:
    global Total_Number_of_Card
    Total_Number_of_Card = 30
    LIST_SUSPECT = ["Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Colonel Mustard", "Professor Plum", "Miss Peach", "Sgt. Gray", "Monsieur Brunette", "Mme. Rose"]
    LIST_WEAPON = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench", "Horseshoe", "Poison"]
    LIST_ROOM = ["Carriage House", "Conservatory", "Kitchen", "Trophy Room", "Dining Room", "Drawing Room", "Gazebo", "Courtyard", "Fountain", "Library", "Billiard Room", "Studio"]
    def __init__(self, numberOfPlayers):
        cardPerPlayer = int((Total_Number_of_Card - 3)//numberOfPlayers)
        print("You should have " + str(cardPerPlayer) + " cards in your hand\n")
        suspects, weapons, rooms = self.collectInfo(cardPerPlayer)
    
        self.initpProbabilityTable(suspects, weapons, rooms)
        self.main()
        #self.log = 
    
    def main(self):
        while True:
            type_of_turn = input("Whose making a query: ")
            if type_of_turn == "myself":
                break
            else:
                pass
        
    def collectInfo(self, cardPerPlayer):
        suspects = []
        weapons = []
        rooms = []
        while True:
            ## collect suspect
            print("Please enter your Suspect Cards, enter 'That's all' when finished\n")
            for i in range(0, cardPerPlayer):
                ele = input("suspect: ")
                if ele == "That's all":
                    break
                else:
                    suspects.append(ele)
            
            ## collect weapons
            print("Please enter your Weapon Cards, enter 'That's all' when finished\n")       
            for i in range(0, cardPerPlayer):
                ele = input("weapon: ")
                if ele == "That's all":
                    break
                else:
                    weapons.append(ele)

            ## collect rooms
            print("Please enter your Room Cards, enter 'That's all' when finished\n")       
            for i in range(0, cardPerPlayer):
                ele = input("room: ")
                if ele == "That's all":
                    break
                else:
                    rooms.append(ele)
            
            if len(rooms) + len(weapons) + len(suspects) != cardPerPlayer:
                print("incorrect total cards, enter again")
            else:
                break
        return suspects, weapons, rooms


    def initpProbabilityTable(self, suspects, weapons, rooms):
        self.df_suspect = pd.DataFrame(index = range(50), columns = LIST_SUSPECT)
        probab = 1/(len(LIST_SUSPECT) - len(suspects))
        for col in self.df_suspect.columns:
            if col in suspects:
                self.df_suspect[col][0] = 0
            else:
                self.df_suspect[col][0] = probab
        
        self.df_weapon = pd.DataFrame(index = range(50), columns = LIST_WEAPON)
        probab = 1/(len(LIST_WEAPON) - len(weapons))
        for col in self.df_weapon.columns:
            if col in weapons:
                self.df_weapon[col][0] = 0
            else:
                self.df_weapon[col][0] = probab
        
        self.df_room = pd.DataFrame(index = range(50), columns = LIST_ROOM)
        probab = 1/(len(LIST_ROOM) - len(rooms))
        for col in self.df_room.columns:
            if col in rooms:
                self.df_room[col][0] = 0
            else:
                self.df_room[col][0] = probab