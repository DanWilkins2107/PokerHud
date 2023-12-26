def sbraiseCalc(hand, usernames):
    output = {}
    for user in usernames:
        output[user] = {
            "sb_limp": False,
            "sb_raise": False,
            "sb_raise_opp": False,
        }
    
    try:
        for line in hand:
            if 'posts small blind' in line:
                sb_raiser = line.split(' posts small blind')[0]
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
        sb_line = hand[current_line]
        sb_username = sb_line.split()[0]
        sb_action = sb_line.split()[1]
        assert sb_username == sb_raiser
        output[sb_username]["sb_raise_opp"] = True
        if sb_action == "raises":
            output[sb_username]["sb_raise"] = True
        if sb_action == "calls":
            output[sb_username]["sb_limp"] = True

    return output
    
    
    
            
        
        