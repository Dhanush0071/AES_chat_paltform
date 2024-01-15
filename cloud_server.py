import socket
import os
import mysql.connector

# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhanush5",
    database="crypto"
)
cursor = db.cursor()

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.126.34', 5555))  # Replace with your server IP and port
server_socket.listen(5)

print("Server is running...")

def handle_client(client_socket):
    # Authentication
    credentials = client_socket.recv(1024).decode().split(':')  # Assuming format "username:password"
    username, password = credentials[0], credentials[1]

    query = f"SELECT * FROM credentials WHERE username = '{username}' AND pwd = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()

    if user:
        client_socket.send("Authenticated".encode())
        # File upload
        file_name = client_socket.recv(1024).decode()
        file_data = client_socket.recv(1024)

        directory = f"cloud_files/{username}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(f"{directory}/{file_name}", 'wb') as file:
            file.write(file_data)
        print(f"File '{file_name}' uploaded for user '{username}'")
    else:
        client_socket.send("Authentication failed".encode())

while True:
    client_socket, addr = server_socket.accept()
    print(f"Accepted connection from {addr}")
    handle_client(client_socket)
    client_socket.close()
