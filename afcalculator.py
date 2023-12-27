def afCalc(hand, usernames):
    output = {}
    for user in usernames:
        output[user] = {
            "calls": 0,
            "bets/raises": 0,
        }
    
    reached_flop = False
    for line in hand:
        if line.startswith("** Dealing flop **"):
            reached_flop = True
        if reached_flop:
            player = line.split()[0]
            action = line.split()[1]
            if action == "calls":
                output[player]["calls"] += 1
            elif action == "bets" or action == "raises":
                output[player]["bets/raises"] += 1
    print(str(reached_flop))
    print(output)
        
            