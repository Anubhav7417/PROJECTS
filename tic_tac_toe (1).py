
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("❌⭕ Tic Tac Toe")
root.geometry("360x420")
root.configure(bg="#0f172a")

current = tk.StringVar(value="X")
board = [["" for _ in range(3)] for _ in range(3)]
buttons = []

def check_winner():
    lines = []
    # rows and cols
    for i in range(3):
        lines.append(board[i])
        lines.append([board[0][i], board[1][i], board[2][i]])
    # diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])
    for line in lines:
        if line[0] and line[0] == line[1] == line[2]:
            return line[0]
    # draw
    if all(board[r][c] for r in range(3) for c in range(3)):
        return "Draw"
    return None

def on_click(r, c):
    if board[r][c]:
        return
    b = buttons[r][c]
    b.config(text=current.get(), state="disabled")
    board[r][c] = current.get()

    res = check_winner()
    if res:
        if res == "Draw":
            messagebox.showinfo("Result", "It's a Draw!")
        else:
            messagebox.showinfo("Winner", f"{res} wins!")
        reset()
        return

    current.set("O" if current.get() == "X" else "X")
    turn_label.config(text=f"Turn: {current.get()}")

def reset():
    for r in range(3):
        for c in range(3):
            board[r][c] = ""
            buttons[r][c].config(text="", state="normal")
    current.set("X")
    turn_label.config(text=f"Turn: {current.get()}")

title = tk.Label(root, text="Tic Tac Toe", bg="#0f172a", fg="#e2e8f0", font=("Segoe UI", 18, "bold"))
title.pack(pady=10)

grid = tk.Frame(root, bg="#0f172a")
grid.pack()

for r in range(3):
    row_btns = []
    for c in range(3):
        btn = tk.Button(grid, text="", width=6, height=3, font=("Segoe UI", 20, "bold"),
                        bg="#1f2937", fg="#f8fafc", activebackground="#334155",
                        command=lambda r=r, c=c: on_click(r, c))
        btn.grid(row=r, column=c, padx=6, pady=6)
        row_btns.append(btn)
    buttons.append(row_btns)

ctrl = tk.Frame(root, bg="#0f172a")
ctrl.pack(pady=6)
turn_label = tk.Label(ctrl, text=f"Turn: {current.get()}", bg="#0f172a", fg="#a5b4fc", font=("Segoe UI", 12, "bold"))
turn_label.grid(row=0, column=0, padx=6)
tk.Button(ctrl, text="Reset", command=reset, bg="#22c55e", fg="black", width=10, font=("Segoe UI", 11, "bold")).grid(row=0, column=1, padx=6)

root.mainloop()
