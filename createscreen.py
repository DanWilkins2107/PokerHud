from datafetch import get_data
import tkinter as tk
import time

window = tk.Tk()
window.title("Poker HUD")

frame_width = 200
frame_height = 100

#Function to update stats
def updateStats():
    data = get_data()
    if player_1_nameVar.get() in data:
        player_1_statString_val.set("No of Hands: "+ str(data[player_1_nameVar.get()]["no_hands"]) + "\nVPIP: " + str(data[player_1_nameVar.get()]["pf_vpip"]) + "\nPFR: " + str(data[player_1_nameVar.get()]["pf_pfr"]) + "\nWtSD: " + str(data[player_1_nameVar.get()]["wtsd"]))
    else:
        player_1_statString_val.set("Player not found")
    if player_2_nameVar.get() in data:
        player_2_statString_val.set("No of Hands: "+ str(data[player_2_nameVar.get()]["no_hands"]) + "\nVPIP: " + str(data[player_2_nameVar.get()]["pf_vpip"]) + "\nPFR: " + str(data[player_2_nameVar.get()]["pf_pfr"]) + "\nWtSD: " + str(data[player_2_nameVar.get()]["wtsd"]))
    else:
        player_2_statString_val.set("Player not found")
    if player_3_nameVar.get() in data:
        player_3_statString_val.set("No of Hands: "+ str(data[player_3_nameVar.get()]["no_hands"]) + "\nVPIP: " + str(data[player_3_nameVar.get()]["pf_vpip"]) + "\nPFR: " + str(data[player_3_nameVar.get()]["pf_pfr"]) + "\nWtSD: " + str(data[player_3_nameVar.get()]["wtsd"]))
    else:
        player_3_statString_val.set("Player not found")
    if player_4_nameVar.get() in data:
        player_4_statString_val.set("No of Hands: "+ str(data[player_4_nameVar.get()]["no_hands"]) + "\nVPIP: " + str(data[player_4_nameVar.get()]["pf_vpip"]) + "\nPFR: " + str(data[player_4_nameVar.get()]["pf_pfr"]) + "\nWtSD: " + str(data[player_4_nameVar.get()]["wtsd"]))
    else:
        player_4_statString_val.set("Player not found")
    if player_5_nameVar.get() in data:
        player_5_statString_val.set("No of Hands: "+ str(data[player_5_nameVar.get()]["no_hands"]) + "\nVPIP: " + str(data[player_5_nameVar.get()]["pf_vpip"]) + "\nPFR: " + str(data[player_5_nameVar.get()]["pf_pfr"]) + "\nWtSD: " + str(data[player_5_nameVar.get()]["wtsd"]))
    else:
        player_5_statString_val.set("Player not found")

    

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

