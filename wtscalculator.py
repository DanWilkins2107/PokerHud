def wtsCalc(hand, usernames):
    output = {}
    for user in usernames:
        output[user] = {
            "went_to_showdown": True,
            "went_to_flop": True,
        }
    
    total_players = usernames.copy()
    reached_flop = False
    for line in hand:
        if line.startswith("** Dealing flop **"):
            reached_flop = True
            
    if reached_flop:
        try:
            dealing_cards_index = hand.index("** Dealing down cards **\n")
        except:
            raise Exception("No preflop data")
        preflop_start_index = dealing_cards_index + 3 if hand[dealing_cards_index + 1] == "Dealt" else dealing_cards_index + 2
        assert hand[preflop_start_index - 1][0:5] == "Dealt" or hand[preflop_start_index - 1][0:2] == "**"
        current_line = preflop_start_index

        while hand[current_line] != "" and hand[current_line][0] != "*":
            parts = hand[current_line].split()
            current_user = parts[0]
            action = parts[1]
            if action == "folds":
                output[current_user]["went_to_flop"] = False
                output[current_user]["went_to_showdown"] = False
                total_players.remove(current_user)
            current_line += 1
        
        assert(hand[current_line].startswith("** Dealing flop **"))
        current_line += 1
        
        while hand[current_line] != ("** Summary **\n"):
            parts = hand[current_line].split()
            current_user = parts[0]
            action = parts[1]
            if action == "folds":
                output[current_user]["went_to_showdown"] = False
                total_players.remove(current_user)
            current_line += 1

        
        assert(hand[current_line].startswith("** Summary **"))
        if len(total_players) == 1:
            for user in usernames:
                output[user]["went_to_showdown"] = False   
    else:
        for user in usernames:
            output[user]["went_to_flop"] = False
            output[user]["went_to_showdown"] = False
    
    return output
        
    
        