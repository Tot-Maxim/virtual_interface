import  socket

Server_HOST = ('192.168.56.101')

Server_PORT = 6060

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((Server_HOST, Server_PORT))

message = 'Hello, server!'
client_socket.sendall(message.encode())

recived_data = client_socket.recv(1024)
print(f'Recived from server: {recived_data.decode()}')
client_socket.close()