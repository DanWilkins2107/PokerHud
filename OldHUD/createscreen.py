from datafetch import get_data
import tkinter as tk

window = tk.Tk()
window.title("Poker HUD")

frame_width = 300
frame_height = 150

def createPreflopString(username, data):
    if username in data:
        no_handsString = "No. Hands: " + str(data[username]["no_hands"])
        vpipString = "\nVPIP: " + str(round(data[username]["pf_vpip"] * 100 /data[username]["no_hands"])) + "%"
        pfrString = "\nPFR: " + str(round(data[username]["pf_pfr"] * 100 /data[username]["no_hands"])) + "%"
        threeBetString = "\n3Bet: " + str(data[username]["pf_3bet"]) + "/" + str(data[username]["pf_3bet_opp"])
        threeBetFoldString = "\n3Bet Fold: " + str(data[username]["pf_3bet_fold"]) + "/" + str(data[username]["pf_3bet_recieved"])
        sbRaiseString = "\n SB(R, L): " + "(" + str(data[username]["sb_raise"]) + ", " + str(data[username]["sb_limp"]) + ")" + "/" + str(data[username]["sb_raise_opp"])
        bbString = "\n BB(F, C, R): " + "(" + str(data[username]["sb_raise_fold"]) + ", " + str(data[username]["sb_raise_call"]) + ", " + str(data[username]["sb_raise_raise"]) + ")" + "/" + str(data[username]["sb_raise_recieved"])
        return no_handsString + vpipString + pfrString + threeBetString + threeBetFoldString + sbRaiseString + bbString
    else:
        return "Player not found"


def createPostFlopString(username, data):
    if username in data:
        if data[username]["af_calls"] == 0:
            afString = "AF: n/a"
        else:
            afString = "AF: " + str(round(data[username]["af_bets/raises"] / data[username]["af_calls"], 2))
        cbetString = "\nFlop CBet: " + str(data[username]["cbet_flop"]) + "/" + str(data[username]["cbet_flop_opp"])
        cbetFoldString = "\nCBet Defend: " + str(data[username]["cbet_flop_defend"]) + "/" + str(data[username]["cbet_flop_recieved"])
        wtsString = "\nWTS: " + str(data[username]["went_to_showdown"]) + "/" + str(data[username]["went_to_flop"])
        wonAtSString = "\nWon at SD: " + str(data[username]["won_at_showdown"]) + "/" + str(data[username]["went_to_showdown"])
        return afString + cbetString + cbetFoldString + wtsString + wonAtSString
    else:
        return "Player not found"

#Function to update stats
def updateStats():
    data = get_data()
    myData = get_data(True)
    player_1_statString_val.set(createPreflopString(player_1_nameVar.get(), data))
    player_2_statString_val.set(createPreflopString(player_2_nameVar.get(), data))
    player_3_statString_val.set(createPreflopString(player_3_nameVar.get(), data))
    player_4_statString_val.set(createPreflopString(player_4_nameVar.get(), data))
    player_5_statString_val.set(createPreflopString(player_5_nameVar.get(), data))
    player_1_statString_2_val.set(createPostFlopString(player_1_nameVar.get(), data))
    player_2_statString_2_val.set(createPostFlopString(player_2_nameVar.get(), data))
    player_3_statString_2_val.set(createPostFlopString(player_3_nameVar.get(), data))
    player_4_statString_2_val.set(createPostFlopString(player_4_nameVar.get(), data))
    player_5_statString_2_val.set(createPostFlopString(player_5_nameVar.get(), data))
    player_me_statString_val.set(createPreflopString("dwilkins2107", myData))
    player_me_statString_2_val.set(createPostFlopString("dwilkins2107", myData))
    

    

#Button to update stats
update_button = tk.Button(text="Update Stats", command=updateStats)
update_button.pack()

#Frames
player_1_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#FFFFAA")
player_1_frame.pack()
player_1_frame.pack_propagate(False)
player_1_nameVar = tk.StringVar()
player_1_field = tk.Entry(master=player_1_frame, textvariable=player_1_nameVar)
player_1_field.pack()
player_1_statString_val = tk.StringVar()
player_1_statString = tk.Label(master=player_1_frame, textvariable=player_1_statString_val)
player_1_statString.pack(side=tk.LEFT)
player_1_statString_2_val = tk.StringVar()
player_1_statString_2 = tk.Label(master=player_1_frame, textvariable=player_1_statString_2_val)
player_1_statString_2.pack(side=tk.RIGHT)


player_2_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#FFAAFF")
player_2_frame.pack()
player_2_frame.pack_propagate(False)
player_2_nameVar = tk.StringVar()
player_2_field = tk.Entry(master=player_2_frame, textvariable=player_2_nameVar)
player_2_field.pack()
player_2_statString_val = tk.StringVar()
player_2_statString = tk.Label(master=player_2_frame, textvariable=player_2_statString_val)
player_2_statString.pack(side=tk.LEFT)
player_2_statString_2_val = tk.StringVar()
player_2_statString_2 = tk.Label(master=player_2_frame, textvariable=player_2_statString_2_val)
player_2_statString_2.pack(side=tk.RIGHT)

player_3_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#AAFFFF")
player_3_frame.pack()
player_3_frame.pack_propagate(False)
player_3_nameVar = tk.StringVar()
player_3_field = tk.Entry(master=player_3_frame, textvariable=player_3_nameVar)
player_3_field.pack()
player_3_statString_val = tk.StringVar()
player_3_statString = tk.Label(master=player_3_frame, textvariable=player_3_statString_val)
player_3_statString.pack(side=tk.LEFT)
player_3_statString_2_val = tk.StringVar()
player_3_statString_2 = tk.Label(master=player_3_frame, textvariable=player_3_statString_2_val)
player_3_statString_2.pack(side=tk.RIGHT)

player_4_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#AAAAFF")
player_4_frame.pack()
player_4_frame.pack_propagate(False)
player_4_nameVar = tk.StringVar()
player_4_field = tk.Entry(master=player_4_frame, textvariable=player_4_nameVar)
player_4_field.pack()
player_4_statString_val = tk.StringVar()
player_4_statString = tk.Label(master=player_4_frame, textvariable=player_4_statString_val)
player_4_statString.pack(side=tk.LEFT)
player_4_statString_2_val = tk.StringVar()
player_4_statString_2 = tk.Label(master=player_4_frame, textvariable=player_4_statString_2_val)
player_4_statString_2.pack(side=tk.RIGHT)

player_5_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#AAFFAA")
player_5_frame.pack()
player_5_frame.pack_propagate(False)
player_5_nameVar = tk.StringVar()
player_5_field = tk.Entry(master=player_5_frame, textvariable=player_5_nameVar)
player_5_field.pack()
player_5_statString_val = tk.StringVar()
player_5_statString = tk.Label(master=player_5_frame, textvariable=player_5_statString_val)
player_5_statString.pack(side=tk.LEFT)
player_5_statString_2_val = tk.StringVar()
player_5_statString_2 = tk.Label(master=player_5_frame, textvariable=player_5_statString_2_val)
player_5_statString_2.pack(side=tk.RIGHT)

player_me_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#FFAAAA")
player_me_frame.pack()
player_me_frame.pack_propagate(False)
player_me_statString_val = tk.StringVar()
player_me_statString = tk.Label(master=player_me_frame, textvariable=player_me_statString_val)
player_me_statString.pack(side=tk.LEFT)
player_me_statString_2_val = tk.StringVar()
player_me_statString_2 = tk.Label(master=player_me_frame, textvariable=player_me_statString_2_val)
player_me_statString_2.pack(side=tk.RIGHT)

window.mainloop()

