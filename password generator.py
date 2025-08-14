import tkinter as tk
from tkinter import messagebox
import secrets, string, math

HISTORY_FILE = "passwords.txt"

def build_charset():
    chars = ""
    if var_lower.get(): chars += string.ascii_lowercase
    if var_upper.get(): chars += string.ascii_uppercase
    if var_digits.get(): chars += string.digits
    if var_symbols.get(): chars += "!@#$%^&*()-_=+[]{};:,.<>/?|\\"
    return chars

def generate_password():
    charset = build_charset()
    if not charset:
        return messagebox.showwarning("Warning", "Select at least one character type.")
    pwd = "".join(secrets.choice(charset) for _ in range(length_var.get()))
    pwd_var.set(pwd)
    show_strength()
    show_crack_time(charset)

def copy_password():
    if not pwd_var.get():
        return messagebox.showwarning("Warning", "No password to copy.")
    root.clipboard_clear(); root.clipboard_append(pwd_var.get())
    messagebox.showinfo("Copied", "Password copied!")

def save_password():
    if not pwd_var.get():
        return messagebox.showwarning("Warning", "No password to save.")
    with open(HISTORY_FILE, "a") as f:
        note = note_entry.get().strip()
        f.write(f"{note} :: {pwd_var.get()}\n" if note else f"{pwd_var.get()}\n")
    messagebox.showinfo("Saved", "Password saved.")
    note_entry.delete(0, tk.END)

def show_strength():
    pwd = pwd_var.get()
    score = sum([len(pwd) >= 8,
                 any(c.islower() for c in pwd),
                 any(c.isupper() for c in pwd),
                 any(c.isdigit() for c in pwd),
                 any(c in "!@#$%^&*()-_=+[]{};:,.<>/?|\\" for c in pwd)])
    strength_lbl.config(text=f"Strength: {['Very Weak','Weak','Fair','Good','Strong','Very Strong'][score]}")

def show_crack_time(charset):
    length = len(pwd_var.get())
    charset_size = len(charset)
    guesses_per_sec = 1e9  # 1 billion guesses per second
    total_combinations = charset_size ** length
    seconds = total_combinations / guesses_per_sec
    crack_time_lbl.config(text=f"Crack Time: {human_readable_time(seconds)}")

def human_readable_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} sec"
    elif seconds < 3600:
        return f"{seconds/60:.2f} min"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        years = seconds / 31536000
        return f"{years:.2e} years" if years > 1e6 else f"{years:.2f} years"

root = tk.Tk()
root.title("🔐 Password Generator")
root.geometry("500x440")
root.configure(bg="#1e1f29")

tk.Label(root, text="Password Generator", font=("Segoe UI", 18, "bold"), bg="#1e1f29", fg="#ffdd57").pack(pady=10)

frame = tk.Frame(root, bg="#2b2d3a", padx=10, pady=10)
frame.pack(padx=12, pady=6, fill="x")

length_var = tk.IntVar(value=16)
tk.Label(frame, text="Length:", bg="#2b2d3a", fg="white").grid(row=0, column=0, sticky="w")
tk.Scale(frame, from_=4, to=64, orient="horizontal", variable=length_var, bg="#2b2d3a", troughcolor="#44475a", fg="white").grid(row=0, column=1, columnspan=3, sticky="ew", padx=6)

# Fixed BooleanVar creation
var_lower = tk.BooleanVar(value=True)
var_upper = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

for i, (txt, var) in enumerate([("lowercase", var_lower), ("UPPERCASE", var_upper), ("digits", var_digits), ("symbols", var_symbols)]):
    tk.Checkbutton(frame, text=txt, variable=var, bg="#2b2d3a", fg="white", selectcolor="#6272a4").grid(row=1, column=i, sticky="w")

pwd_var = tk.StringVar()
tk.Entry(root, textvariable=pwd_var, font=("Consolas", 14), justify="center", bg="white").pack(fill="x", padx=24, pady=(10,4))

btn_frame = tk.Frame(root, bg="#1e1f29")
btn_frame.pack(pady=6)
tk.Button(btn_frame, text="Generate", command=generate_password, bg="#50fa7b", fg="black", width=12).grid(row=0, column=0, padx=8)
tk.Button(btn_frame, text="Copy", command=copy_password, bg="#8be9fd", fg="black", width=10).grid(row=0, column=1, padx=8)
tk.Button(btn_frame, text="Save", command=save_password, bg="#ff79c6", fg="black", width=10).grid(row=0, column=2, padx=8)

note_entry = tk.Entry(root, font=("Segoe UI", 10))
note_entry.pack(fill="x", padx=24, pady=(6,0))
note_entry.insert(0, "Optional note")

strength_lbl = tk.Label(root, text="Strength: ", bg="#1e1f29", fg="#cbd5e1", font=("Segoe UI", 10, "bold"))
strength_lbl.pack(pady=3)

crack_time_lbl = tk.Label(root, text="Crack Time: ", bg="#1e1f29", fg="#cbd5e1", font=("Segoe UI", 10, "bold"))
crack_time_lbl.pack(pady=3)

root.bind("<Return>", lambda e: generate_password())
root.mainloop()
