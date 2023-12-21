import os

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
        # Read the file and print the first line
        line1 = f.readline()
        
        # Discard all tournament files
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
                # If the action is a raise add to pf_vpip and pf_pfr
                elif action == "raises":
                    users[username]["pf_vpip"] = True
                    users[username]["pf_pfr"] = True
                
                current_line += 1
                
            # Now we have all the information for the hand, add it to the data dictionary
            for username in users:
                if username not in data:
                    data[username] = {
                                        "no_hands": 0,
                                        "pf_vpip": 0,
                                        "pf_pfr": 0,
                                    }
                
                if users[username]["pf_vpip"]:
                    data[username]["pf_vpip"] += 1
                if users[username]["pf_pfr"]:
                    data[username]["pf_pfr"] += 1
                data[username]["no_hands"] += 1
                
# Input username to get stats

while True:
    username = input("Enter a username: ")

    if username in data:
        print(f"Stats for {username}:")
        print(f"Number of hands: {data[username]['no_hands']}")
        print(f"PF_VPIP: {int(data[username]['pf_vpip'] / data[username]['no_hands'] * 100)}")
        print(f"PF_PFR: {int(data[username]['pf_pfr'] / data[username]['no_hands'] * 100)}")
    else:
        print(f"No data available for username: {username}")

        
            
        
        
        
        
        
        

