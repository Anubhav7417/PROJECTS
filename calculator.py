import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import random

MATH_FACTS = [
    "Zero is the only number that cannot be represented by Roman numerals.",
    "A 'jiffy' is an actual unit of time: 1/100th of a second.",
    "The number 'e' is as important as π in mathematics.",
    "111,111,111 × 111,111,111 = 12,345,678,987,654,321",
    "A googol is 1 followed by 100 zeros."
]

RATES = {
    "USD": {"EUR": 0.91, "GBP": 0.78, "INR": 83.1},
    "EUR": {"USD": 1.1, "GBP": 0.86, "INR": 91.4},
    "GBP": {"USD": 1.28, "EUR": 1.16, "INR": 106.3},
    "INR": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0094}
}

def add_to_expression(symbol):
    current = expression_var.get()
    expression_var.set(current + str(symbol))

def clear_expression():
    expression_var.set("")

def calculate():
    try:
        result = eval(expression_var.get())
        expression_var.set(str(result))
    except Exception:
        messagebox.showerror("Error", "Invalid Expression")

def show_fact():
    messagebox.showinfo("Math Fact", random.choice(MATH_FACTS))

def convert_currency():
    try:
        amount = float(conv_amount.get())
        from_cur = conv_from.get()
        to_cur = conv_to.get()
        if from_cur == to_cur:
            messagebox.showinfo("Result", f"{amount} {from_cur} = {amount} {to_cur}")
            return
        converted = amount * RATES[from_cur][to_cur]
        messagebox.showinfo("Result", f"{amount} {from_cur} = {converted:.2f} {to_cur}")
    except ValueError:
        messagebox.showerror("Error", "Enter a valid amount.")

def calc_age():
    try:
        y = int(year_entry.get())
        m = int(month_entry.get())
        d = int(day_entry.get())
    except ValueError:
        return messagebox.showerror("Error", "Year, month and day must be integers.")

    if not (1 <= m <= 12):
        return messagebox.showerror("Error", "Month must be 1-12.")
    if not (1 <= d <= 31):
        return messagebox.showerror("Error", "Day must be 1-31.")

    try:
        dob = datetime(y, m, d)
    except ValueError:
        return messagebox.showerror("Error", "Invalid date (check day for the month and leap years).")

    today = datetime.today()
    if dob > today:
        return messagebox.showerror("Error", "DOB is in the future.")

    years = today.year - dob.year
    months = today.month - dob.month
    days = today.day - dob.day

    if days < 0:
        # borrow days from previous month
        prev_month = (today.month - 1) or 12
        prev_year = today.year if today.month != 1 else today.year - 1
        # compute days in previous month
        from calendar import monthrange
        days_in_prev = monthrange(prev_year, prev_month)[1]
        days += days_in_prev
        months -= 1

    if months < 0:
        months += 12
        years -= 1

    messagebox.showinfo("Your Age", f"You are {years} years, {months} months, {days} days old.")

root = tk.Tk()
root.title("🧮 Smart Calculator")
root.geometry("420x660")
root.configure(bg="#1e1f29")

tk.Label(root, text="Smart Calculator", font=("Segoe UI", 18, "bold"), bg="#1e1f29", fg="#ffdd57").pack(pady=10)

expression_var = tk.StringVar()
tk.Entry(root, textvariable=expression_var, font=("Consolas", 18), justify="right").pack(fill="x", padx=20, pady=5)

btn_frame = tk.Frame(root, bg="#1e1f29")
btn_frame.pack()

buttons = [
    "7","8","9","/",
    "4","5","6","*",
    "1","2","3","-",
    "0",".","%","+",
    "**","C","=","Fact"
]

for i, btn in enumerate(buttons):
    def cmd(x=btn):
        if x == "C":
            clear_expression()
        elif x == "=":
            calculate()
        elif x == "Fact":
            show_fact()
        else:
            add_to_expression(x)
    tk.Button(btn_frame, text=btn, command=cmd, width=5, height=2, bg="#44475a", fg="white").grid(row=i//4, column=i%4, padx=2, pady=2)

tk.Label(root, text="Currency Converter", bg="#1e1f29", fg="#8be9fd", font=("Segoe UI", 12, "bold")).pack(pady=(10,2))
conv_frame = tk.Frame(root, bg="#1e1f29")
conv_frame.pack()

conv_amount = tk.Entry(conv_frame, width=10)
conv_amount.grid(row=0, column=0, padx=5)

conv_from = tk.StringVar(value="USD")
conv_to = tk.StringVar(value="INR")
tk.OptionMenu(conv_frame, conv_from, *RATES.keys()).grid(row=0, column=1)
tk.Label(conv_frame, text="→", bg="#1e1f29", fg="white").grid(row=0, column=2)
tk.OptionMenu(conv_frame, conv_to, *RATES.keys()).grid(row=0, column=3)

tk.Button(conv_frame, text="Convert", command=convert_currency, bg="#50fa7b").grid(row=0, column=4, padx=5)

tk.Label(root, text="Age Calculator (enter numbers manually)", bg="#1e1f29", fg="#ff79c6", font=("Segoe UI", 12, "bold")).pack(pady=(12,2))

age_frame = tk.Frame(root, bg="#1e1f29")
age_frame.pack(pady=(0,6))

tk.Label(age_frame, text="Year", bg="#1e1f29", fg="white").grid(row=0, column=0, padx=6)
tk.Label(age_frame, text="Month", bg="#1e1f29", fg="white").grid(row=0, column=1, padx=6)
tk.Label(age_frame, text="Day", bg="#1e1f29", fg="white").grid(row=0, column=2, padx=6)

year_entry = tk.Entry(age_frame, width=8)
year_entry.grid(row=1, column=0, padx=6)
month_entry = tk.Entry(age_frame, width=6)
month_entry.grid(row=1, column=1, padx=6)
day_entry = tk.Entry(age_frame, width=6)
day_entry.grid(row=1, column=2, padx=6)

tk.Button(root, text="Calculate Age", command=calc_age, bg="#bd93f9").pack(pady=6)

root.mainloop()
