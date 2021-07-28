class Advisor:
    # CONSTANTS in Advisor class
    global Total_Number_of_Card, LIST_SUSPECT, LIST_WEAPON, LIST_ROOM
    Total_Number_of_Card = 30
    LIST_SUSPECT = ["Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Colonel Mustard", "Professor Plum", "Miss Peach", "Sgt. Gray", "Monsieur Brunette", "Mme. Rose"]
    LIST_WEAPON = ["Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", "Wrench", "Horseshoe", "Poison"]
    LIST_ROOM = ["Carriage House", "Conservatory", "Kitchen", "Trophy Room", "Dining Room", "Drawing Room", "Gazebo", "Courtyard", "Fountain", "Library", "Billiard Room", "Studio"]
    
    def __init__(self, numberOfPlayers):
        """

        self.df_suspect : a real-time df showing probability of each suspect
        self.df_weapon  : a real-time df showing probability of each weapon
        self.df_room    : a real-time df showing probability of each room
        self.opponents  : a list of playerObject 
        """
        self.suspects, self.weapons, self.rooms = self.collectInfo(numberOfPlayers)
        self.initProbabilityTable(self.suspects, self.weapons, self.rooms)
        
        self.initialize_other_players(numberOfPlayers - 1)
        self.log = self.initialize_log()
        self.main()
        
    
    def main(self):
        while True:
            type_of_turn = input("Whose making a query: ")
            if type_of_turn == "myself":
                self.update_myturn()
                break
            else:
                pass
    
    def update_myturn(self):
        myQuery = input("My Claim:  ")
        myQuery_suspect, myQuery_weapon, myQuery_room = myQuery.split(",")[0].strip(), myQuery.split(",")[1].strip(), myQuery.split(",")[2].strip()
        if myQuery_suspect not in self.suspects:
            suspect_giver = input("Player who provides the suspect, enter None if nobody: ")
            if suspect_giver != "None":
                self.Opponents[suspect_giver].update_suspect_must_have(myQuery_suspect)
                #self.update_probability_table("suspect", myQuery_suspect)
        if myQuery_weapon not in self.weapons:
            weapon_giver = input("Player who provides the weapon, enter None if nobody: ")
            if weapon_giver != "None":
                self.Opponents[weapon_giver].update_weapon_must_have(myQuery_weapon)
                #self.update_probability_table("weapon", myQuery_weapon)
        if myQuery_room not in self.rooms:
            room_giver = input("Player who provides the room, enter None if nobody: ")
            if room_giver != "None":
                self.Opponents[room_giver].update_room_must_have(myQuery_room)
                #self.update_probability_table("room", myQuery_room)



    def initialize_other_players(self, numberOpponents):
        self.Opponents = {}
        for i in range(numberOpponents):
            playerInfo = input("Enter opponent's name, # of cards, seperated by comma, if no name or #ofcards given, it will be preset by the program\n")
            name, cardQuantity = playerInfo.split(",")[0].strip(), int(playerInfo.split(",")[1].strip())
            if name == "":
                name = "Player_" + str(i)
            # if not isinstance(cardQuantity, int):
            #     cardQuantity = 

            opponent = Player(name, cardQuantity)
            self.Opponents[name] = opponent

        
    def collectInfo(self, numberOfPlayers):

        cardPerPlayer = int((Total_Number_of_Card - 3)//numberOfPlayers)
        print("You should have " + str(cardPerPlayer) + " cards in your hand\n")

        while True:
            ## collect suspect
            print("Please enter your Suspect Cards, seperated by comma, enter None if you don't have suspect cards\n")
            txt = input("suspect(s): ")
            if txt == "None":
                suspects = []
            else:
                suspects = [x.strip() for x in txt.split(",")]
            print("\n")
            
            ## collect weapons
            print("Please enter your Weapon Cards, seperated by comma, enter None if you don't have weapon cards\n")       
            txt = input("weapon(s): ")
            if txt == "None":
                weapons = []
            else:
                weapons = [x.strip() for x in txt.split(",")]
            print("\n")

            ## collect rooms
            print("Please enter your Room Cards, seperated by comma, enter None if you don't have room cards\n")       
            txt = input("room(s): ")
            if txt == "None":
                rooms = []
            else:
                rooms = [x.strip() for x in txt.split(",")]
            print("\n")
            
            if len(rooms) + len(weapons) + len(suspects) != cardPerPlayer:
                print("incorrect total cards, enter again")
            else:
                break

        return suspects, weapons, rooms


    def initProbabilityTable(self, suspects, weapons, rooms):
        self.df_suspect = pd.DataFrame(index = range(1), columns = LIST_SUSPECT)
        probab = 1/(len(LIST_SUSPECT) - len(suspects))
        for col in self.df_suspect.columns:
            if col in suspects:
                self.df_suspect[col][0] = 0
            else:
                self.df_suspect[col][0] = probab
        
        self.df_weapon = pd.DataFrame(index = range(1), columns = LIST_WEAPON)
        probab = 1/(len(LIST_WEAPON) - len(weapons))
        for col in self.df_weapon.columns:
            if col in weapons:
                self.df_weapon[col][0] = 0
            else:
                self.df_weapon[col][0] = probab
        
        self.df_room = pd.DataFrame(index = range(1), columns = LIST_ROOM)
        probab = 1/(len(LIST_ROOM) - len(rooms))
        for col in self.df_room.columns:
            if col in rooms:
                self.df_room[col][0] = 0
            else:
                self.df_room[col][0] = probab

    def initialize_log(self):
        cols = ["player_makeQuery", "claim_suspect", "claim_weapon", "claim_room", "cards_received", "card_giver"]
        log = pd.DataFrame(index = range(0), columns = LIST_SUSPECT)
        return log

    # def update_probability_table(df, ele_eliminated):
    #     if df == "suspect":
    #         newRow = self.df_suspect.iloc[-1,:].copy()
    #         newRow[ele_eliminated] = 0
    #     elif df == "weapon":
        
    #     elif df == "room":



    #def construct_log(self, player_Query, suspect_queried, weapon_queried, room_queried, numberOfResponce, card_givers):
    