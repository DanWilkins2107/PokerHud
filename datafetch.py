import os
from vpipcalculator import vpipCalc 
from pfrcalculator import pfrCalc
from threebetcalculator import threeBetCalc
from threebetfoldcalculator import threeBetFoldCalc
from sbraisecalculator import sbraiseCalc
from sbraisefoldcalculator import sbraisefoldCalc
from afcalculator import afCalc
from cbetflopcalculator import cbetflopCalc
from wtscalculator import wtsCalc
from wonatscalculator import wonAtSCalc

def get_data(myStats=False, testData = False):
    # Specify the path to your parent directory
    parent_directory = "../PokerData/dwilkins2107"

    # Get a list of all files in the directory
    files = os.listdir(parent_directory)
    files.sort(key=lambda x: os.path.getmtime(os.path.join(parent_directory, x)), reverse=True)

    #For each file in the directory, open it in a for loop
    test_files = [files[0]]

    data = {} 
    
    if myStats:
        files = [files[0]]
    
    if testData:
        files = test_files

    for file in files:
        # Open the file
        with open(os.path.join(parent_directory, file), "r") as f:
            # Discard all tournament files
            try:
                line1 = f.readline()
                if line1[0] == "*":
                    raise Exception("Tournament file")
            except:
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
            test_hands = hands[0:3]
            
            if testData:
                hands = test_hands
            
            for hand in hands:       
                players = (hand[5][-2])
                usernames = []
                for i in range(int(players)):
                    player_line = hand[6 + i]
                    parts = player_line.split()
                    username = parts[2]
                    usernames.append(username)
                
                # print("Starting hand ------------------")
                
                try:
                    vpip = vpipCalc(hand, usernames)
                    pfr = pfrCalc(hand, usernames)
                    threeBet = threeBetCalc(hand, usernames)
                    threeBetFold = threeBetFoldCalc(hand, usernames)
                    sbRaise = sbraiseCalc(hand, usernames)
                    sbRaiseFold = sbraisefoldCalc(hand, usernames)
                    af = afCalc(hand, usernames)
                    cbetflop = cbetflopCalc(hand, usernames)
                    wts = wtsCalc(hand, usernames)
                    wonats = wonAtSCalc(hand, usernames)
                    
                except:
                    continue
                # print("Ending hand ------------------")
                
                # Now we have all the information for the hand, add it to the data dictionary
                for username in usernames:
                    if username not in data:
                        data[username] = {
                                            "no_hands": 0,
                                            "pf_vpip": 0,
                                            "pf_pfr": 0,
                                            "pf_3bet_opp": 0,
                                            "pf_3bet": 0,
                                            "pf_3bet_recieved": 0,
                                            "pf_3bet_fold": 0,
                                            "sb_limp": 0,
                                            "sb_raise": 0,
                                            "sb_raise_opp": 0,
                                            "sb_raise_recieved": 0,
                                            "sb_raise_fold": 0,
                                            "sb_raise_call": 0,
                                            "sb_raise_raise": 0,
                                            "af_calls": 0,
                                            "af_bets/raises": 0,
                                            "cbet_flop": 0,
                                            "cbet_flop_opp": 0,
                                            "cbet_flop_recieved": 0,
                                            "cbet_flop_defend": 0,
                                            "went_to_flop": 0,
                                            "went_to_showdown": 0,
                                            "won_at_showdown": 0,
                                        }
                    if vpip[username]["vpip"]:
                        data[username]["pf_vpip"] += 1
                    if pfr[username]["pfr"]:
                        data[username]["pf_pfr"] += 1
                    if threeBet[username]["pf_3bet"]:
                        data[username]["pf_3bet"] += 1
                    if threeBet[username]["pf_3bet_opp"]:
                        data[username]["pf_3bet_opp"] += 1
                    if threeBetFold[username]["pf_3bet_fold"]:
                        data[username]["pf_3bet_fold"] += 1
                    if threeBetFold[username]["pf_3bet_recieved"]:
                        data[username]["pf_3bet_recieved"] += 1
                    if sbRaise[username]["sb_limp"]:
                        data[username]["sb_limp"] += 1
                    if sbRaise[username]["sb_raise"]:
                        data[username]["sb_raise"] += 1
                    if sbRaise[username]["sb_raise_opp"]:
                        data[username]["sb_raise_opp"] += 1
                    if sbRaiseFold[username]["sb_raise_recieved"]:
                        data[username]["sb_raise_recieved"] += 1
                    if sbRaiseFold[username]["sb_raise_fold"]:
                        data[username]["sb_raise_fold"] += 1
                    if sbRaiseFold[username]["sb_raise_call"]:
                        data[username]["sb_raise_call"] += 1
                    if sbRaiseFold[username]["sb_raise_raise"]:
                        data[username]["sb_raise_raise"] += 1
                    if cbetflop[username]["c_bet"]:
                        data[username]["cbet_flop"] += 1
                    if cbetflop[username]["c_bet_opp"]:
                        data[username]["cbet_flop_opp"] += 1
                    if cbetflop[username]["c_bet_recieved"]:
                        data[username]["cbet_flop_recieved"] += 1
                    if cbetflop[username]["c_bet_defend"]:
                        data[username]["cbet_flop_defend"] += 1
                    if wts[username]["went_to_flop"]:
                        data[username]["went_to_flop"] += 1
                    if wts[username]["went_to_showdown"]:
                        data[username]["went_to_showdown"] += 1
                    if wonats[username]["won_at_showdown"]:
                        data[username]["won_at_showdown"] += 1
                    data[username]["af_calls"] += af[username]["calls"]
                    data[username]["af_bets/raises"] += af[username]["bets/raises"]
                    data[username]["no_hands"] += 1
    return data

data = get_data(testData=True)
# print(data)
