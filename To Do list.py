import tkinter as tk
from tkinter import messagebox
import json
import os
import threading
import time

TASK_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks():
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f)

def add_task():
    task = entry.get()
    if task:
        tasks.append({"task": task, "done": False, "time": None})
        update_task_list()
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def toggle_done(index):
    tasks[index]["done"] = not tasks[index]["done"]
    update_task_list()
    save_tasks()

def delete_task(index):
    tasks.pop(index)
    update_task_list()
    save_tasks()

def set_timer(index):
    try:
        hours = int(hour_entry.get())
        minutes = int(min_entry.get())
        seconds = int(sec_entry.get())
        total_seconds = hours * 3600 + minutes * 60 + seconds
        if total_seconds > 0:
            tasks[index]["time"] = total_seconds
            threading.Thread(target=run_timer, args=(index,), daemon=True).start()
            save_tasks()
        else:
            messagebox.showerror("Error", "Time must be greater than 0.")
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")

def run_timer(index):
    while tasks[index]["time"] is not None and tasks[index]["time"] > 0:
        time.sleep(1)
        tasks[index]["time"] -= 1
        update_task_list()
        if tasks[index]["time"] == 0:
            messagebox.showinfo("Timer Done", f"Time's up for: {tasks[index]['task']}")
            tasks[index]["time"] = None
            save_tasks()

def format_time(seconds):
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def update_task_list():
    for widget in task_frame.winfo_children():
        widget.destroy()

    for i, task_data in enumerate(tasks):
        frame = tk.Frame(task_frame, bg="#f0f8ff", padx=5, pady=5)
        frame.pack(fill="x", pady=3)

        var = tk.BooleanVar(value=task_data["done"])
        chk = tk.Checkbutton(frame, text=task_data["task"], variable=var,
                             onvalue=True, offvalue=False,
                             command=lambda i=i: toggle_done(i),
                             font=("Arial", 12), bg="#f0f8ff")
        chk.pack(side="left")

        if task_data["done"]:
            chk.config(fg="gray", selectcolor="#d3d3d3")

        if task_data["time"]:
            timer_lbl = tk.Label(frame, text=f"⏱ {format_time(task_data['time'])}", font=("Arial", 11), fg="blue", bg="#f0f8ff")
            timer_lbl.pack(side="left", padx=5)

        del_btn = tk.Button(frame, text="❌", command=lambda i=i: delete_task(i), bg="#ff6961", fg="white", font=("Arial", 10, "bold"))
        del_btn.pack(side="right", padx=5)

        timer_btn = tk.Button(frame, text="⏱ Set", command=lambda i=i: set_timer(i), bg="#77dd77", fg="black", font=("Arial", 10, "bold"))
        timer_btn.pack(side="right", padx=5)

root = tk.Tk()
root.title("To-Do List with Timer")
root.geometry("550x650")
root.configure(bg="#add8e6")

tasks = load_tasks()

title_lbl = tk.Label(root, text="📝 To-Do List with Timer", font=("Arial", 16, "bold"), bg="#add8e6", fg="darkblue")
title_lbl.pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=5)

tk.Button(root, text="Add Task", command=add_task, bg="#77dd77", fg="black", font=("Arial", 12, "bold")).pack(pady=5)

time_frame = tk.Frame(root, bg="#add8e6")
time_frame.pack(pady=5)

hour_entry = tk.Entry(time_frame, font=("Arial", 12), width=5)
hour_entry.pack(side="left", padx=2)
hour_entry.insert(0, "0")

min_entry = tk.Entry(time_frame, font=("Arial", 12), width=5)
min_entry.pack(side="left", padx=2)
min_entry.insert(0, "0")

sec_entry = tk.Entry(time_frame, font=("Arial", 12), width=5)
sec_entry.pack(side="left", padx=2)
sec_entry.insert(0, "0")

task_frame = tk.Frame(root, bg="#add8e6")
task_frame.pack(fill="both", expand=True, pady=10)

update_task_list()

root.mainloop()
