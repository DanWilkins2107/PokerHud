from datafetch import get_data
import tkinter as tk

window = tk.Tk()
window.title("Poker HUD")

frame_width = 200
frame_height = 150

def createString(username, data):
    if username in data:
        no_handsString = "No. Hands: " + str(data[username]["no_hands"])
        vpipString = "\nVPIP: " + str(round(data[username]["pf_vpip"] * 100 /data[username]["no_hands"])) + "%"
        pfrString = "\nPFR: " + str(round(data[username]["pf_pfr"] * 100 /data[username]["no_hands"])) + "%"
        threeBetString = "\n3Bet: " + str(data[username]["pf_3bet"]) + "/" + str(data[username]["pf_3bet_opp"])
        threeBetFoldString = "\n3Bet Fold: " + str(data[username]["pf_3bet_fold"]) + "/" + str(data[username]["pf_3bet_recieved"])
        sbRaiseString = "\n SB(R, L): " + "(" + str(data[username]["sb_raise"]) + ", " + str(data[username]["sb_limp"]) + ")" + "/" + str(data[username]["sb_raise_opp"])
        return no_handsString + vpipString + pfrString + threeBetString + threeBetFoldString + sbRaiseString
    else:
        return "Player not found"

#Function to update stats
def updateStats():
    data = get_data()
    player_1_statString_val.set(createString(player_1_nameVar.get(), data))
    player_2_statString_val.set(createString(player_2_nameVar.get(), data))
    player_3_statString_val.set(createString(player_3_nameVar.get(), data))
    player_4_statString_val.set(createString(player_4_nameVar.get(), data))
    player_5_statString_val.set(createString(player_5_nameVar.get(), data))

    

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
player_1_statString.pack()


player_2_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#FFAAFF")
player_2_frame.pack()
player_2_frame.pack_propagate(False)
player_2_nameVar = tk.StringVar()
player_2_field = tk.Entry(master=player_2_frame, textvariable=player_2_nameVar)
player_2_field.pack()
player_2_statString_val = tk.StringVar()
player_2_statString = tk.Label(master=player_2_frame, textvariable=player_2_statString_val)
player_2_statString.pack()

player_3_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#AAFFFF")
player_3_frame.pack()
player_3_frame.pack_propagate(False)
player_3_nameVar = tk.StringVar()
player_3_field = tk.Entry(master=player_3_frame, textvariable=player_3_nameVar)
player_3_field.pack()
player_3_statString_val = tk.StringVar()
player_3_statString = tk.Label(master=player_3_frame, textvariable=player_3_statString_val)
player_3_statString.pack()

player_4_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#AAAAFF")
player_4_frame.pack()
player_4_frame.pack_propagate(False)
player_4_nameVar = tk.StringVar()
player_4_field = tk.Entry(master=player_4_frame, textvariable=player_4_nameVar)
player_4_field.pack()
player_4_statString_val = tk.StringVar()
player_4_statString = tk.Label(master=player_4_frame, textvariable=player_4_statString_val)
player_4_statString.pack()

player_5_frame = tk.Frame(master=window, width=frame_width, height=frame_height, bg="#AAFFAA")
player_5_frame.pack()
player_5_frame.pack_propagate(False)
player_5_nameVar = tk.StringVar()
player_5_field = tk.Entry(master=player_5_frame, textvariable=player_5_nameVar)
player_5_field.pack()
player_5_statString_val = tk.StringVar()
player_5_statString = tk.Label(master=player_5_frame, textvariable=player_5_statString_val)
player_5_statString.pack()

window.mainloop()

