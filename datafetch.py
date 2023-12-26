import os

def get_data():
    # Specify the path to your parent directory
    parent_directory = "../PokerData/dwilkins2107"

    # Get a list of all files in the directory
    files = os.listdir(parent_directory)

    # Count the number of files
    num_files = len(files)

    #For each file in the directory, open it in a for loop
    test_files = [files[0]]

    data = {}

    for file in files:
        # Open the file
        with open(os.path.join(parent_directory, file), "r") as f:
            # Discard all tournament files
            line1 = f.readline()
            if line1[0] == "*":
                print("Tournament file")
            else:
                # Go back to start of file
                f.seek(0)
                hands = []
                
                # Read file line by line, adding each line to a sublist, then make a new sublist after each blank line, making sure to skip to next nonblank line
                hand = []
                for line in f:
                    if line.strip():  # line is not blank
                        hand.append(line)
                    else:  # line is blank
                        if hand:  # if hand is not empty
                            hands.append(hand)
                            hand = []  # start a new hand
                if hand:  # add the last hand if it's not empty
                    hands.append(hand)
                
                # Now looping over all hands
                test_hands = hands[0:10]
                for hand in hands:       
                    # For each hand, line 6 shows the number of players. Get that information, it looks like Total number of players : 5
                    players = (hand[5][-2])
                    
                    users = {} 
                    # Get the usernames of all players
                    for i in range(int(players)):
                        player_line = hand[6 + i]
                        parts = player_line.split()
                        username = parts[2]
                        
                        users[username] = {
                                            "no_hands": False,
                                            "pf_vpip": False,
                                            "pf_pfr": False,
                                            "pf_3bet_opp": False,
                                            "pf_3bet": False,
                                            "pf_3bet_recieved": False,
                                            "pf_3bet_fold": False,
                        }
                    
                    
                    current_line = 6 + int(players) + 4
                    
                    # Fixes bug of faulty data
                    try: 
                        if hand[current_line][0] == "*":
                            current_line += 1
                    except:
                        continue
                    
                    # Check whether first 5 letters are "Dealt"
                    if hand[current_line][0:5] == "Dealt":
                        current_line += 1
                    
                    print(hand[current_line])
                    
                    # Loop over hand until first letter is a *
                    raisers = []
                    while hand[current_line] != "" and hand[current_line][0] != "*":
                        # Split the line into parts
                        parts = hand[current_line].split()
                        username = parts[0]
                        action = parts[1]
                        
                        if len(raisers) == 1:
                            users[username]["pf_3bet_opp"] = True
                        
                        # If the action is a call add to pf_vpip
                        if action == "calls":
                            users[username]["pf_vpip"] = True
                        # If the action is a raise add to pf_vpip and pf_pfr
                        elif action == "raises":
                            users[username]["pf_vpip"] = True
                            users[username]["pf_pfr"] = True
                            raisers.append(username)
                            
                            #check here for 3bet opportunity
                            if len(raisers) == 2:
                                users[raisers[0]]["pf_3bet_recieved"] = True
                                users[raisers[1]]["pf_3bet"] = True
                        
                        # If the action is a fold, check if it is a 3bet fold
                        elif action == "folds":
                            if len(raisers) == 2 and username == raisers[0]:
                                users[raisers[0]]["pf_3bet_fold"] = True
        
                        elif action == "checks":
                            pass
                        
                        current_line += 1
                        
                    while hand[current_line] != "** Summary **\n":
                        # Split the line into parts
                        current_line += 1
                    
                    current_line += 1
                    for i in range(len(hand) - current_line):
                        line = hand[current_line + i]
                        parts = line.split()
                        username = parts[0]
                    
                    # Now we have all the information for the hand, add it to the data dictionary
                    for username in users:
                        if username not in data:
                            data[username] = {
                                                "no_hands": 0,
                                                "pf_vpip": 0,
                                                "pf_pfr": 0,
                                                "pf_3bet_opp": 0,
                                                "pf_3bet": 0,
                                                "pf_3bet_recieved": 0,
                                                "pf_3bet_fold": 0,
                                            }
                        if users[username]["pf_vpip"]:
                            data[username]["pf_vpip"] += 1
                        if users[username]["pf_pfr"]:
                            data[username]["pf_pfr"] += 1
                        if users[username]["pf_3bet_opp"]:
                            data[username]["pf_3bet_opp"] += 1
                        if users[username]["pf_3bet"]:
                            data[username]["pf_3bet"] += 1
                        if users[username]["pf_3bet_recieved"]:
                            data[username]["pf_3bet_recieved"] += 1
                        if users[username]["pf_3bet_fold"]:
                            data[username]["pf_3bet_fold"] += 1
                        data[username]["no_hands"] += 1
    return data

data = get_data()
        
        

