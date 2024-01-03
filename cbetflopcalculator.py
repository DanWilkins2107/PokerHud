def cbetflopCalc(hand, usernames):
    output = {}
    for user in usernames:
        output[user] = {
            "c_bet_opp": False,
            "c_bet": False,
            "c_bet_recieved": False,   
            "c_bet_defend": False,
        }
        
    reached_flop = False
    c_bet = False
    preflop_aggressor = None
    donk_bet = False
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
            if action == "raises":
                preflop_aggressor = current_user
            current_line += 1
        
        assert(hand[current_line].startswith("** Dealing flop **"))
        current_line += 1
        
        while hand[current_line] != "" and hand[current_line][0] != "*":
            parts = hand[current_line].split()
            current_user = parts[0]
            action = parts[1]
            if c_bet and not output[current_user]["c_bet_recieved"] :
                output[current_user]["c_bet_recieved"] = True
                if action == "calls" or action == "raises":
                    output[current_user]["c_bet_defend"] = True
            if preflop_aggressor == current_user and not donk_bet:
                output[current_user]["c_bet_opp"] = True
            if action == "bets":
                if preflop_aggressor == current_user and not donk_bet:
                    c_bet = True
                    output[current_user]["c_bet"] = True
                else :
                    donk_bet = True
            current_line += 1
    return output
            
        