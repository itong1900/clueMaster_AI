from logging import raiseExceptions

from numpy import empty
from Player import Player
import pandas as pd

import sys
sys.path.append("../utils/")
from agentAIUtils import search_in_must_have, myself_turn_players_update, secret_infer_helper, otherAgent_infer_helper, otherAgent_turnUpdate_3cardsCase, otherAgent_turnUpdate_OneTwo_cardsCase, otherAgent_turnUpdate_0cardsCase
from recommenderAIUtils import magnifier_recom_system, turn_recom_system
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card


class Advisor:
    
    
    def __init__(self, numberOfPlayers):
        """
        self.df_suspect : a real-time df showing probability of each suspect
        self.df_weapon  : a real-time df showing probability of each weapon
        self.df_room    : a real-time df showing probability of each room
        self.players    : a list of playerObject 
        """

        self.numberOfPlayers = numberOfPlayers
        ## get info I entered
        self.suspects, self.weapons, self.rooms, self.cardsIhave = self.collectInfo()

        ## init myself agent
        self.players = {"myself": self.initPlayers(self.suspects, self.weapons, self.rooms, self.cardsIhave)}

        # self.initProbabilityTable(self.suspects, self.weapons, self.rooms)
        
        ## init other agents
        self.initialize_secret_and_other_players(numberOfPlayers - 1)

        ## init log
        self.log = self.initialize_log()

        ## init every player's score table
        self.add_recent_row_to_all_player("init")

        ## start the game
        self.turnCycle()
        
    
    def turnCycle(self):
        while True:
            action = input("Next turn / Suggestion / Query / Magnifier / ScoreTable / Exit: ")
            if action == "Next turn":
                whose_turn = input("Whose turn is this: ")
                if whose_turn == "myself":
                    self.update_myturn()
                    self.AI_unit_myselfTurn_update()
                    self.secret_Infer_Rebalance()
                    self.otherAgent_Rebalance()
                    self.add_recent_row_to_all_player("selfTurn")
                    #break
                elif whose_turn in self.players:
                    self.update_oppoTurn(whose_turn)
                    self.AI_unit_otherTurn_update()
                    self.secret_Infer_Rebalance()
                    self.otherAgent_Rebalance()
                    self.add_recent_row_to_all_player("otherTurn")
                    #break
                else:
                    print("Wrong name, enter again: ")
                ## Alert feature, when secret is fully hacked, send notifications.
                self.alertWin()
            elif action == "Suggestion":
                self.turn_recommendation()
            elif action == "Query":
                what_query = input("Player_Summary / Log / Probability_Table:  ")
                if what_query == "Log":
                    self.display_log()
                elif what_query == "Player_Summary":
                    name = input("Player's Name: ")
                    while name not in self.players.keys():
                        print("invalid name, enter again\n")
                        name = input("Player's Name: ")
                    self.player_summary(name)
            elif action == "ScoreTable":
                self.displayScoreTable()
            elif action == "Exit":
                break
            elif action == "Magnifier":
                self.magnifier_recom()
                self.magnifierCheck()
                self.secret_Infer_Rebalance()
                self.otherAgent_Rebalance()
                self.add_recent_row_to_all_player("magnifier")
            else:
                print("Invalid input, enter again")
            print("\n")
    
    def alertWin(self):
        if len(self.players["secret"].suspect_must_have) and len(self.players["secret"].weapon_must_have) and len(self.players["secret"].room_must_have):
            print("Secret Hacked, Make Accusation Now:\n")
            self.players["secret"].display_suspect_must_have()
            self.players["secret"].display_weapon_must_have()
            self.players["secret"].display_room_must_have()
    
    def magnifier_recom(self):
        result = magnifier_recom_system(self.players)
        print("Player to check: ", result)

    def turn_recommendation(self):
        result = turn_recom_system(self.players)
        print("\nSuggested Claim: ", result, "\n")

    def update_myturn(self):
        myQuery = input("My Claim:  ")
        myQuery_suspect, myQuery_weapon, myQuery_room = myQuery.split(",")[0].strip(), myQuery.split(",")[1].strip(), myQuery.split(",")[2].strip()

        response = input("Player who provides the suspect, weapon, room, enter None if nobody, enter myself if you claim a card you own: ")
        suspect_giver, weapon_giver, room_giver = response.split(",")[0].strip(), response.split(",")[1].strip(), response.split(",")[2].strip() 
   
        listOfGiver = [suspect_giver, weapon_giver, room_giver]
        cardsCollected = 3 - listOfGiver.count("None")
        
        self.udpate_log("myself", myQuery_suspect, myQuery_weapon, myQuery_room, cardsCollected, listOfGiver)

    def update_oppoTurn(self, whose_turn):
        oppoQuery = input(whose_turn + "'s Claim:  ")
        oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room = oppoQuery.split(",")[0].strip(), oppoQuery.split(",")[1].strip(), oppoQuery.split(",")[2].strip()
        
        cardGivers = input("Player(s) who give a card(including yourself, Enter None if no ones) : ")
        cardGivers_list = [] if cardGivers == "None" else [x.strip() for x in cardGivers.split(",")]
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
        for ele in [x for x in LIST_SUSPECT if x not in suspect_list]:
            playerMyself.update_suspect_must_not_have(ele)
        for ele in [x for x in LIST_WEAPON if x not in weapon_list]:
            playerMyself.update_weapon_must_not_have(ele)
        for ele in [x for x in LIST_ROOM if x not in room_list]:
            playerMyself.update_room_must_not_have(ele)
        return playerMyself


    def initialize_secret_and_other_players(self, numberOpponents):
        secret_suspect_prob_init = 1/len([x for x in LIST_SUSPECT if x not in self.suspects])
        secret_weapon_prob_init = 1/len([x for x in LIST_WEAPON if x not in self.weapons])
        secret_room_prob_init = 1/len([x for x in LIST_ROOM if x not in self.rooms])

        ## add secret agent
        secret = Player("secret", 3)
        self.players["secret"] = secret
        for ele in self.suspects:
            self.players["secret"].update_suspect_must_not_have(ele)
        for ele in self.weapons:
            self.players["secret"].update_weapon_must_not_have(ele)
        for ele in self.rooms:
            self.players["secret"].update_room_must_not_have(ele)
        for ele in [x for x in LIST_SUSPECT if x not in self.suspects]:
            self.players["secret"].update_suspect_possibly_have(ele, secret_suspect_prob_init)
        for ele in [x for x in LIST_WEAPON if x not in self.weapons]:
            self.players["secret"].update_weapon_possibly_have(ele, secret_weapon_prob_init)
        for ele in [x for x in LIST_ROOM if x not in self.rooms]:
            self.players["secret"].update_room_possibly_have(ele, secret_room_prob_init)
        self.players["secret"].set_defaultBaseValue(suspect_value=secret_suspect_prob_init, weapon_value=secret_weapon_prob_init, room_value=secret_room_prob_init)

        other_prob_init = 1/(Total_Number_of_Card - self.cardsIhave)
        for i in range(numberOpponents):
            playerInfo = input("Enter opponent's name, # of cards, seperated by comma, if no name or #ofcards given, it will be preset by the program\n")
            name, cardQuantity = playerInfo.split(",")[0].strip(), int(playerInfo.split(",")[1].strip())

            self.players[name] = Player(name, cardQuantity)
            this_prob_init = other_prob_init * self.players[name].numberOfCards

            for ele in self.suspects:
                self.players[name].update_suspect_must_not_have(ele)
            for ele in self.weapons:
                self.players[name].update_weapon_must_not_have(ele)
            for ele in self.rooms:
                self.players[name].update_room_must_not_have(ele)
            for ele in [x for x in LIST_SUSPECT if x not in self.suspects]:
                self.players[name].update_suspect_possibly_have(ele, this_prob_init)
            for ele in [x for x in LIST_WEAPON if x not in self.weapons]:
                self.players[name].update_weapon_possibly_have(ele, this_prob_init)
            for ele in [x for x in LIST_ROOM if x not in self.rooms]:
                self.players[name].update_room_possibly_have(ele, this_prob_init)

            self.players[name].set_defaultBaseValue(general_value=this_prob_init)
                
        
        
    def collectInfo(self):

        while True:
            ## collect number of cards
            txt = input("Please enter number of cards you have:  ")
            cardsIhave = int(txt)

            ## collect suspect
            print("Please enter your Suspect Cards, seperated by comma, enter None if you don't have suspect cards")
            txt = input("suspect(s): ")
            if txt == "None":
                suspects = []
            else:
                suspects = [x.strip() for x in txt.split(",")]
            
            ## collect weapons
            print("Please enter your Weapon Cards, seperated by comma, enter None if you don't have weapon cards")       
            txt = input("weapon(s): ")
            if txt == "None":
                weapons = []
            else:
                weapons = [x.strip() for x in txt.split(",")]

            ## collect rooms
            print("Please enter your Room Cards, seperated by comma, enter None if you don't have room cards")       
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


    # def initProbabilityTable(self, suspects, weapons, rooms):
    #     self.df_suspect = pd.DataFrame(index = range(1), columns = LIST_SUSPECT)
    #     probab = 1/(len(LIST_SUSPECT) - len(suspects))
    #     for col in self.df_suspect.columns:
    #         if col in suspects:
    #             self.df_suspect[col][0] = 0
    #         else:
    #             self.df_suspect[col][0] = probab
        
    #     self.df_weapon = pd.DataFrame(index = range(1), columns = LIST_WEAPON)
    #     probab = 1/(len(LIST_WEAPON) - len(weapons))
    #     for col in self.df_weapon.columns:
    #         if col in weapons:
    #             self.df_weapon[col][0] = 0
    #         else:
    #             self.df_weapon[col][0] = probab
        
    #     self.df_room = pd.DataFrame(index = range(1), columns = LIST_ROOM)
    #     probab = 1/(len(LIST_ROOM) - len(rooms))
    #     for col in self.df_room.columns:
    #         if col in rooms:
    #             self.df_room[col][0] = 0
    #         else:
    #             self.df_room[col][0] = probab

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
        
        if player_name != "secret":
            print("\n Base Value: ", self.players[player_name].base_value_general)
        else:
            print("\n Suspect Base Value: ", self.players[player_name].base_value_secret_suspect)
            print("\n Weapon Base Value: ", self.players[player_name].base_value_secret_weapon)
            print("\n Room Base Value: ", self.players[player_name].base_value_secret_room)
        
        print("\n ** suspect must have **:  ")
        self.players[player_name].display_suspect_must_have()
        print("\n suspect probably have:  ")
        self.players[player_name].display_suspect_possibly_have()
        print("\n suspect must not have:  ")
        self.players[player_name].display_suspect_must_not_have()

        print("\n ** weapon must have **:  ")
        self.players[player_name].display_weapon_must_have()
        print("\n weapon probably have:  ")
        self.players[player_name].display_weapon_possibly_have()
        print("\n weapon must not have:  ")
        self.players[player_name].display_weapon_must_not_have()
        
        print("\n ** room must have **:  ")
        self.players[player_name].display_room_must_have()
        print("\n room probably have:  ")
        self.players[player_name].display_room_possibly_have()
        print("\n room must not have:  ")
        self.players[player_name].display_room_must_not_have()



    def display_log(self):
        print(self.log)

    def AI_unit_myselfTurn_update(self):
        # Retrieve info from log
        player_makeQuery = self.log.iloc[-1,:]["player_makeQuery"]
        claim_suspect = self.log.iloc[-1,:]["claim_suspect"]
        claim_weapon = self.log.iloc[-1,:]["claim_weapon"]
        claim_room = self.log.iloc[-1,:]["claim_room"]
        cards_received = self.log.iloc[-1,:]["cards_received"]
        card_givers = self.log.iloc[-1,:]["card_giver(s)"]

        if player_makeQuery == "myself":
            ## deal with suspect
            not_in_must_have = search_in_must_have(self.players, claim_suspect, LIST_SUSPECT, LIST_WEAPON, LIST_ROOM) == "None"
            myself_turn_players_update("suspect", not_in_must_have, card_givers[0], card_givers, self.players, claim_suspect, cards_received)
            

            ## deal with weapon
            not_in_must_have = search_in_must_have(self.players, claim_weapon, LIST_SUSPECT, LIST_WEAPON, LIST_ROOM) == "None"
            myself_turn_players_update("weapon", not_in_must_have, card_givers[1], card_givers, self.players, claim_weapon, cards_received)

            ## deal with room
            not_in_must_have = search_in_must_have(self.players, claim_room, LIST_SUSPECT, LIST_WEAPON, LIST_ROOM) == "None"
            myself_turn_players_update("room", not_in_must_have, card_givers[2], card_givers, self.players, claim_room, cards_received)


    def AI_unit_otherTurn_update(self):
        # Retrieve info from log
        player_makeQuery = self.log.iloc[-1,:]["player_makeQuery"]
        claim_suspect = self.log.iloc[-1,:]["claim_suspect"]
        claim_weapon = self.log.iloc[-1,:]["claim_weapon"]
        claim_room = self.log.iloc[-1,:]["claim_room"]
        cards_received = self.log.iloc[-1,:]["cards_received"]
        card_givers = self.log.iloc[-1,:]["card_giver(s)"]

        if cards_received == 3:
            otherAgent_turnUpdate_3cardsCase(player_makeQuery, claim_suspect, claim_weapon, claim_room, card_givers, self.players)
        elif cards_received == 2:
            otherAgent_turnUpdate_OneTwo_cardsCase(player_makeQuery, claim_suspect, claim_weapon, claim_room, card_givers, self.players, "two")
        elif cards_received == 1:
            otherAgent_turnUpdate_OneTwo_cardsCase(player_makeQuery, claim_suspect, claim_weapon, claim_room, card_givers, self.players, "one")
        elif cards_received == 0:
            otherAgent_turnUpdate_0cardsCase(player_makeQuery, claim_suspect, claim_weapon, claim_room, self.players)



    def secret_Infer_Rebalance(self):
        """
        This method make straight forward inferences after each round and rebalance the score of secret agent after each round.
        """
        secret_infer_helper("suspect", LIST_SUSPECT, self.players, self.numberOfPlayers)
        secret_infer_helper("weapon", LIST_WEAPON, self.players, self.numberOfPlayers)
        secret_infer_helper("room", LIST_ROOM, self.players, self.numberOfPlayers)

        ## Rebalance here
        base_value_suspect_secret = self.players["secret"].getSecretBaseValue_suspect()
        for ele in self.players["secret"].suspect_possibly_have.keys():
            self.players["secret"].suspect_possibly_have[ele] = max(self.players["secret"].suspect_possibly_have[ele], base_value_suspect_secret)

        base_value_weapon_secret = self.players["secret"].getSecretBaseValue_weapon()
        for ele in self.players["secret"].weapon_possibly_have.keys():
            self.players["secret"].weapon_possibly_have[ele] = max(self.players["secret"].weapon_possibly_have[ele], base_value_weapon_secret)

        base_value_room_secret = self.players["secret"].getSecretBaseValue_room()
        for ele in self.players["secret"].room_possibly_have.keys():
            self.players["secret"].room_possibly_have[ele] = max(self.players["secret"].room_possibly_have[ele], base_value_room_secret)

        self.players["secret"].set_defaultBaseValue(suspect_value=base_value_suspect_secret,weapon_value=base_value_weapon_secret,room_value=base_value_room_secret)

       
    def otherAgent_Rebalance(self):
        exemptPlayers = {"myself", "secret"}
        for otherAgent in [x for x in self.players.keys() if x not in exemptPlayers]:
            ## Reverse Impact 
            otherAgent_infer_helper("suspect", self.players, otherAgent, self.numberOfPlayers)
            otherAgent_infer_helper("weapon", self.players, otherAgent, self.numberOfPlayers)
            otherAgent_infer_helper("room", self.players, otherAgent, self.numberOfPlayers)

            base_value = self.players[otherAgent].getBaseValue()
            prev_base_value = self.players[otherAgent].base_value_general
            if base_value == 0:
                continue
            ## deal with suspect
            for ele in self.players[otherAgent].suspect_possibly_have.keys():
                if base_value >= prev_base_value:
                    self.players[otherAgent].suspect_possibly_have[ele] = max(self.players[otherAgent].suspect_possibly_have[ele], base_value)
                else:  ## base_value < prev_base_value
                    if self.players[otherAgent].suspect_possibly_have[ele] <= prev_base_value:
                        self.players[otherAgent].suspect_possibly_have[ele] = base_value
                    else:
                        pass
            ## deal with weapon
            for ele in self.players[otherAgent].weapon_possibly_have.keys():
                if base_value >= prev_base_value:
                    self.players[otherAgent].weapon_possibly_have[ele] = max(self.players[otherAgent].weapon_possibly_have[ele], base_value)
                else:  ## base_value < prev_base_value
                    if self.players[otherAgent].weapon_possibly_have[ele] <= prev_base_value:
                        self.players[otherAgent].weapon_possibly_have[ele] = base_value
                    else:
                        pass
            ## deal with room
            for ele in self.players[otherAgent].room_possibly_have.keys():
                if base_value >= prev_base_value:
                    self.players[otherAgent].room_possibly_have[ele] = max(self.players[otherAgent].room_possibly_have[ele], base_value)
                else:  ## base_value < prev_base_value
                    if self.players[otherAgent].room_possibly_have[ele] <= prev_base_value:
                        self.players[otherAgent].room_possibly_have[ele] = base_value
                    else:
                        pass

            self.players[otherAgent].set_defaultBaseValue(general_value=base_value)
            

    def magnifierCheck(self):
        """
        magnifer check by other players doesn't bring extra straightforward info here, we'll skip those cases
        """
        magnifierResult = input("Enter player you check and the card you get, separated by ,\n")
        playerName, cardGot = magnifierResult.split(",")[0].strip(), magnifierResult.split(",")[1].strip() 
        ## determine what card is this
        if cardGot in LIST_SUSPECT:
            if cardGot in self.players[playerName].suspect_possibly_have.keys():
                self.players[playerName].update_suspect_must_have(cardGot)
                del self.players[playerName].suspect_possibly_have[cardGot]
                ## put the cardGot in must-not-have in other agent, and remove from their possibly have as well
                for other_agent in [x for x in self.players.keys() if x != playerName]:
                    if cardGot in self.players[other_agent].suspect_possibly_have.keys():
                        self.players[other_agent].update_suspect_must_not_have(cardGot)
                        del self.players[other_agent].suspect_possibly_have[cardGot]
            elif cardGot in self.players[playerName].suspect_must_not_have:
                raiseExceptions("impossible to catch a card in must-not-have class, set up wrong, or someone forgets to give a card")
        elif cardGot in LIST_WEAPON:
            if cardGot in self.players[playerName].weapon_possibly_have.keys():
                self.players[playerName].update_weapon_must_have(cardGot)
                del self.players[playerName].weapon_possibly_have[cardGot]
                ## put the cardGot in must-not-have in other agent, and remove from their possibly have as well
                for other_agent in [x for x in self.players.keys() if x != playerName]:
                    if cardGot in self.players[other_agent].weapon_possibly_have.keys():
                        self.players[other_agent].update_weapon_must_not_have(cardGot)
                        del self.players[other_agent].weapon_possibly_have[cardGot]
            elif cardGot in self.players[playerName].weapon_must_not_have:
                raiseExceptions("impossible to catch a card in must-not-have class, set up wrong, or someone forgets to give a card")
        elif cardGot in LIST_ROOM:
            if cardGot in self.players[playerName].room_possibly_have.keys():
                self.players[playerName].update_room_must_have(cardGot)
                del self.players[playerName].room_possibly_have[cardGot]
                ## put the cardGot in must-not-have in other agent, and remove from their possibly have as well
                for other_agent in [x for x in self.players.keys() if x != playerName]:
                    if cardGot in self.players[other_agent].room_possibly_have.keys():
                        self.players[other_agent].update_room_must_not_have(cardGot)
                        del self.players[other_agent].room_possibly_have[cardGot]
            elif cardGot in self.players[playerName].room_must_not_have:
                raiseExceptions("impossible to catch a card in must-not-have class, set up wrong, or someone forgets to give a card")
        else:
            raiseExceptions("invalid card type in magnifier method")

    
    def add_recent_row_to_all_player(self, updateEvent):
        """
        updateEvent will always be among {"init", "selfTurn", "otherTurn", "magnifier"}
        """
        if updateEvent not in {"init", "selfTurn", "otherTurn", "magnifier"}:
            raiseExceptions("new row type not valid")

        for player in self.players.keys():
            self.players[player].newScore_append(updateEvent)
            
        
    def displayScoreTable(self):
        playerName = input("Whose score table to check: ")
        self.players[playerName].display_score_table()


    # def update_probability_table(df, ele_eliminated):
    #     if df == "suspect":
    #         newRow = self.df_suspect.iloc[-1,:].copy()
    #         newRow[ele_eliminated] = 0
    #     elif df == "weapon":
        
    #     elif df == "room":

# if __name__ == '__main__':
#     Advisor.__init__(4)