import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import requests
from io import BytesIO
import webbrowser
import os
import model

geometry = None

frame_for_songs = {}


def set_window_geometry():
    global geometry
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    if screen_width > 7680 and screen_height > 4320:
        window.geometry("7680x4320")
        geometry = "7680x4320"
    elif screen_width > 3840 and screen_height > 2160:
        window.geometry("3840x2160")
        geometry = "3840x2160"
    elif screen_width > 2560 and screen_height > 1440:
        window.geometry("2560x1440")
        geometry = "2560x1440"
    elif screen_width > 1920 and screen_height > 1080:
        window.geometry("1920x1080")
        geometry = "1920x1080"
    elif screen_width > 1280 and screen_height > 720:
        window.geometry("1280x720")
        geometry = "1280x720"
    elif screen_width > 720 and screen_height > 576:
        window.geometry("720x576")
        geometry = "720x576"
    elif screen_width > 720 and screen_height > 480:
        window.geometry("720x480")
        geometry = "720x480"
    else:
        window.geometry("640x480")
        geometry = "640x480"


def open_link(link):
    webbrowser.open(link)


def suggestion():
    infos = {}
    infos = model.return_infos()
    for i in range(len(infos)):
        frame_name = "frame_for_songs" + str(i + 1)
        frame_for_songs[frame_name] = tk.Frame(frame_for_suggestions, bg="#191414")
        frame_for_songs[frame_name].pack(anchor=tk.NW)

        photo_name = "photo" + str(i + 1)
        globals()[photo_name] = Image.open(icon_path)
        globals()[photo_name] = globals()[photo_name].resize((100, 100))
        globals()[photo_name] = ImageTk.PhotoImage(globals()[photo_name])

        photo_label_name = "photo_label" + str(i + 1)
        globals()[photo_label_name] = tk.Label(frame_for_songs[frame_name], image=globals()[photo_name], bg="#191414")
        globals()[photo_label_name].pack(side=tk.LEFT, anchor=tk.W)

        response = requests.get(infos[i]["image"])
        globals()[photo_name] = Image.open(BytesIO(response.content))
        globals()[photo_name] = globals()[photo_name].resize((100, 100))
        globals()[photo_name] = ImageTk.PhotoImage(globals()[photo_name])

        globals()[photo_label_name].configure(image=globals()[photo_name])
        globals()[photo_label_name].image = globals()[photo_name]

        song_name_label_name = "song_name_label" + str(i + 1)
        globals()[song_name_label_name] = tk.Label(frame_for_songs[frame_name],
                                                   text="Song Name: " + infos[i]["name"],
                                                   font=("Arial", 12),
                                                   bg="#191414",
                                                   fg="white")
        globals()[song_name_label_name].pack(anchor=tk.W)

        artist_name_label_name = "artist_name_label" + str(i + 1)
        globals()[artist_name_label_name] = tk.Label(frame_for_songs[frame_name],
                                                     text="Artist Name: " + infos[i]["artists"],
                                                     font=("Arial", 12),
                                                     bg="#191414",
                                                     fg="white")
        globals()[artist_name_label_name].pack(anchor=tk.W)

        link_button_name = "link_button" + str(i + 1)
        globals()[link_button_name] = tk.Label(frame_for_songs[frame_name],
                                               text="Listen on Spotify",
                                               cursor="hand2",
                                               fg="#30d5c8",
                                               bg="#191414")
        globals()[link_button_name].pack(anchor=tk.W)
        globals()[link_button_name].bind("<Button-1>", lambda e, i=i: open_link(infos[i]["url"]))


def login_new_spotify_account():
    if os.path.exists(".cache"):
        os.remove(".cache")
    for i in range(5):
        frame_name = "frame_for_songs" + str(i + 1)
        if frame_name in frame_for_songs and frame_for_songs[frame_name].winfo_ismapped():
            frame_for_songs[frame_name].destroy()
    suggestion()


def login_old_spotify_account():
    for i in range(5):
        frame_name = "frame_for_songs" + str(i + 1)
        if frame_name in frame_for_songs and frame_for_songs[frame_name].winfo_ismapped():
            frame_for_songs[frame_name].destroy()
    suggestion()


window = tk.Tk()

# window settings
window.title("Song Recommender")
window.configure(bg="#191414")
set_window_geometry()
window.resizable(False, False)
current_dir = os.path.dirname(__file__)
icon_path = os.path.join(current_dir, "icon.ico")
window.iconbitmap(icon_path)
# end window settings

# scrollbar settings
scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
# end scrollbar settings

# main canvas frame
canvas = tk.Canvas(window, yscrollcommand=scrollbar.set, bg="#191414")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=canvas.yview)
# end main canvas frame

# ttk style
style = ttk.Style()
style.configure("Custom.TFrame", background="#191414", pady=50, padx=10)
# end ttk style

# frame for suggestions
frame_for_suggestions = ttk.Frame(canvas,
                                  style="Custom.TFrame")
frame_for_suggestions.pack(anchor=tk.N)
# end frame for suggestions

# frame for buttons
frame_for_buttons = ttk.Frame(canvas,
                              style="Custom.TFrame")
frame_for_buttons.pack(anchor=tk.CENTER)

frame_for_buttons2 = tk.Frame(frame_for_buttons,
                              bg="#191414")
frame_for_buttons2.pack(side=tk.TOP)

login_label1 = tk.Label(frame_for_buttons2,
                        text="Login to Spotify",
                        font=("Arial", 12),
                        bg="#191414",
                        fg="white")
login_label1.pack(side=tk.TOP)

login_button1 = tk.Button(frame_for_buttons2,
                          text="Login With Old Spotify Account",
                          width=25, font=("Arial", 12),
                          command=login_old_spotify_account,
                          bg="#1DB954",
                          fg="white",
                          activebackground="white",
                          activeforeground="#1DB954")
login_button1.pack(side=tk.LEFT, padx=5)

login_button2 = tk.Button(frame_for_buttons2,
                          text="Login With New Spotify Account",
                          width=25, font=("Arial", 12),
                          command=login_new_spotify_account,
                          bg="#1DB954",
                          fg="white",
                          activebackground="white",
                          activeforeground="#1DB954")
login_button2.pack(side=tk.LEFT, padx=5)

frame_for_buttons3 = tk.Frame(frame_for_buttons)
frame_for_buttons3.pack(side=tk.BOTTOM)

login_label2 = tk.Label(frame_for_buttons3,
                        text="If you login with a new account, you need to log out from your old account from your browser.",
                        font=("Arial", 8),
                        bg="#191414",
                        fg="white")
login_label2.pack(side=tk.BOTTOM)
# end frame for buttons

window.mainloop()
