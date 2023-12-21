while hand[current_line][0] != "*":
            #     # Split into username and action
            #     action_line = hand[current_line]
            #     parts = action_line.split()
            #     username = parts[0]
            #     action = parts[1]

            #     # If the action is a fold or check, skip
            #     if action == "folds" or action == "checks":
            #         continue
                
            #     # If the action is a call, set pf_vpip to true
            #     elif action == "calls":
            #         users[username]["pf_vpip"] = True
                
            #     # If the action is a raise, set pf_vpip and pf_pfr to true
            #     elif action == "raises":
            #         users[username]["pf_vpip"] = True
            #         users[username]["pf_pfr"] = True
                
            #     current_line += 1
            #     print(hand[current_line])
                
            # # Print the current line
            # print(hand[current_line])