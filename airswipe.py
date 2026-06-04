import tkinter as tk
from tkinter import Button
from threading import Thread
import subprocess


def start_hand_gesture_recognition(script_path):
    try:
        thread = Thread(
            target=subprocess.run,
            args=(["python", script_path],)
        )
        thread.start()

    except Exception as e:
        print(f"Error starting hand gesture recognition: {e}")


def on_key_press(event):
    key = event.char.upper()

    for gesture_name, script_path, virtual_key in gesture_data:
        if key == virtual_key:
            start_hand_gesture_recognition(script_path)


def on_enter(event):
    event.widget.config(
        bg="#1a1aff",
        fg="black",
        relief="sunken"
    )


def on_leave(event):
    event.widget.config(
        bg="#04048c",
        fg="white",
        relief="raised"
    )


root = tk.Tk()
root.title("AirSwipe Gesture Recognition")
root.configure(bg="#080533")


gesture_data = [
    ("Advance", "main.py", "A"),
    ("Scroll", "scroll.py", "S"),
    ("PPT Swipe", "pptswipe.py", "P"),
    ("Min-Max", "minmax.py", "M"),
    ("Copy-Paste", "copypaste.py", "C"),
    ("Zoom", "zoomin.py", "Z")
]


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root.geometry(f"{screen_width}x{screen_height}+0+0")


heading_label = tk.Label(
    root,
    text="AirSwipe",
    font=("Impact", 60, "bold"),
    fg="white",
    bg="#080533"
)

heading_label.pack(pady=70)


button_width = 20
button_height = 3

buttons_per_row = 3

button_font = ("Helvetica", 16, "bold")

button_padx = 40
button_pady = 40


frame1 = tk.Frame(root, bg="#080533")
frame2 = tk.Frame(root, bg="#080533")

frame1.pack(side=tk.TOP)
frame2.pack(side=tk.TOP)


for i, (gesture_name, script_path, virtual_key) in enumerate(gesture_data):

    gesture_button = Button(
        root,
        text=gesture_name,
        command=lambda path=script_path:
        start_hand_gesture_recognition(path),
        width=button_width,
        height=button_height,
        font=button_font,
        bg="#04048c",
        fg="white",
        relief="raised",
        bd=3
    )

    gesture_button.bind("<Enter>", on_enter)
    gesture_button.bind("<Leave>", on_leave)

    if i < buttons_per_row:
        gesture_button.pack(
            side=tk.LEFT,
            padx=button_padx,
            pady=button_pady,
            in_=frame1
        )
    else:
        gesture_button.pack(
            side=tk.LEFT,
            padx=button_padx,
            pady=button_pady,
            in_=frame2
        )


root.bind("<KeyPress>", on_key_press)

root.mainloop()