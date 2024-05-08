import os
from socket import *
from struct import unpack

ip_address = '10.1.1.7'
TCP_port = 5050
class ServerProtocol:

    def __init__(self):
        self.socket = None
        self.output_dir = '.'
        self.file_num = 1

    def listen(self, server_ip, server_port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((server_ip, server_port))
        self.socket.listen(1)

    def handle_images(self):

        try:
            while True:
                (connection, addr) = self.socket.accept()
                try:
                    bs = connection.recv(8)
                    (length,) = unpack('>Q', bs)
                    data = b''
                    while len(data) < length:
                        to_read = length - len(data)
                        data += connection.recv(
                            4096 if to_read > 4096 else to_read)
                    print(f'Receive data : {data}')

                    # send our 0 ack
                    assert len(b'\00') == 1
                    connection.sendall(b'\00')
                finally:
                    connection.shutdown(SHUT_WR)
                    connection.close()

                with open(os.path.join(
                        self.output_dir, 'Copy_' + '%02d.png' % self.file_num), 'wb'
                ) as fp:
                    fp.write(data)
                    print('File write success')

                self.file_num += 1
        finally:
            self.close()

    def close(self):
        self.socket.close()
        self.socket = None


if __name__ == '__main__':
    print('START SERVER')

    sp = ServerProtocol()
    print(f'Server try listen {ip_address, TCP_port}')
    sp.listen(ip_address, TCP_port)

    sp.handle_images()