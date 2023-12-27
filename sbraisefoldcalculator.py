def sbraisefoldCalc(hand, usernames):
    output = {}
    for user in usernames:
        output[user] = {
            "sb_raise_recieved": False,
            "sb_raise_fold": False,
            "sb_raise_call": False,
            "sb_raise_raise": False,
        }
    
    try:
        for line in hand:
            if 'posts big blind' in line:
                bb_username = line.split(' posts big blind')[0]
    except:
        raise Exception("Faulty preflop data")
    
    try:   
        dealing_cards_index = hand.index("** Dealing down cards **\n")
    except:
        raise Exception("No preflop data")
    
    preflop_start_index = dealing_cards_index + 3 if hand[dealing_cards_index + 1] == "Dealt" else dealing_cards_index + 2
    assert hand[preflop_start_index - 1][0:5] == "Dealt" or hand[preflop_start_index - 1][0:2] == "**"
    
    current_line = preflop_start_index
    sb_raise_opp = True
    for i in range(len(usernames) - 2):
        parts = hand[current_line].split()
        action = parts[1]

        if action != "folds":
            sb_raise_opp = False
        
        current_line += 1
    

    if sb_raise_opp:
        sb_action = hand[current_line].split()[1]
        if sb_action == "raises":
            output[bb_username]["sb_raise_recieved"] = True
            current_line += 1
            bb_action = hand[current_line].split()[1]
            if bb_action == "folds":
                output[bb_username]["sb_raise_fold"] = True
            elif bb_action == "calls":
                output[bb_username]["sb_raise_call"] = True
            elif bb_action == "raises":
                output[bb_username]["sb_raise_raise"] = True

    return output
    