import socket
import os
import time

# Server information
server_ip = '10.1.1.8'  # Update with the server's IP address
server_port = 5050  # Update with the server's port number
# Client code to send data to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def read_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        hex_array_in_str = ''.join([format(byte, '02x') for byte in content])
        print(content)
        print(len(content))
    return hex_array_in_str

try:
    for _ in range(3):
        client_socket.connect((server_ip, server_port))

        while True:
            Test_text = input('Enter the text to send to the interface:\n')
            current_dir = os.path.dirname(os.path.abspath(__file__))
            path_dir = os.path.join(current_dir, 'logo.png')
            byte_text = read_file(path_dir)
            path_dir_logo = os.path.join(current_dir, 'logo_rec.png')
            byte_text_logo = read_file(path_dir_logo)

            if byte_text:# Send the data to the server
                client_socket.sendall(byte_text.encode())
                #server_response = client_socket.recv(1024).decode('utf-8')
                print("\nServer response")
            client_socket.close()

except ConnectionRefusedError:
    print("Connection to the server refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the socket connection and TAP interface
    client_socket.close()
