import tkinter as tk
from tkinter import ttk, messagebox
import random
from playsound import playsound
import threading

# ---- Configuration ----
AI_MODE = False  # Set to True to play vs AI

def play_sound(file):
    threading.Thread(target=lambda: playsound(file), daemon=True).start()

def check_winner():
    global winner
    for combo in [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]:
        if buttons[combo[0]]["text"] == buttons[combo[1]]["text"] == buttons[combo[2]]["text"] != "":
            winner = True
            flash_winner(combo)
            play_sound("win.mp3")
            messagebox.showinfo("🎉 Game Over", f"Player {buttons[combo[0]]['text']} wins!")
            return

    if all(button["text"] != "" for button in buttons) and not winner:
        play_sound("draw.mp3")
        messagebox.showinfo("🤝 Game Over", "It's a Draw!")
        winner = True

def button_click(index):
    if buttons[index]["text"] == "" and not winner:
        buttons[index]["text"] = current_player
        play_sound("click.mp3")
        check_winner()
        if not winner:
            toggle_player()
            if AI_MODE and current_player == "O":
                root.after(300, ai_move)

def toggle_player():
    global current_player
    current_player = "X" if current_player == "O" else "O"
    label.config(text=f"Player {current_player}'s turn")

def reset_game():
    global current_player, winner
    for btn in buttons:
        btn.config(text="", style='TButton')
    current_player = "X"
    winner = False
    label.config(text="Player X's turn")

def ai_move():
    empty_indices = [i for i, b in enumerate(buttons) if b["text"] == ""]
    if empty_indices:
        choice = random.choice(empty_indices)
        button_click(choice)

def flash_winner(combo, count=6):
    def flash():
        color = 'green' if count % 2 == 0 else 'white'
        for i in combo:
            buttons[i].config(style='Winning.TButton' if color == 'green' else 'TButton')
        if count > 0:
            root.after(300, lambda: flash_winner(combo, count-1))
    flash()

def toggle_theme():
    global is_dark
    is_dark = not is_dark
    if is_dark:
        root.configure(bg="#2e2e2e")
        label.config(background="#2e2e2e", foreground="white")
        style.configure('TButton', background="#555", foreground="white")
    else:
        root.configure(bg="#f0f0f0")
        label.config(background="#f0f0f0", foreground="black")
        style.configure('TButton', background="#f0f0f0", foreground="black")

# ---- GUI Setup ----
root = tk.Tk()
root.title("Modern Tic-Tac-Toe")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=("Helvetica", 24), width=5, height=2, padding=10)
style.configure('Winning.TButton', background="green", foreground="white", font=("Helvetica", 24, "bold"))

buttons = [ttk.Button(root, text="", command=lambda i=i: button_click(i)) for i in range(9)]
for i, button in enumerate(buttons):
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

current_player = "X"
winner = False
is_dark = False

label = ttk.Label(root, text="Player X's turn", font=("Helvetica", 16))
label.grid(row=3, column=0, columnspan=3, pady=10)

reset_btn = ttk.Button(root, text="🔁 Reset", command=reset_game)
reset_btn.grid(row=4, column=0, pady=10)

theme_btn = ttk.Button(root, text="🌓 Toggle Theme", command=toggle_theme)
theme_btn.grid(row=4, column=2, pady=10)

root.mainloop()
