import tkinter as tk
from tkinter import filedialog

def upload_button_clicked():
    upload_section.pack()
    create_user_section.pack_forget()

def create_user_button_clicked():
    create_user_section.pack()
    upload_section.pack_forget()

def send_button_clicked():
    username = upload_username_entry.get()
    password = upload_password_entry.get()
    file_path = file_path_var.get()

    # Construct message format: "<username>,<password> upload"
    message = f"{username},{password} upload"

    # Now you can send this 'message' to your server
    # along with the file using your preferred method

    # For demonstration purposes, printing the message
    print("Sending message:", message)

def create_user_button_submit_clicked():
    new_username = create_username_entry.get()
    new_password = create_password_entry.get()
    confirm_password = confirm_password_entry.get()

    # Validate passwords match
    if new_password != confirm_password:
        print("Passwords don't match")
        return

    # Construct message format: "<new_username>,<new_password> createuser"
    message = f"{new_username},{new_password} createuser"

    # Now you can send this 'message' to your server for user creation

    # For demonstration purposes, printing the message
    print("Sending message:", message)

# Create main window
root = tk.Tk()
root.title("Client UI")

# Upload Section
upload_section = tk.Frame(root)
upload_username_label = tk.Label(upload_section, text="Username:")
upload_username_entry = tk.Entry(upload_section)
upload_password_label = tk.Label(upload_section, text="Password:")
upload_password_entry = tk.Entry(upload_section, show="*")
file_path_var = tk.StringVar()
file_path_label = tk.Label(upload_section, text="File Path:")
file_path_entry = tk.Entry(upload_section, textvariable=file_path_var)
browse_button = tk.Button(upload_section, text="Browse", command=lambda: file_path_var.set(filedialog.askopenfilename()))
send_button = tk.Button(upload_section, text="Send", command=send_button_clicked)

# Create User Section
create_user_section = tk.Frame(root)
create_username_label = tk.Label(create_user_section, text="Username:")
create_username_entry = tk.Entry(create_user_section)
create_password_label = tk.Label(create_user_section, text="Password:")
create_password_entry = tk.Entry(create_user_section, show="*")
confirm_password_label = tk.Label(create_user_section, text="Confirm Password:")
confirm_password_entry = tk.Entry(create_user_section, show="*")
create_user_submit_button = tk.Button(create_user_section, text="Create", command=create_user_button_submit_clicked)

# Configure layout
upload_username_label.grid(row=0, column=0, sticky="e")
upload_username_entry.grid(row=0, column=1)
upload_password_label.grid(row=1, column=0, sticky="e")
upload_password_entry.grid(row=1, column=1)
file_path_label.grid(row=2, column=0, sticky="e")
file_path_entry.grid(row=2, column=1)
browse_button.grid(row=2, column=2)
send_button.grid(row=3, column=1)

create_username_label.grid(row=0, column=0, sticky="e")
create_username_entry.grid(row=0, column=1)
create_password_label.grid(row=1, column=0, sticky="e")
create_password_entry.grid(row=1, column=1)
confirm_password_label.grid(row=2, column=0, sticky="e")
confirm_password_entry.grid(row=2, column=1)
create_user_submit_button.grid(row=3, column=1)

# Buttons for switching sections
upload_button = tk.Button(root, text="Upload", command=upload_button_clicked)
upload_button.pack(side="left")
create_user_button = tk.Button(root, text="Create User", command=create_user_button_clicked)
create_user_button.pack(side="right")

# Start the Tkinter event loop
root.mainloop()
