import socket
import subprocess

subprocess.check_call('ip tuntap add tap0 mode tap', shell=True)
subprocess.check_call('ip link set tap0 up', shell=True)
subprocess.check_call('ip addr add 192.168.1.1/255.255.255.0 dev tap0', shell=True)

# Server configuration
server_ip = '192.168.1.1'  # Server listens on all available network interfaces
server_port = 5050

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the server address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(5)  # Up to 5 connections can wait in the connection queue

print(f"Server is listening on {server_ip}:{server_port}...")

while True:
    # Accept a new connection
    client_socket, client_address = server_socket.accept()

    print(f"Connection established with {client_address}")

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break  # Break the loop if no more data is received

            print(f"Received data from client: {data}")

            # Process the received data (if needed)

            # Send a response back to the client
            response = "Data received by the server."
            client_socket.sendall(response.encode())
    except ConnectionResetError:
        print("Connection reset by the client.")
    finally:
        # Close the client socket
        client_socket.close()

# Close the server socket
server_socket.close()