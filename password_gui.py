import tkinter as tk
import re
import random
import string
import hashlib

FILE_NAME = "old_passwords.txt"

# Hash password for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Check strength
def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*]", password):
        score += 1

    if score <= 2:
        return "Weak", "red"
    elif score <= 4:
        return "Moderate", "orange"
    else:
        return "Strong", "green"

# Suggest password
def suggest_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    suggestion = ''.join(random.choice(chars) for _ in range(12))
    suggestion_label.config(text=f"Suggestion: {suggestion}")

# Check reuse
def is_reused(password):
    hashed = hash_password(password)
    try:
        with open(FILE_NAME, "r") as f:
            return hashed in f.read().splitlines()
    except FileNotFoundError:
        return False

# Save password
def save_password(password):
    hashed = hash_password(password)
    with open(FILE_NAME, "a") as f:
        f.write(hashed + "\n")

# Update strength
def update_strength(event):
    password = entry.get()

    if not password:
        result_label.config(text="Strength: ", fg="black")
        return

    if is_reused(password):
        result_label.config(text="Password already used!", fg="purple")
        return

    strength, color = check_strength(password)
    result_label.config(text=f"Strength: {strength}", fg=color)

# Submit
def submit_password():
    password = entry.get()
    if password:
        save_password(password)
        result_label.config(text="Password saved securely!", fg="blue")

# GUI
root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("400x320")

tk.Label(root, text="Password Strength Analyzer", font=("Arial", 14)).pack(pady=10)

entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
entry.pack(pady=10)
entry.bind("<KeyRelease>", update_strength)

result_label = tk.Label(root, text="Strength: ", font=("Arial", 12))
result_label.pack(pady=10)

tk.Button(root, text="Suggest Strong Password", command=suggest_password).pack(pady=5)

suggestion_label = tk.Label(root, text="", font=("Arial", 10))
suggestion_label.pack()

tk.Button(root, text="Save Password", command=submit_password).pack(pady=10)

root.mainloop()