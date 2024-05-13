def threeBetCalc(hand, usernames):
    output = {}
    for user in usernames:
        output[user] = {
            "pf_3bet_opp": False,
            "pf_3bet": False,
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

        if len(raisers) == 1:
            output[current_user]["pf_3bet_opp"] = True
        
        if action == "raises":
            raisers.append(current_user)
            if len(raisers) == 2:
                output[current_user]["pf_3bet"] = True
                
        current_line += 1
    
    return output
    
