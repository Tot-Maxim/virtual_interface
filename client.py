from socket import *
from struct import pack


class ClientProtocol:

    def __init__(self):
        self.socket = None

    def connect(self, server_ip, server_port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((server_ip, server_port))

    def close(self):
        self.socket.shutdown(SHUT_WR)
        self.socket.close()
        self.socket = None

    def send_image(self, image_data):

        # use struct to make sure we have a consistent endianness on the length
        length = pack('>Q', len(image_data))

        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(image_data)

        ack = self.socket.recv(1)


if __name__ == '__main__':
    Test_text = input('Enter the text to send to the interface:\n')
    print('START CLIENT')
    cp = ClientProtocol()

    image_data = None
    with open('logo.png', 'rb') as file:
        image_data = file.read()

    assert(len(image_data))
    cp.connect('10.1.1.7', 5050)
    cp.send_image(image_data)
    cp.close()