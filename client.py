import socket
import fcntl
import os
import struct
import subprocess
import time

# Server information
server_ip = '127.0.0.1'  # Update with the server's IP address
server_port = 12345  # Update with the server's port number

# Open TAP interface
TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

tap = open('/dev/net/tun', 'r+b', buffering=0)
ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
fcntl.ioctl(tap, TUNSETIFF, ifr)
fcntl.ioctl(tap, TUNSETOWNER, 1000)

# Bring up the TAP interface and assign IP addresses
subprocess.check_call('ifconfig tap0 192.168.1.2 pointopoint 192.168.1.1 up', shell=True)

# Client code to send data to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((server_ip, server_port))

    while True:
        # Read data from the TAP interface
        packet = os.read(tap.fileno(), 2048)
        print('Packet read from TAP interface:', packet)

        # Send the data to the server
        client_socket.sendall(packet)

        # Receive response from the server
        server_response = client_socket.recv(1024).decode()
        print(f"Server response: {server_response}")

        time.sleep(0.5)

except ConnectionRefusedError:
    print("Connection to the server refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the socket connection and TAP interface
    client_socket.close()
    tap.close()