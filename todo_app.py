import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

# Initialize task list with completion status and timestamps
tasks = []

# Load tasks from file (if any)
def load_tasks():
    global tasks
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            for line in file.readlines():
                task, done, created_at, completed_at = line.strip().split("|")
                tasks.append((task, done == 'True', created_at, completed_at if completed_at != "None" else None))

# Save tasks to file
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task, done, created_at, completed_at in tasks:
            completed_at_str = completed_at if completed_at else "None"
            file.write(f"{task}|{done}|{created_at}|{completed_at_str}\n")

# Add task to the list
def add_task():
    task = task_entry.get()
    if task:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasks.append((task, False, current_time, None))  # New task is marked as not done with a creation time
        update_task_listbox()
        task_entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

# Remove selected task from the list
def remove_task():
    try:
        selected_task_index = task_listbox.curselection()[0]
        tasks.pop(selected_task_index)
        update_task_listbox()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Selection Error", "Please select a task to remove.")

# Toggle task completion
def toggle_task(event):
    selected_task_index = task_listbox.curselection()[0]
    task, done, created_at, completed_at = tasks[selected_task_index]
    if not done:
        completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        completed_at = None  # Reset the completion time if toggling to not done
    tasks[selected_task_index] = (task, not done, created_at, completed_at)
    update_task_listbox()
    save_tasks()

# Update the listbox to show the current tasks with checkboxes and timestamps
def update_task_listbox():
    task_listbox.delete(0, tk.END)
    for task, done, created_at, completed_at in tasks:
        status = "✔" if done else " "
        time_info = f"(Created: {created_at}" + (f", Done: {completed_at})" if completed_at else ")")
        display_text = f"[{status}] {task} {time_info}"
        task_listbox.insert(tk.END, display_text)

# Create the main window
root = tk.Tk()
root.title("To-Do List with Timestamps")
root.geometry("600x450")
root.configure(bg="#d9eafc")  # Light blue background

# Set up style
style = ttk.Style(root)
style.theme_use("clam")

# Blue color scheme for buttons, labels, and entries
style.configure("TButton", font=("Helvetica", 12), background="#0d47a1", foreground="white", padding=10)  # Dark blue button
style.map("TButton", background=[("active", "#1565c0")])  # Lighter blue when pressed
style.configure("TLabel", font=("Helvetica", 12), background="#d9eafc", foreground="#333")  # Dark text on light blue
style.configure("TEntry", font=("Helvetica", 12), padding=5)

# Task entry field
task_entry = ttk.Entry(root, width=30)
task_entry.pack(pady=10)

# Add task button
add_button = ttk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=5)

# Task listbox with a frame for better control over background
listbox_frame = tk.Frame(root, bd=1, relief=tk.SUNKEN, bg="#f0f4ff")  # Very light blue background for listbox
listbox_frame.pack(pady=10, padx=10)

task_listbox = tk.Listbox(listbox_frame, width=60, height=10, font=("Helvetica", 12), bg="#ffffff", bd=0)
task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Scrollbar for the task listbox
scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
task_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=task_listbox.yview)

# Bind listbox click event for toggling task status
task_listbox.bind("<Double-1>", toggle_task)

# Remove task button
remove_button = ttk.Button(root, text="Remove Task", command=remove_task)
remove_button.pack(pady=5)

# Load tasks when the app starts
load_tasks()
update_task_listbox()

# Run the Tkinter event loop
root.mainloop()
