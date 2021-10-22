from logging import raiseExceptions

import numpy as np
import random
import threading


from Advisor_Algo_I import Advisor_Algo_I
from Player import Player
from Player import Secret

import sys

sys.path.append("../utils/")
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card, SECRET_HOLDING, CHANCE_GET_MAGNIFIER, CHANCE_MAKE_CLAIM


class Simulator:
    
    def __init__(self, numberOfPlayers, maxRoundAllowed = 50):
        ## create the ground truth info of the game

        self.number_of_players = numberOfPlayers
        self.agent_hashmap = {"Player_" + str(x): None for x in range(numberOfPlayers)}
        self.solutions = {}
        self.shuffle_distribute_cards()
        self.winner = None
        self.turncount = 0
        self.whose_turn = None
        print(self.solutions)
        
        # main turn cycle
        while self.winner == None and self.turncount < maxRoundAllowed:
            self.turncount += 1
            print(f"Round {self.turncount}")
            self.whose_turn = self.get_whose_turn_helper()
            ## have a chance to make a magnifier
            if np.random.binomial(1, CHANCE_GET_MAGNIFIER, 1)[0]: ## need a further edit here
                who_to_check = self.agent_hashmap[self.whose_turn].magnifier_recom()
                list_of_card_might_get = self.agent_hashmap[who_to_check].suspects + self.agent_hashmap[who_to_check].weapons + self.agent_hashmap[who_to_check].rooms
                card_get = random.choice(list_of_card_might_get)
                self.agent_hashmap[self.whose_turn].everything_magnifier(who_to_check, card_get)

                print(f"{self.whose_turn} magnifier check {who_to_check}, and get {card_get}.")
                if self.agent_hashmap[self.whose_turn].alertWin():
                    print(f"{self.whose_turn} wins")
                    self.agent_hashmap[self.whose_turn].players["secret"].display_player_summary("secret")
                    return
            # have a chance to make a claim
            if np.random.binomial(1, CHANCE_MAKE_CLAIM, 1)[0]:
                ## from the claim maker's perspective, 
                claim = self.agent_hashmap[self.whose_turn].turn_recommendation()
                myQuery_suspect, myQuery_weapon, myQuery_room = claim.split(",")[0].strip(), claim.split(",")[1].strip(), claim.split(",")[2].strip()

                # hard part here
                suspect_giver_include_self_secret, weapon_giver_include_self_secret, room_giver_include_self_secret = self.get_card_givers_helper(myQuery_suspect, myQuery_weapon, myQuery_room)
                suspect_giver_I_enter, weapon_giver_I_enter, room_giver_I_enter = self.giver_convertor_to_me(self.whose_turn ,suspect_giver_include_self_secret, weapon_giver_include_self_secret, room_giver_include_self_secret)

                self.agent_hashmap[self.whose_turn].everything_myturn(suspect_giver_I_enter, weapon_giver_I_enter, room_giver_I_enter, myQuery_suspect, myQuery_weapon, myQuery_room)

                
                print(f"{self.whose_turn} makes a claim {myQuery_suspect}, {myQuery_weapon}, {myQuery_room}, and get {suspect_giver_I_enter}, {weapon_giver_I_enter}, {room_giver_I_enter}")

                if self.agent_hashmap[self.whose_turn].alertWin():
                    print(f"{self.whose_turn} wins")
                    self.agent_hashmap[self.whose_turn].players["secret"].display_player_summary("secret")
                    return
                ## from other players' perspective

                    ## common data to input for opponents
                oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room = myQuery_suspect, myQuery_weapon, myQuery_room

                # for i in range(self.number_of_players):
                #     whose_perspective = "Player_" + str(i)
                #     if whose_perspective == self.whose_turn:
                #         continue
                #     cardGivers_list = self.giver_convertor_to_others(suspect_giver_I_enter, weapon_giver_I_enter, room_giver_I_enter, whose_perspective)
                    
                #     print(f"from {whose_perspective}'s perspective, {self.whose_turn} claims {oppoQuery_suspect}, {oppoQuery_weapon}, {oppoQuery_room}, and get {cardGivers_list}")

                #     self.agent_hashmap[whose_perspective].update_oppoTurn(self.whose_turn, cardGivers_list, oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room)
                #     self.agent_hashmap[whose_perspective].AI_unit_otherTurn_update()
                #     self.agent_hashmap[whose_perspective].secret_Infer_Rebalance()
                #     self.agent_hashmap[whose_perspective].otherAgent_Rebalance()
                #     self.agent_hashmap[whose_perspective].add_recent_row_to_all_player("otherTurn")
                    
                #     if self.agent_hashmap[whose_perspective].alertWin():
                #         print(f"{self.whose_turn} wins")
                #         self.agent_hashmap[whose_perspective].players["secret"].display_player_summary("secret")
                #         return 
                
                #print(f"from {whose_perspective}'s perspective, {self.whose_turn} claims {oppoQuery_suspect}, {oppoQuery_weapon}, {oppoQuery_room}, and get {cardGivers_list_multi[i]}")

                cardGivers_list_multi = {}
                for i in range(self.number_of_players):
                    whose_perspective = "Player_" + str(i)
                    if whose_perspective == self.whose_turn:
                        continue
                    cardGivers_list_multi[i] = self.giver_convertor_to_others(suspect_giver_I_enter, weapon_giver_I_enter, room_giver_I_enter, whose_perspective)
                    print(f"from {whose_perspective}'s perspective, {self.whose_turn} claims {oppoQuery_suspect}, {oppoQuery_weapon}, {oppoQuery_room}, and get {cardGivers_list_multi[i]}")

                threads_1 = []
                for i in range(self.number_of_players):
                    whose_perspective = "Player_" + str(i)
                    if whose_perspective == self.whose_turn:
                        continue
                    t1 = threading.Thread(target=self.agent_hashmap[whose_perspective].everything_otherTurn, args=[self.whose_turn, cardGivers_list_multi[i], oppoQuery_suspect, oppoQuery_weapon, oppoQuery_room])
                    t1.start()
                    threads_1.append(t1)
                for thread in threads_1:
                    thread.join() 
                
                for i in range(self.number_of_players):
                    whose_perspective = "Player_" + str(i)
                    if self.agent_hashmap[whose_perspective].alertWin():
                        print(f"{self.whose_turn} wins")
                        self.agent_hashmap[whose_perspective].players["secret"].display_player_summary("secret")
                        return 

            print("\n")

            ## if winalert is True, claim win, break

            

    ## A helper method to get secret and players cards
    def shuffle_distribute_cards(self):
        deck_of_card = LIST_SUSPECT + LIST_WEAPON + LIST_ROOM
        #card_availability = {x: True for x in range(Total_Number_of_Card)}
        
        secret_suspect_index = random.randint(0, len(LIST_SUSPECT) - 1)
        secret_weapon_index = random.randint(len(LIST_SUSPECT), len(LIST_SUSPECT) + len(LIST_WEAPON) - 1)
        secret_room_index = random.randint(len(LIST_SUSPECT) + len(LIST_WEAPON), Total_Number_of_Card - 1)

        confidential_room = deck_of_card.pop(secret_room_index)
        confidential_weapon = deck_of_card.pop(secret_weapon_index)
        confidential_suspect = deck_of_card.pop(secret_suspect_index)
        self.secrets = [confidential_suspect, confidential_weapon, confidential_room]
        self.solutions[confidential_suspect], self.solutions[confidential_weapon], self.solutions[confidential_room] = "secret", "secret", "secret"

        cardEachUser_base = (Total_Number_of_Card - SECRET_HOLDING) // self.number_of_players  ## 27 // 5 = 5 
        remainders = (Total_Number_of_Card - SECRET_HOLDING) % self.number_of_players  ## 27 % 5 = 2
        actual_card_each_player = [cardEachUser_base if i >= remainders else cardEachUser_base + 1 for i in range(self.number_of_players)]
        
        # distribute the rest of the cards into numberOfPlayers piles.
        for i in range(self.number_of_players):
            cards_player_draw = self.get_hand_of_card(actual_card_each_player[i], deck_of_card, i)
            opponent_list_hashmap = self.create_opponent_profile(i, actual_card_each_player)
            ## create the virtual Agent object
            self.agent_hashmap["Player_" + str(i)] = Advisor_Algo_I("Player_" + str(i), opponent_list_hashmap, cards_player_draw, self.number_of_players)
            

    def get_hand_of_card(self, cardNum, cardAvailable, playerIdx):
        result = []
        while cardNum > 0:
            card_drawed = cardAvailable.pop(random.randint(0, len(cardAvailable) -1))
            result.append(card_drawed)
            cardNum -= 1
            ## update solutions
            self.solutions[card_drawed] = "Player_"+str(playerIdx)
        return result

    def create_opponent_profile(self, playerIdx, actual_card_each_player):
        result = {}
        for j in range(self.number_of_players):
            if j == playerIdx:
                continue
            result["Player_" + str(j)] = actual_card_each_player[j]
        return result


    def get_whose_turn_helper(self):
        if self.turncount == 1:
            ## get whose turn on the first turn, start with the smallest player_idx with least cards in hand, otherwise start with Player_0, number of players >= 3
            idx = 0
            min_num_cards_inHand = self.agent_hashmap["Player_0"].numcardsIhave
            for i in range(self.number_of_players):
                if self.agent_hashmap["Player_" + str(i)].numcardsIhave < min_num_cards_inHand:
                    idx = i
                    break
            return "Player_" + str(idx)
        else:
            curIdx = int(self.whose_turn.split("_")[1])
            nextIdx = 0 if curIdx == self.number_of_players - 1 else curIdx + 1
            return "Player_" + str(nextIdx)


    def get_card_givers_helper(self, myQuery_suspect, myQuery_weapon, myQuery_room):
        ## return the player who holds myQuery_suspect, myQuery_weapon, myQuery_room, including myself and secret. 
        return self.solutions[myQuery_suspect], self.solutions[myQuery_weapon], self.solutions[myQuery_room]

    def giver_convertor_to_me(self, whose_turn ,suspect_giver_include_self_secret, weapon_giver_include_self_secret, room_giver_include_self_secret):
        ## translate suspect
        if suspect_giver_include_self_secret == "secret":
            suspect_slot = "None"
        elif suspect_giver_include_self_secret == whose_turn:
            suspect_slot = "myself"
        else:
            suspect_slot = suspect_giver_include_self_secret
        ## translate weapon
        if weapon_giver_include_self_secret == "secret":
            weapon_slot = "None"
        elif weapon_giver_include_self_secret == whose_turn:
            weapon_slot = "myself"
        else:
            weapon_slot = weapon_giver_include_self_secret
        ## translate room
        if room_giver_include_self_secret == "secret":
            room_slot = "None"
        elif room_giver_include_self_secret == whose_turn:
            room_slot = "myself"
        else:
            room_slot = room_giver_include_self_secret

        ## if a player appears in more than one slots, only remains one slot, and change the rest to None, and which one to remain is random ## TODO: may be updaetd by more sophisticated strategy
        if suspect_slot == weapon_slot and suspect_slot == room_slot and suspect_slot != "None" and suspect_slot != "myself":
            list_to_shuffle = ["None", "None", suspect_slot]
            random.shuffle(list_to_shuffle)
            return list_to_shuffle[0], list_to_shuffle[1], list_to_shuffle[2]
        elif suspect_slot == weapon_slot and suspect_slot != "None" and suspect_slot != "myself":
            list_to_shuffle = ["None", suspect_slot]
            random.shuffle(list_to_shuffle)
            return list_to_shuffle[0], list_to_shuffle[1], room_slot
        elif suspect_slot == room_slot and suspect_slot != "None" and suspect_slot != "myself":
            list_to_shuffle = ["None", suspect_slot]
            random.shuffle(list_to_shuffle)
            return list_to_shuffle[0], weapon_slot, list_to_shuffle[1]
        elif weapon_slot == room_slot and weapon_slot != "None" and weapon_slot != "myself":
            list_to_shuffle = ["None", weapon_slot]
            random.shuffle(list_to_shuffle)
            return suspect_slot, list_to_shuffle[0], list_to_shuffle[1]
        else: ## no need to give one out many cards in hand for anyone
            return suspect_slot, weapon_slot, room_slot
    

        
    def giver_convertor_to_others(self, suspect_giver_I_enter, weapon_giver_I_enter, room_giver_I_enter, whose_perspective):
        result = []
        if suspect_giver_I_enter == "myself":
            result.append(self.whose_turn)
        elif suspect_giver_I_enter == whose_perspective:
            result.append("myself")
        elif suspect_giver_I_enter == "None":
            pass
        else:
            result.append(suspect_giver_I_enter)

        if weapon_giver_I_enter == "myself":
            result.append(self.whose_turn)
        elif weapon_giver_I_enter == whose_perspective:
            result.append("myself")
        elif weapon_giver_I_enter == "None":
            pass
        else:
            result.append(weapon_giver_I_enter)

        if room_giver_I_enter == "myself":
            result.append(self.whose_turn)
        elif room_giver_I_enter == whose_perspective:
            result.append("myself")
        elif room_giver_I_enter == "None":
            pass
        else:
            result.append(room_giver_I_enter)

        return result


        



