def threeBetFoldCalc(hand, usernames): 
    output = {}
    for user in usernames:
        output[user] = {
            "pf_3bet_fold": False,
            "pf_3bet_recieved": False,
        }
    try:
        dealing_cards_index = hand.index("** Dealing down cards **\n")
    except:
        raise Exception("No preflop data")
    
    preflop_start_index = dealing_cards_index + 3 if hand[dealing_cards_index + 1] == "Dealt" else dealing_cards_index + 2
    assert hand[preflop_start_index - 1][0:5] == "Dealt" or hand[preflop_start_index - 1][0:2] == "**"
    
    current_line = preflop_start_index
    raisers = []
    
    while hand[current_line] != "" and hand[current_line][0] != "*":
        parts = hand[current_line].split()
        current_user = parts[0]
        action = parts[1]
        
        if action == "raises":
            raisers.append(current_user)
            
        if len(raisers) == 2 and raisers[0] == current_user:
            output[current_user]["pf_3bet_recieved"] = True
            if action == "folds":
                output[current_user]["pf_3bet_fold"] = True
    
        current_line += 1
        
    return output
            
        
        