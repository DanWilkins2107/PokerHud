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
                continue
            
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
            test_hands = [hands[0]]
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
                                        "pf_vpip": False,
                                        "pf_pfr": False, 
                                        "wtsd": False,   
                                        "hand_entry": False,                                  
                                    }
                
                
                current_line = 6 + int(players) + 4

                # Loop over hand until first letter is a *
                while hand[current_line][0] != '*':
                    # Split the line into parts
                    parts = hand[current_line].split()
                    username = parts[0]
                    action = parts[1]
                    
                    # If the action is a call add to pf_vpip
                    if action == "calls":
                        users[username]["pf_vpip"] = True
                        users[username]["hand_entry"] = True
                    # If the action is a raise add to pf_vpip and pf_pfr
                    elif action == "raises":
                        users[username]["pf_vpip"] = True
                        users[username]["pf_pfr"] = True
                        users[username]["hand_entry"] = True
                    elif action == "checks":
                        users[username]["hand_entry"] = True
                    
                    current_line += 1
                    
                while hand[current_line] != "** Summary **\n":
                    # Split the line into parts
                    current_line += 1
                
                current_line += 1
                for i in range(len(hand) - current_line):
                    line = hand[current_line + i]
                    parts = line.split()
                    username = parts[0]
                    users[username]["wtsd"] = True
                
                # Now we have all the information for the hand, add it to the data dictionary
                for username in users:
                    if username not in data:
                        data[username] = {
                                            "no_hands": 0,
                                            "pf_vpip": 0,
                                            "pf_pfr": 0,
                                            "wtsd": 0,
                                            "hand_entry": 0,
                                        }
                    
                    if users[username]["pf_vpip"]:
                        data[username]["pf_vpip"] += 1
                    if users[username]["pf_pfr"]:
                        data[username]["pf_pfr"] += 1
                    if users[username]["wtsd"]:
                        data[username]["wtsd"] += 1
                    if users[username]["hand_entry"]:
                        data[username]["hand_entry"] += 1
                    data[username]["no_hands"] += 1
    return data
        
        

