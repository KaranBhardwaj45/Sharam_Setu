import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import threading
import os
from google_auth_oauthlib.flow import InstalledAppFlow
import requests

# DB setup
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
""")
conn.commit()

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Traditional register
def register_user():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Missing Info", "Please fill all fields.")
        return

    try:
        hashed_pw = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
        conn.commit()
        messagebox.showinfo("Success", "Registered successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

# Google Register
def google_register():
    def auth_flow():
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json",
                scopes=["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
            )
            creds = flow.run_local_server(port=0)
            user_info = requests.get(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                params={"alt": "json"},
                headers={"Authorization": f"Bearer {creds.token}"}
            ).json()

            email = user_info.get("email")
            if email:
                try:
                    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (email, None))
                    conn.commit()
                    messagebox.showinfo("Google Registered", f"Registered via Google as: {email}")
                except sqlite3.IntegrityError:
                    messagebox.showwarning("Already Registered", "This Google account is already registered.")
            else:
                messagebox.showerror("Error", "Failed to get email from Google.")
        except Exception as e:
            messagebox.showerror("Google Auth Error", str(e))

    threading.Thread(target=auth_flow).start()

# GUI setup
root = tk.Tk()
root.title("Register Page")
root.geometry("380x300")
root.configure(bg="#121212")

tk.Label(root, text="Register", font=("Helvetica", 20, "bold"), fg="white", bg="#121212").pack(pady=10)

tk.Label(root, text="Username", fg="white", bg="#121212").pack()
entry_username = tk.Entry(root)
entry_username.pack(pady=5)

tk.Label(root, text="Password", fg="white", bg="#121212").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack(pady=5)

tk.Button(root, text="Register", command=register_user, bg="#1f6feb", fg="white", width=20).pack(pady=10)
tk.Label(root, text="or", fg="gray", bg="#121212").pack()

tk.Button(root, text="Register with Google", command=google_register, bg="#db4437", fg="white", width=25).pack(pady=10)

root.mainloop()
conn.close()
