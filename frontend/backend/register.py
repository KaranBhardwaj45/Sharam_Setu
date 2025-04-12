import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

# Database setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL
    )
""")
conn.commit()

# Hash function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register logic
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Input Error", "All fields are required.")
        return

    hashed_pw = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")

# GUI setup
root = tk.Tk()
root.title("Register Page")
root.geometry("350x250")
root.configure(bg="#1e1e1e")

tk.Label(root, text="Register", font=("Helvetica", 18, "bold"), fg="white", bg="#1e1e1e").pack(pady=10)

tk.Label(root, text="Username", fg="white", bg="#1e1e1e").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password", fg="white", bg="#1e1e1e").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Register", command=register_user, bg="#0066cc", fg="white").pack(pady=15)

root.mainloop()

# Don't forget to close connection when app exits
conn.close()
