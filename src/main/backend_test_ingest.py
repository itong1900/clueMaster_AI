

from Advisor_Algo_I import Advisor_Algo_I
#from Advisor_Algo_II import Advisor_Algo_II

def main():
    backend_test_ingest(4)

class backend_test_ingest:
    def __init__(self, numberOfPlayers):
        self.number_of_player = numberOfPlayers
        self.algo_this_advisor = self.init_advisor_algo()

        ## start the game at the backend
        self.turnCycle()


    def turnCycle(self):
        """
        The main round structure of the advisor mode.
        """
        while True:
            action = input("Next turn / Suggestion / Query / Magnifier / ScoreExport / Exit: ")
            if action == "Next turn":
                whose_turn = input("Whose turn is this: ")
                if whose_turn == "myself":
                    myQuery = input("My Claim:  ")
                    myQuery_suspect, myQuery_weapon, myQuery_room = myQuery.split(",")[0].strip(), myQuery.split(",")[1].strip(), myQuery.split(",")[2].strip()

                    response = input("Player who provides the suspect, weapon, room, enter None if nobody, enter myself if you claim a card you own: ")
                    suspect_giver, weapon_giver, room_giver = response.split(",")[0].strip(), response.split(",")[1].strip(), response.split(",")[2].strip() 

                    self.algo_this_advisor.update_myturn(suspect_giver, weapon_giver, room_giver, myQuery_suspect, myQuery_weapon, myQuery_room)
                    self.algo_this_advisor.AI_unit_myselfTurn_update()
                    self.algo_this_advisor.secret_Infer_Rebalance()
                    self.algo_this_advisor.otherAgent_Rebalance()
                    self.algo_this_advisor.add_recent_row_to_all_player("selfTurn")
                    #break
                elif whose_turn in self.algo_this_advisor.players:
                    oppoQuery = input(whose_turn + "'s Claim:  ")
                    oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room = oppoQuery.split(",")[0].strip(), oppoQuery.split(",")[1].strip(), oppoQuery.split(",")[2].strip()
        
                    cardGivers = input("Player(s) who give a card(including yourself, Enter None if no ones) : ")
                    cardGivers_list = [] if cardGivers == "None" else [x.strip() for x in cardGivers.split(",")]

                    self.algo_this_advisor.update_oppoTurn(whose_turn, cardGivers_list, oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room)
                    self.algo_this_advisor.AI_unit_otherTurn_update()
                    self.algo_this_advisor.secret_Infer_Rebalance()
                    self.algo_this_advisor.otherAgent_Rebalance()
                    self.algo_this_advisor.add_recent_row_to_all_player("otherTurn")
                    #break
                else:
                    print("Wrong name, enter again: ")
                ## Alert feature, when secret is fully hacked, send notifications.
                if self.algo_this_advisor.alertWin():
                    self.algo_this_advisor.players["secret"].display_suspect_must_have()
                    self.algo_this_advisor.players["secret"].display_weapon_must_have()
                    self.algo_this_advisor.players["secret"].display_room_must_have()
            elif action == "Suggestion":
                self.algo_this_advisor.turn_recommendation()
            elif action == "Query":
                what_query = input("Player_Summary / Log / Probability_Table:  ")
                if what_query == "Log":
                    print(self.algo_this_advisor.log)
                elif what_query == "Player_Summary":
                    player_name = input("Player's Name: ")
                    while player_name not in self.algo_this_advisor.players.keys():
                        print("invalid name, enter again\n")
                        player_name = input("Player's Name: ")
                    self.algo_this_advisor.players[player_name].display_player_summary(player_name)
            elif action == "ScoreExport":
                #self.displayScoreTable()
                self.algo_this_advisor.exportAllTables()
            elif action == "Exit":
                break
            elif action == "Magnifier":
                self.algo_this_advisor.magnifier_recom()
                magnifierResult = input("Enter player you check and the card you get, separated by ,\n")
                playerName, cardGot = magnifierResult.split(",")[0].strip(), magnifierResult.split(",")[1].strip() 
                self.algo_this_advisor.magnifierCheck(playerName, cardGot)
                self.algo_this_advisor.secret_Infer_Rebalance()
                self.algo_this_advisor.otherAgent_Rebalance()
                self.algo_this_advisor.add_recent_row_to_all_player("magnifier")
            else:
                print("Invalid input, enter again")
            print("\n")



    def init_advisor_algo(self):
        algoName = input("Input the name of the algo for advisor: ")
        cardsIhave, num_of_cards_Ihave = self.collect_self_Info()
        otherPlayerInfo_hashmap = self.collect_other_player_info(self.number_of_player - 1)

        if algoName == "Advisor_Algo_I":
            return Advisor_Algo_I("Advisor_Type_I", otherPlayerInfo_hashmap, cardsIhave, self.number_of_player)
        #elif algoName == "":
        


    def collect_self_Info(self):
        """
        helper method to collect the info of myself at the start of the game, with some input validation
        """
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

        return suspects + weapons + rooms,  cardsIhave


    def collect_other_player_info(self, numberOpponents):
        opponent_list_hashmap = {}
        
        for i in range(numberOpponents):
            playerInfo = input("Enter opponent's name, # of cards, seperated by comma, if no name or #ofcards given, it will be preset by the program\n")
            name, cardQuantity = playerInfo.split(",")[0].strip(), int(playerInfo.split(",")[1].strip())
            opponent_list_hashmap[name] = int(cardQuantity)

        return opponent_list_hashmap

if __name__ == '__main__':
    main()