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
        self.players    : a list of playerObject 
        """
        self.suspects, self.weapons, self.rooms, self.cardsIhave = self.collectInfo()
        self.players = {"myself": self.initPlayers(self.suspects, self.weapons, self.rooms, self.cardsIhave)}

        self.initProbabilityTable(self.suspects, self.weapons, self.rooms)
        
        self.initialize_other_players(numberOfPlayers - 1)
        self.log = self.initialize_log()
        self.turnCycle()
        
    
    def turnCycle(self):
        while True:
            action = input("Next turn / Query / Exit: ")
            if action == "Next turn":
                whose_turn = input("Whose turn is this: ")
                if whose_turn == "myself":
                    self.update_myturn()
                    #break
                elif whose_turn in self.players:
                    self.update_oppoTurn(whose_turn)
                    #break
                else:
                    print("Wrong name, enter again: ")
            elif action == "Query":
                what_query = input("Player_Summary / Log / Probability_Table:  ")
                if what_query == "Log":
                    self.display_log()
                elif what_query == "Player_Summry":
                    pass
            elif action == "Exit":
                break
            print("\n")
    
    def update_myturn(self):
        myQuery = input("My Claim:  ")
        myQuery_suspect, myQuery_weapon, myQuery_room = myQuery.split(",")[0].strip(), myQuery.split(",")[1].strip(), myQuery.split(",")[2].strip()

        response = input("Player who provides the suspect, weapon, room, enter None if nobody: ")
        suspect_giver, weapon_giver, room_giver = response.split(",")[0].strip(), response.split(",")[1].strip(), response.split(",")[2].strip() 

        cardsCollected = 0
        listOfGiver = []
        if myQuery_suspect not in self.suspects:
            if suspect_giver != "None":
                cardsCollected += 1
                listOfGiver.append(suspect_giver)
                self.players[suspect_giver].update_suspect_must_have(myQuery_suspect)
                #self.update_probability_table("suspect", myQuery_suspect)
        else:
            listOfGiver.append("myself")
            cardsCollected += 1

        if myQuery_weapon not in self.weapons:
            if weapon_giver != "None":
                cardsCollected += 1
                listOfGiver.append(weapon_giver)
                self.players[weapon_giver].update_weapon_must_have(myQuery_weapon)
                #self.update_probability_table("weapon", myQuery_weapon)
        else:
            listOfGiver.append("myself")
            cardsCollected += 1

        if myQuery_room not in self.rooms:
            if room_giver != "None":
                cardsCollected += 1
                listOfGiver.append(room_giver)
                self.players[room_giver].update_room_must_have(myQuery_room)
                #self.update_probability_table("room", myQuery_room)
        else:
            listOfGiver.append("myself")
            cardsCollected += 1
        
        self.udpate_log("myself", myQuery_suspect, myQuery_weapon, myQuery_room, cardsCollected, listOfGiver)

    def update_oppoTurn(self, whose_turn):
        oppoQuery = input(whose_turn + "'s Claim:  ")
        oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room = oppoQuery.split(",")[0].strip(), oppoQuery.split(",")[1].strip(), oppoQuery.split(",")[2].strip()
        
        cardGivers = input("Player(s) who give a card(including yourself, Enter None if no ones) : ")
        cardGivers_list = [x.strip() for x in cardGivers.split(",")]
        cardNumber = 0 if cardGivers == "None" else len(cardGivers_list)

        self.udpate_log(whose_turn, oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room, cardNumber, cardGivers_list)

    def initPlayers(self, suspect_list, weapon_list, room_list, cardsIhave):
        playerMyself = Player("myself", cardsIhave)
        for ele in suspect_list:
            playerMyself.update_suspect_must_have(ele)
        for ele in weapon_list:
            playerMyself.update_weapon_must_have(ele)
        for ele in room_list:
            playerMyself.update_room_must_have(ele)
        return playerMyself


    def initialize_other_players(self, numberOpponents):
        
        for i in range(numberOpponents):
            playerInfo = input("Enter opponent's name, # of cards, seperated by comma, if no name or #ofcards given, it will be preset by the program\n")
            name, cardQuantity = playerInfo.split(",")[0].strip(), int(playerInfo.split(",")[1].strip())
            if name == "":
                name = "Player_" + str(i)
            # if not isinstance(cardQuantity, int):
            #     cardQuantity = 

            opponent = Player(name, cardQuantity)
            self.players[name] = opponent

        
    def collectInfo(self):

        while True:
            ## collect number of cards
            txt = input("Please enter number of cards you have:  ")
            cardsIhave = int(txt)
            print("\n")

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
            
            # 
            # Data Validation
            # else:
            break

        return suspects, weapons, rooms, cardsIhave


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
        cols = ["player_makeQuery", 
                "claim_suspect", 
                "claim_weapon", 
                "claim_room", 
                "cards_received", 
                "card_giver(s)"]
        log = pd.DataFrame(index = range(0), columns = cols)
        return log

    def udpate_log(self, playerName, claim_suspect, claim_weapon, claim_room, numberCards, cardGivers):
        self.log = self.log.append({"player_makeQuery": playerName, 
                                    "claim_suspect": claim_suspect,
                                    "claim_weapon": claim_weapon, 
                                    "claim_room": claim_room,
                                    "cards_received": numberCards, 
                                    "card_giver(s)": cardGivers}, ignore_index=True)

    def player_summary(self, player_name):
        print(player_name)
        print("\n suspect must have:  ")
        self.players[player_name].display_suspect_must_have()
        print("\n weapon must have:  ")
        self.players[player_name].display_weapon_must_have()
        print("\n room must have:  ")
        self.players[player_name].display_room_must_have()


    def display_log(self):
        display(self.log)


    # def update_probability_table(df, ele_eliminated):
    #     if df == "suspect":
    #         newRow = self.df_suspect.iloc[-1,:].copy()
    #         newRow[ele_eliminated] = 0
    #     elif df == "weapon":
        
    #     elif df == "room":



    #def construct_log(self, player_Query, suspect_queried, weapon_queried, room_queried, numberOfResponce, card_givers):
        