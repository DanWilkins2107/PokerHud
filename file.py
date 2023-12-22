import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
import tkinter as tk

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

data = get_data()
# Input username to get stats
# while True:
#     username = input("Enter a username: ")

#     if username in data:
#         print(f"Stats for {username}:")
#         print(f"Number of hands: {data[username]['no_hands']}")
#         print(f"PF_VPIP: {int(data[username]['pf_vpip'] / data[username]['no_hands'] * 100)}")
#         print(f"PF_PFR: {int(data[username]['pf_pfr'] / data[username]['no_hands'] * 100)}")
#         print(f"WtSD: {int(data[username]['wtsd'] / data[username]['hand_entry'] * 100)}")
#     else:
#         print(f"No data available for username: {username}")
        
        
# Create the main window
window = tk.Tk()

# Create a list to store the usernames and text fields
usernames = [""]
text_fields = []

# Create a function to add a new text field
def add_text_field():
    usernames.append("")
    create_text_fields(usernames)

# Create a function to delete all text fields
def delete_text_fields():
    for text_field in text_fields:
        text_field.destroy()
    text_fields.clear()

# Create a function to update the stats
def refresh():
    for username in usernames:
        print(username)  # Replace this with your code to update the stats

# Create an add button
add_button = tk.Button(window, text="Add", command=add_text_field, background="green")
add_button.pack()

# Create a refresh button
refresh_button = tk.Button(window, text="Refresh", command=refresh, background="red")
refresh_button.pack()

# Create a text field for each username
def create_text_fields(username):
    for username in usernames:
        text_field = tk.Entry(window)
        text_field.insert(0, username)  # Set the initial value to the username
        text_field.pack()
        
create_text_fields(usernames)

# Start the main loop
window.mainloop()

        
        
        
        
        

