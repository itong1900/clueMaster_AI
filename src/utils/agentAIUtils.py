

from logging import raiseExceptions


def search_in_must_have(playersHashMap, item_checking, LIST_SUSPECT, LIST_WEAPON, LIST_ROOM):
    '''
    return who has the item or None if no one has it.
    '''
    attribute_to_search = ""
    
    if item_checking in LIST_SUSPECT:
        attribute_to_search = "suspect"
    elif item_checking in LIST_WEAPON:
        attribute_to_search = "weapon"
    elif item_checking in LIST_ROOM:
        attribute_to_search = "room"
    
    if attribute_to_search == "suspect":
        for agent in playersHashMap.keys():
            if playersHashMap[agent].search_suspect_must_have(item_checking):
                return agent
    elif attribute_to_search == "weapon":
        for agent in playersHashMap.keys():
            if playersHashMap[agent].search_weapon_must_have(item_checking):
                return agent
    elif attribute_to_search == "room":
        for agent in playersHashMap.keys():
            if playersHashMap[agent].search_room_must_have(item_checking):
                return agent
    return "None"


def myself_turn_players_update(ObjectDealing ,not_in_must_have, card_giver, card_giver_list, playersHashmap, claim_object, cards_received):

    if ObjectDealing == "suspect":
        if not_in_must_have:
            if card_giver != "None":
                playersHashmap[card_giver].update_suspect_must_have(claim_object)
                # remove the card from the possibly have of this giver
                if claim_object in playersHashmap[card_giver].suspect_possibly_have:
                    del playersHashmap[card_giver].suspect_possibly_have[claim_object]
                # add to must_not_have in other agents, remove from their probably have list, including secret agent
                for other_agent in [x for x in playersHashmap.keys() if x != card_giver]:
                    # the claim object can only within must not have or possibly have,              
                    if claim_object in playersHashmap[other_agent].suspect_possibly_have:
                        playersHashmap[other_agent].update_suspect_must_not_have(claim_object)
                        del playersHashmap[other_agent].suspect_possibly_have[claim_object]
                    elif claim_object in playersHashmap[other_agent].suspect_must_have:
                        raiseExceptions("agent should not have this card in must have")
            else:
                # secret agent and related agent share the probability having this card, only if this card not in this agent's must_not_haves
                ## be aware that, the card might already in must-have or must-not-have, in that case, don't add it to possibly, bascially do nothing
                score_adding = 1/(1+cards_received)
                playersHashmap["secret"].update_suspect_possibly_have(claim_object, score_adding)
                for related_agent in card_giver_list:
                    if related_agent == "None":
                        continue
                    playersHashmap[related_agent].update_suspect_possibly_have(claim_object, score_adding)
                # people who doesn't give a card here have 0 probability having this card, excluding the secret agent
                for non_related_agent in [x for x in playersHashmap.keys() if x not in card_giver_list]:
                    if non_related_agent == "secret":
                        continue
                    playersHashmap[non_related_agent].update_suspect_must_not_have(claim_object)
                    if claim_object in playersHashmap[non_related_agent].suspect_possibly_have:
                        del playersHashmap[non_related_agent].suspect_possibly_have[claim_object]
        else:
            # sanity check
            pass

    elif ObjectDealing == "weapon":
        if not_in_must_have:
            if card_giver != "None":
                playersHashmap[card_giver].update_weapon_must_have(claim_object)
                # remove the card from the possibly have of this giver
                if claim_object in playersHashmap[card_giver].weapon_possibly_have:
                    del playersHashmap[card_giver].weapon_possibly_have[claim_object]
                # add to must_not_have in other agents, remove from their probably have list, including secret agent
                for other_agent in [x for x in playersHashmap.keys() if x != card_giver]:
                    # add to must_not_have in other agents, remove from their probably have list, including secret agent
                    if claim_object in playersHashmap[other_agent].weapon_possibly_have:
                        playersHashmap[other_agent].update_weapon_must_not_have(claim_object)
                        del playersHashmap[other_agent].weapon_possibly_have[claim_object]
                    elif claim_object in playersHashmap[other_agent].weapon_must_have:
                        raiseExceptions("agent should not have this card in must have")
            else:
                # secret agent and related agent share the probability having this card
                score_adding = 1/(1+cards_received)
                playersHashmap["secret"].update_weapon_possibly_have(claim_object, score_adding)
                for related_agent in card_giver_list:
                    if related_agent == "None":
                        continue
                    playersHashmap[related_agent].update_weapon_possibly_have(claim_object, score_adding)
                # people who doesn't give a card here have 0 probability having this card, excluding the secret agent
                for non_related_agent in [x for x in playersHashmap.keys() if x not in card_giver_list]:
                    if non_related_agent == "secret":
                        continue
                    playersHashmap[non_related_agent].update_weapon_must_not_have(claim_object)
                    if claim_object in playersHashmap[non_related_agent].weapon_possibly_have:
                        del playersHashmap[non_related_agent].weapon_possibly_have[claim_object]
        else:
            # sanity check
            pass
    elif ObjectDealing == "room":
        if not_in_must_have:
            if card_giver != "None":
                playersHashmap[card_giver].update_room_must_have(claim_object)
                # remove the card from the possibly have of this giver
                if claim_object in playersHashmap[card_giver].room_possibly_have:
                    del playersHashmap[card_giver].room_possibly_have[claim_object]
                # add to must_not_have in other agents, remove from their probably have list, including secret agent
                for other_agent in [x for x in playersHashmap.keys() if x != card_giver]:
                    # add to must_not_have in other agents, remove from their probably have list, including secret agent
                    if claim_object in playersHashmap[other_agent].room_possibly_have:
                        playersHashmap[other_agent].update_room_must_not_have(claim_object)
                        del playersHashmap[other_agent].room_possibly_have[claim_object]
                    elif claim_object in playersHashmap[other_agent].suspect_must_have:
                        raiseExceptions("agent should not have this card in must have")
            else:
                # secret agent and related agent share the probability having this card
                score_adding = 1/(1+cards_received)
                playersHashmap["secret"].update_room_possibly_have(claim_object, score_adding)
                for related_agent in card_giver_list:
                    if related_agent == "None":
                        continue
                    playersHashmap[related_agent].update_room_possibly_have(claim_object, score_adding)
                # people who doesn't give a card here have 0 probability having this card, excluding the secret agent
                for non_related_agent in [x for x in playersHashmap.keys() if x not in card_giver_list]:
                    if non_related_agent == "secret":
                        continue
                    playersHashmap[non_related_agent].update_room_must_not_have(claim_object)
                    if claim_object in playersHashmap[non_related_agent].room_possibly_have:
                        del playersHashmap[non_related_agent].room_possibly_have[claim_object]
        else:
            # sanity check
            pass



def secret_infer_helper(ObjectDealing, LIST_XXX, playersHashmap):
    if ObjectDealing == "suspect":
        if len(playersHashmap["secret"].suspect_must_have) == 0:
            suspect_found = "None"
            for suspect_poss in LIST_XXX:
                flag = "This One"
                for player in [x for x in playersHashmap.keys() if x != "secret"]:
                    if suspect_poss in playersHashmap[player].suspect_must_not_have:
                        continue
                    else:
                        flag = "Not this One"
                        break
                if flag == "This One":
                    suspect_found = suspect_poss
                    break
                elif flag == "Not this One":
                    continue
            # if None is found, do nothing, otherwise, make inference
            if suspect_found == "None":
                pass
            else:
                ## update secret must have, delete the suspect_found from possibly set
                playersHashmap["secret"].update_suspect_must_have(suspect_found)
                del playersHashmap["secret"].suspect_possibly_have[suspect_found]
                ## clean up the rest of possibly set, and move them to must-not-have class
                for ele in playersHashmap["secret"].suspect_possibly_have.keys():
                    playersHashmap["secret"].update_suspect_must_not_have(ele)
                playersHashmap["secret"].suspect_possibly_have = {}
    elif ObjectDealing == "weapon":
        if len(playersHashmap["secret"].weapon_must_have) == 0:
            weapon_found = "None"
            for weapon_poss in LIST_XXX:
                flag = "This One"
                for player in [x for x in playersHashmap.keys() if x != "secret"]:
                    if weapon_poss in playersHashmap[player].weapon_must_not_have:
                        continue
                    else:
                        flag = "Not this One"
                        break
                if flag == "This One":
                    weapon_found = weapon_poss
                    break
                elif flag == "Not this One":
                    continue
            # if None is found, do nothing, otherwise, make inference
            if weapon_found == "None":
                pass
            else:
                ## update secret must have, delete the weapon_found from possibly set
                playersHashmap["secret"].update_weapon_must_have(weapon_found)
                del playersHashmap["secret"].weapon_possibly_have[weapon_found]
                ## clean up the rest of possibly set, and move them to must-not-have class
                for ele in playersHashmap["secret"].weapon_possibly_have.keys():
                    playersHashmap["secret"].update_weapon_must_not_have(ele)
                playersHashmap["secret"].weapon_possibly_have = {}
    elif ObjectDealing == "room":
        if len(playersHashmap["secret"].room_must_have) == 0:
            room_found = "None"
            for room_poss in LIST_XXX:
                flag = "This One"
                for player in [x for x in playersHashmap.keys() if x != "secret"]:
                    if room_poss in playersHashmap[player].room_must_not_have:
                        continue
                    else:
                        flag = "Not this One"
                        break
                if flag == "This One":
                    room_found = room_poss
                    break
                elif flag == "Not this One":
                    continue
            # if None is found, do nothing, otherwise, make inference
            if room_found == "None":
                pass
            else:
                ## update secret must have, delete the room_found from possibly set
                playersHashmap["secret"].update_room_must_have(room_found)
                del playersHashmap["secret"].room_possibly_have[room_found]
                ## clean up the rest of possibly set, and move them to must-not-have class
                for ele in playersHashmap["secret"].room_possibly_have.keys():
                    playersHashmap["secret"].update_room_must_not_have(ele)
                playersHashmap["secret"].room_possibly_have = {}


def otherAgent_infer_helper(ObjectDealing, playerHashmap, playerName, playerQuantity):
    if ObjectDealing == "suspect":
        for ele in playerHashmap[playerName].suspect_possibly_have.keys():
            results = [playerHashmap[x].check_in_must_not_have(ele) for x in playerHashmap.keys() if x != playerName]
            ## move to must_have if this it's in all other players' must_not_have
            if sum(results) == playerQuantity:
                playerHashmap[playerName].update_suspect_must_have(ele)
                del playerHashmap[playerName].suspect_possibly_have[ele]
    elif ObjectDealing == "weapon":
        for ele in playerHashmap[playerName].weapon_possibly_have.keys():
            results = [playerHashmap[x].check_in_must_not_have(ele) for x in playerHashmap.keys() if x != playerName]
            ## move to must_have if this it's in all other players' must_not_have
            if sum(results) == playerQuantity:
                playerHashmap[playerName].update_weapon_must_have(ele)
                del playerHashmap[playerName].weapon_possibly_have[ele]
    elif ObjectDealing == "room":
        for ele in playerHashmap[playerName].room_possibly_have.keys():
            results = [playerHashmap[x].check_in_must_not_have(ele) for x in playerHashmap.keys() if x != playerName]
            ## move to must_have if this it's in all other players' must_not_have
            if sum(results) == playerQuantity:
                playerHashmap[playerName].update_room_must_have(ele)
                del playerHashmap[playerName].room_possibly_have[ele]