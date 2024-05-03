from scapy.all import *
from array import array
import fcntl
import os
import struct
import subprocess
import time
import argparse

# Server information
server_ip = '192.168.1.1'  # Update with the server's IP address
server_port = 5050  # Update with the server's port number

parser = argparse.ArgumentParser(description='Process file types list.')
parser.add_argument('--IP-dst', type=str, default='192.168.1.1', help='IP address. Default 192.168.1.1')
parser.add_argument('--Eth-dst', type=str, default='0a:1a:de:3c:f0:5d', help='Ether address. Default 0a:1a:de:3c:f0:5d')
parser.add_argument('--TCP-port', type=int, default=12345, help='input TCP port')
args = parser.parse_args()
IP_dst = args.IP_dst
Eth_dst = args.Eth_dst
TCP_port = args.TCP_port
Test_text = 'Hello world'

# Некоторые константы, используемые для ioctl файла устройства. Я получил их с помощью простой программы на Cи
TUNSETIFF = 0x400454ca
TUNSETOWNER = TUNSETIFF + 2
IFF_TUN = 0x0001
IFF_TAP = 0x0002
IFF_NO_PI = 0x1000

# Открытие файла, соответствующего устройству TUN, в двоичном режиме чтения/записи без буферизации.
tun = open('/dev/net/tun', 'r+b', buffering=0)
ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
fcntl.ioctl(tun, TUNSETIFF, ifr)
fcntl.ioctl(tun, TUNSETOWNER, 1000)

# Поднятие tap0 и назначение адреса
subprocess.check_call('ifconfig tap0 192.168.1.1 pointopoint 192.168.1.1 up', shell=True)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    for _ in range(3):
        client_socket.connect((server_ip, server_port))

        while True:
            Test_text = input('Enter the text to send to the interface:\n')

            # packet = array('B', os.read(tun.fileno(), 2048))
            #current_dir = os.path.dirname(os.path.abspath(__file__))
            #path_dir = os.path.join(current_dir, 'data_file.txt')
            #with open(path_dir, 'rb') as file:
            #    packet = file.read()

            # Вывод содержимое массива пакетов после операции чтения
            #print("raw_read_data:", ''.join('{:02x} '.format(x) for x in packet))

            hex_data = '0a1ade3cf05d0a1ade3cf05d08004500003d000100004006f7ffc0a80101c0a80101d4313039000000000000000005002200d146000054657374207465c8a020666f72206578616d706c65'

            # Convert the hexadecimal data to bytes
            packet_data = bytes.fromhex(hex_data)

            # Print the binary representation of the packet
            print(packet_data)

            # Extract relevant information about the packet
            source_port, destination_port = struct.unpack('!HH', packet_data[20:24])

            print(f"Source Port: {source_port}")
            print(f"Destination Port: {destination_port}")

            current_dir = '/home/tot/FilePack'
            path_dir = os.path.join(current_dir, 'data_file.txt')
            with open(path_dir, 'wb') as file:
                file.write(bytes(packet))

            # Send the data to the server
            client_socket.sendall(packet)

            # Receive response from the server
            server_response = client_socket.recv(1024).decode()
            print(f"Server response: {server_response}")

except ConnectionRefusedError:
    print("Connection to the server refused. Make sure the server is running.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the socket connection and TAP interface
    client_socket.close()
    tun.close()

