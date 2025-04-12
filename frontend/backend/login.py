import tkinter as tk
from tkinter import messagebox

# Dummy user data
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Main window
root = tk.Tk()
root.title("Login Page")
root.geometry("350x200")
root.configure(bg="#1e1e1e")  # dark background

# Title
label_title = tk.Label(root, text="Login", font=("Helvetica", 18, "bold"), fg="white", bg="#1e1e1e")
label_title.pack(pady=10)

# Username
label_username = tk.Label(root, text="Username", fg="white", bg="#1e1e1e")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

# Password
label_password = tk.Label(root, text="Password", fg="white", bg="#1e1e1e")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

# Login button
login_button = tk.Button(root, text="Login", command=login, bg="#2e8b57", fg="white")
login_button.pack(pady=10)

root.mainloop()
