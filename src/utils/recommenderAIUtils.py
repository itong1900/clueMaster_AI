import random

from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM, Total_Number_of_Card

def magnifier_recom_system(playerHashmap):
    player_to_check = [x for x in playerHashmap.keys() if x != "secret"]
    potential_players = set()
    most_yet_to_must_have_card = -1
    for player in player_to_check:
        this_player_card_count = playerHashmap[player].get_not_in_must_have_yet()
        if this_player_card_count < most_yet_to_must_have_card:
            pass
        elif this_player_card_count == most_yet_to_must_have_card:
            potential_players.add(player)
        else: # this_player_card_count > most_yet_to_must_have_card
            potential_players = set()
            potential_players.add(player)
            most_yet_to_must_have_card = this_player_card_count
    return random.sample(potential_players, 1)[0]


def turn_recom_system(playerHashmap):
    ## pick suspect
    if len(playerHashmap["secret"].suspect_must_have):
        suspect_rec = "null"
    else:
        ## get the ele with highest score, suspect
        ele_to_check = [x for x in playerHashmap["secret"].suspect_possibly_have.keys()]
        potential_cards = set()
        highest_score_so_far = -1
        for ele in ele_to_check:
            this_ele_score = playerHashmap["secret"].suspect_possibly_have[ele]
            if this_ele_score < highest_score_so_far:
                pass
            elif this_ele_score == highest_score_so_far:
                potential_cards.add(ele)
            else:
                potential_cards = set()
                potential_cards.add(ele)
                highest_score_so_far = this_ele_score
        suspect_rec = random.sample(potential_cards, 1)[0]

    if len(playerHashmap["secret"].weapon_must_have):
        weapon_rec = "null"
    else:
        ## get the ele with highest score, weapon
        ele_to_check = [x for x in playerHashmap["secret"].weapon_possibly_have.keys()]
        potential_cards = set()
        highest_score_so_far = -1
        for ele in ele_to_check:
            this_ele_score = playerHashmap["secret"].weapon_possibly_have[ele]
            if this_ele_score < highest_score_so_far:
                pass
            elif this_ele_score == highest_score_so_far:
                potential_cards.add(ele)
            else:
                potential_cards = set()
                potential_cards.add(ele)
                highest_score_so_far = this_ele_score
        weapon_rec = random.sample(potential_cards, 1)[0]

    if len(playerHashmap["secret"].room_must_have):
        room_rec = "null"
    else:
        ## get the ele with highest score, room
        ele_to_check = [x for x in playerHashmap["secret"].room_possibly_have.keys()]
        potential_cards = set()
        highest_score_so_far = -1
        for ele in ele_to_check:
            this_ele_score = playerHashmap["secret"].room_possibly_have[ele]
            if this_ele_score < highest_score_so_far:
                pass
            elif this_ele_score == highest_score_so_far:
                potential_cards.add(ele)
            else:
                potential_cards = set()
                potential_cards.add(ele)
                highest_score_so_far = this_ele_score
        room_rec = random.sample(potential_cards, 1)[0]
        
        
    return suspect_rec + ", " + weapon_rec + ", " + room_rec



## helper method, return highest score of ele among all players
def get_ele_highest_score_helper(playerHashmap, ele):
    if ele in LIST_SUSPECT:
        pass
    elif ele in LIST_WEAPON:
        pass
    elif ele in LIST_ROOM:
        pass