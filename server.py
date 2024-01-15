import socket
from threading import Thread
import tkinter as tk
from tkinter import filedialog
import json
from diffie_hellman_key_exchange import *
from test import *
from k import *
import random

global file_k
global file_list
global uploads
uploads=0
aes_key=generate_random_word()

def start_cloud_client():
    global client_socket2
    client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket2.connect(('192.168.175.150', 12200))


def receive_cloud_files(selected_file_name):
    global uploads
    uploads+=1
    x=encrypt(password,file_k)
    cmd=username+" "+selected_file_name+" download_file"
    client_socket2.send(cmd.encode())
    y=client_socket2.recv(1024).decode()
    rand_prime=generate_random_prime()
    primitive_roots=find_primitive_root(rand_prime)
    g=random.choice(primitive_roots)  
    private_key_A=generate_private_key(rand_prime)
    public_key_A = generate_public_key(g,private_key_A,rand_prime)
    client_socket2.send(str(g).encode())  #sending g 
    client_socket2.send(str(rand_prime).encode())  #sending prime
    x=client_socket2.recv(1024).decode()
    client_socket2.send(str(public_key_A).encode())   #sending public key
    public_key_B=int(client_socket2.recv(1024).decode())
    client_socket2.send(" ".encode())
    secret_key_A=generate_secret_key(public_key_B,private_key_A,rand_prime)
    print(g," ",private_key_A," ",public_key_B," ",secret_key_A)
    encrypted_aes_key=client_socket2.recv(1024).decode()
    decrypted_aes_key= decrypt_key(encrypted_aes_key,secret_key_A)
    print(encrypted_aes_key," ",decrypted_aes_key)
    file_path="downloads\\received_file.txt"

    with open(file_path, 'wb') as file:
        data = client_socket2.recv(1024)
        while data:
            file.write(data)
            data = client_socket2.recv(1024)
            x=data.decode()
    with open("downloads\\received_file.txt", 'r') as f:
        content = f.read()
    lines = [content[i:i+33] for i in range(0, len(content), 33)]
    for i in range(len(lines)):
        x=lines[i]
        lines[i]=x[0:32]
    decrypt_array(lines,decrypted_aes_key,selected_file_name)


def upload_file_into_cloud(selected_path):
    # x=encrypt(password,file_k)
    # cmd=username+" "+x+" upload_file"
    # client_socket2.send(cmd.encode())
    rand_prime=generate_random_prime()
    primitive_roots=find_primitive_root(rand_prime)
    g=random.choice(primitive_roots)  
    private_key_A=generate_private_key(rand_prime)
    public_key_A = generate_public_key(g,private_key_A,rand_prime)
    client_socket2.send(str(g).encode())  #sending g 
    client_socket2.send(str(rand_prime).encode())  #sending prime
    x=client_socket2.recv(1024).decode()
    client_socket2.send(str(public_key_A).encode())   #sending public key
    public_key_B=int(client_socket2.recv(1024).decode())
    client_socket2.send(" ".encode())
    secret_key_A=generate_secret_key(public_key_B,private_key_A,rand_prime)
    print(secret_key_A)
    encrypted_aes_key=client_socket2.recv(1024).decode()
    decrypted_aes_key= decrypt_key(encrypted_aes_key,secret_key_A)
        
    file_name = (selected_path.split("/")[-1]).split(".")[0]
    client_socket2.send(file_name.encode())
    encrypt_file(pad_space(selected_path),decrypted_aes_key)
    filename = "cipher_text.txt"
    with open(filename, 'rb') as file:
        data = file.read(1024)
        while data:
            client_socket2.send(data)
            data = file.read(1024)
        client_socket2.close()
        #client_socket2.send("DONE".encode())
        print(f"Sent {filename} to the client")

def get_selected_file_name():
    global selected_file
    selected_index = files_listbox.curselection()
    if selected_index:
        temp = files_listbox.get(selected_index[0])
        y=temp.split(".")
        selected_file=y[0]
        receive_cloud_files(selected_file)


def switch_to_signup():
    print("started sign")  
    login_frame.pack_forget()
    signup_frame.pack(pady=150)

def switch_to_login():
    signup_frame.pack_forget()
    login_frame.pack(pady=300)

def chat_page():
    login_frame.pack_forget()
    signup_frame.pack_forget()
    download_frame.pack_forget()
    upload_frame.pack_forget()
    messages_frame.pack(fill=tk.BOTH, expand=True)

def cloud_page():
    download_frame.pack_forget()
    upload_frame.pack_forget()
    messages_frame.pack_forget()  
    login_frame.pack(pady=300)

def navigate_to_download():
    cloud_page.pack_forget()
    download_frame.pack()
    y=encrypt(password,file_k)
    cmd=username+" "+y+" "+"give_list"
    client_socket2.send(cmd.encode())
    files_data = client_socket2.recv(1024).decode('utf-8')
    files_list = files_data.split("\n")
    for i in files_list:
        x=i.split("_")
        if(x[-1]=="key.txt"):
            files_list.remove(i)
    print(files_list)
    for file_name in files_list:
        files_listbox.insert(tk.END, file_name)


def navigate_to_upload():
    cloud_page.pack_forget()
    upload_frame.pack()
    x=encrypt(password,file_k)
    cmd=username+" "+x+" upload_file"
    client_socket2.send(cmd.encode())


def handle_client(client_socket, client_address):
    print(f"Accepted connection from {client_address}")
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            root.after(100, update_client_ui, decrypt(message,aes_key))  # Update server UI with received message
        except:
            break
def start_server():
    global server_socket, clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('192.168.175.70', 12456))  # Replace with your server IP and port
    server_socket.listen(5)
    print("Server is running...")

    while True:
        global client_socket
        client_socket, client_address = server_socket.accept()
        g=int(client_socket.recv(1024).decode())
        rand_prime=int(client_socket.recv(1024).decode())
        client_socket.send(" ".encode())
        public_key_A=int(client_socket.recv(1024).decode())
        print(g," ",rand_prime," ",public_key_A)
        private_key_B=generate_private_key(rand_prime)
        public_key_B=generate_public_key(g,private_key_B,rand_prime)
        client_socket.send(str(public_key_B).encode()) # senndinmg key
        x=client_socket.recv(1024).decode()
        secret_key_B=generate_secret_key(public_key_A,private_key_B,rand_prime)
        print(g," ",private_key_B," ",public_key_B," ",secret_key_B)
        encrypted_aes_key=encrypt_key(aes_key,secret_key_B)
        print("aes key : ",aes_key)
        print("encrypted key : ",encrypted_aes_key)
        client_socket.send(encrypted_aes_key.encode())

        client_thread = Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

def send_message():
    message = entry.get()
    entry.delete(0, tk.END)
    try:
        client_socket.send(bytes(encrypt(message,aes_key), "utf-8"))
        root.after(100, update_server_ui, message)  # Update client UI with sent message
    except:
        client_socket.close()

def update_client_ui(message):
    msg_frame = tk.Frame(messages_frame, bg="lightblue", padx=10, pady=5)
    msg_label = tk.Label(msg_frame, text=message, wraplength=350, justify=tk.RIGHT)
    msg_label.pack(anchor=tk.W)
    msg_frame.pack(fill=tk.X, padx=5, pady=5)

def update_server_ui(message):
    msg_frame = tk.Frame(messages_frame, bg="lightgreen", padx=10, pady=5)
    msg_label = tk.Label(msg_frame, text=message, wraplength=350, justify=tk.LEFT)
    msg_label.pack(anchor=tk.E)
    msg_frame.pack(fill=tk.X, padx=5, pady=5)

def create_user():
    print("name is  ",client_socket2.getsockname())
    print("started creation")
    new_username = signup_username_entry.get()
    new_password = signup_password_entry.get()
    confirm_password = confirm_password_entry.get()
    if(new_password!=confirm_password):
        print("passwords doesnt match")
        return
    pass_code=encrypt(new_password,"abcdefghijklmnop")
    cmd=new_username+" "+pass_code+" "+"create_user"
    client_socket2.send(cmd.encode())
    print("sent  ",cmd)
    check=client_socket2.recv(1024).decode()
    print(check)

def validate_login():
    files_listbox.delete(0, tk.END)
    global client_socket2
    if uploads>0:
        client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket2.connect(('192.168.175.150', 12200))
    global username
    global password
    username=login_username_entry.get()
    password=login_password_entry.get()
    pass_code=encrypt(password,"abcdefghijklmnop")
    cmd=username+" "+pass_code+" "+"is_user"
    client_socket2.send(cmd.encode())
    ack=client_socket2.recv(1024).decode()
    if(ack=="NO"):
        print("invalid username or password")
        return
    else:
        login_frame.pack_forget()
        cloud_page.pack()

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:  # Check if a file was selected
        text_box.delete(1.0, tk.END)  # Clear the current text box content
        text_box.insert(tk.END, file_path)  # Insert the selected file path into the text box

def upload_file():
    global uploads
    uploads+=1
    selected_path = text_box.get(1.0, tk.END).strip()  # Get the file path from the text box
    upload_file_into_cloud(selected_path)

root = tk.Tk()
root.title("ASCII CHAT")
root.geometry("1000x600")  # Set window size
########################################################################################
sidebar = tk.Frame(root, width=500, bg="lightgray")
sidebar.pack(fill=tk.X, side=tk.TOP)

button_home = tk.Button(sidebar, text="Home", command=chat_page)
button_home.pack(pady=5,side=tk.LEFT)

button_cloud_page = tk.Button(sidebar, text="Cloud", command=cloud_page)
button_cloud_page.pack(pady=5,side=tk.LEFT)
########################################################################################
messages_frame = tk.Frame(root)
messages_frame.pack(fill=tk.BOTH, expand=True)
file_k="abcdefghijklmnop"
send_button = tk.Button(messages_frame, text="Send", command=send_message)
send_button.pack(side=tk.BOTTOM)
entry = tk.Entry(messages_frame)
entry.bind("<Return>", send_message)
entry.pack(side=tk.BOTTOM,fill=tk.X, padx=5, pady=5)
########################################################################################


login_frame = tk.Frame(root)

login_welcome_label = tk.Label(login_frame, text="Welcome back, we missed you", font=("Arial", 14))
login_username_label = tk.Label(login_frame, text="Username:")
login_username_entry = tk.Entry(login_frame)
login_password_label = tk.Label(login_frame, text="Password:")
login_password_entry = tk.Entry(login_frame, show="*")
login_button = tk.Button(login_frame, text="Login",command=validate_login)

signup_button = tk.Button(login_frame, text="Sign Up", command=switch_to_signup)

login_welcome_label.pack()

login_username_label.pack()
login_username_entry.pack()
login_password_label.pack()
login_password_entry.pack()
login_button.pack()
signup_button.pack()

# Signup Frame
signup_frame = tk.Frame(root)
signup_welcome_label = tk.Label(signup_frame, text="Lets Create an account for you", font=("Arial", 14))
signup_username_label = tk.Label(signup_frame, text="Username:")
signup_username_entry = tk.Entry(signup_frame)
signup_password_label = tk.Label(signup_frame, text="Password:")
signup_password_entry = tk.Entry(signup_frame, show="*")
confirm_password_label = tk.Label(signup_frame, text="Confirm Password:")
confirm_password_entry = tk.Entry(signup_frame, show="*")
create_user_button = tk.Button(signup_frame, text="Create User", command=create_user)

login_button_s = tk.Button(signup_frame, text="Back to Login", command=switch_to_login)

signup_welcome_label.pack()
signup_username_label.pack()
signup_username_entry.pack()
signup_password_label.pack()
signup_password_entry.pack()
confirm_password_label.pack()
confirm_password_entry.pack()
create_user_button.pack()
login_button_s.pack()



########################################################################################

cloud_page = tk.Frame(root)
button_frame=tk.Frame(cloud_page,width=500)
upload_button = tk.Button(button_frame, text="Upload", command=navigate_to_upload,height=20,width=30,font=('arial',14))
upload_button.pack(padx=110,side=tk.LEFT)

download_button = tk.Button(button_frame, text="Download", command=navigate_to_download,height=20,width=30,font=('arial',14))
download_button.pack(side=tk.LEFT)

download_frame = tk.Frame(root)
upload_frame = tk.Frame(root)

button_frame.pack(fill=tk.Y,side=tk.TOP,pady=250)
#########################################################################################
upload_contents_frame=tk.Frame(upload_frame)
text_box = tk.Text(upload_contents_frame, width=50, height=2)
text_box.pack()
# Create a "Browse" button
browse_button = tk.Button(upload_contents_frame, text="Browse", command=browse_file)
browse_button.pack()
# Create an "Upload" button
upload_button = tk.Button(upload_contents_frame, text="Upload", command=upload_file)
upload_button.pack()
upload_contents_frame.pack(pady=300)

#########################################################################################
files_listbox = tk.Listbox(download_frame, width=40, height=20)
files_listbox.pack(padx=10, pady=10)

download_button = tk.Button(download_frame, text="Download Selected", command=get_selected_file_name)
download_button.pack()

start_server_thread = Thread(target=start_server)
start_cloud_thread = Thread(target=start_cloud_client)
start_cloud_thread.start()
start_server_thread.start()

tk.mainloop()
