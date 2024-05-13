def wonAtSCalc(hand, usernames):
    output = {}
    for user in usernames:
        output[user] = {
            "won_at_showdown": False,
        }
        
    try:
        dealing_cards_index = hand.index("** Dealing down cards **\n")
    except:
        raise Exception("No preflop data")
    preflop_start_index = dealing_cards_index + 3 if hand[dealing_cards_index + 1] == "Dealt" else dealing_cards_index + 2
    assert hand[preflop_start_index - 1][0:5] == "Dealt" or hand[preflop_start_index - 1][0:2] == "**"
    current_line = preflop_start_index
    
    current_players = usernames.copy()
    while hand[current_line] != ("** Summary **\n"):
        parts = hand[current_line].split()
        current_user = parts[0]
        action = parts[1]
        if action == "folds":
            current_players.remove(current_user)
        current_line += 1
        
    assert(hand[current_line].startswith("** Summary **"))
    if len(current_players) != 1:
        for user in current_players:
            output[user]["went_to_showdown"] = True
    
        #Check from current line to end who collected
        for line in hand[current_line + 1:]:
            parts = line.split()
            if len(parts) > 1:
                if parts[1] == "collected":
                    output[parts[0]]["won_at_showdown"] = True
    
    return output