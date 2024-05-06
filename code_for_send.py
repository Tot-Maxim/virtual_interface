from array import array
import fcntl
import os
import struct
import subprocess
import time
import tempfile
import signal

def signal_handler(sig, frame):
    try:
        print('CTRL + C detected. Exiting gracefully...')
        tun.close()
        exit(0)
    except:
        pass

# Заданные переменные
source_port = 0x0a1a
destination_port = 0xde3c
sequence_number = 0xf05d0a1a
acknowledgment_number = 0xde3cf05d
flags = 0x800
checksum = 0x6f7

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
subprocess.check_call('ifconfig tap0 10.1.1.7 pointopoint 10.1.1.8 up', shell=True)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class AtomicWrite():
    def __init__(self, path, mode='w', encoding='utf-8'):
        self.path = path
        self.mode = mode if mode == 'wb' else 'w'
        self.encoding = encoding

    def __enter__(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            mode=self.mode,
            encoding=self.encoding if self.mode != 'wb' else None,
            delete=False
        )
        return self.temp_file

    def __exit__(self, exc_type, exc_message, traceback):
        self.temp_file.close()
        if exc_type is None:
            os.rename(self.temp_file.name, self.path)
            os.chmod(self.path, 0o664)
        else:
            os.unlink(self.temp_file.name)
            print(bcolors.FAIL + "Break")


def read_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        hex_array_in_str = ''.join([format(byte, '02x') for byte in content])
        print(hex_array_in_str)
    return hex_array_in_str


def write_packet_to_file(packet, file_path):
    directory = os.path.dirname(file_path)
    flag_file = os.path.join(directory, 'flag_to_vb.txt')

    if not os.path.exists(flag_file):
        try:
            with AtomicWrite(file_path, 'wb') as file:
                for x in packet:
                    file.write(bytes([x]))
                # Вывод содержимого массива пакетов после операции записи
                print(bcolors.WARNING + "raw_write_data:" + bcolors.ENDC,
                      ''.join('{:02x} '.format(x) for x in TCP_packet))

            # Создаем файл-флаг после успешной записи
            open(flag_file, 'w').close()
        except Exception as e:
            print(bcolors.FAIL + "Failed to write data. Retrying in 0.1 seconds...")
            time.sleep(0.1)
    else:
        pass



def read_packet_to_file(path_dir):
    directory = os.path.dirname(path_dir)
    flag_file = os.path.join(directory, 'flag_to_host.txt')

    if os.path.exists(flag_file):
        os.remove(flag_file)
        with open(path_dir, 'rb') as file:
            packet = file.read()
            os.write(tun.fileno(), bytes(packet))
            print(bcolors.OKGREEN + "raw_read_data:" + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in packet))
        return packet
    else:
        print(bcolors.FAIL + "Flag file does not exist. Skipping reading.")
        return None


def construct_tcp_packet(source_port, destination_port, sequence_number, acknowledgment_number, flags, checksum, data_body):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_dir = os.path.join(current_dir, 'logo.png')

    data_head = "13BA13BA000000000000000050022000d1460000"
    #data_body = read_file(path_dir)
    data = data_head + data_body.encode().hex()

    # Construct the TCP packet in array format
    packet = array('B', [
        (source_port >> 8) & 0xff, source_port & 0xff,
        (destination_port >> 8) & 0xff, destination_port & 0xff,
        (sequence_number >> 24) & 0xff, (sequence_number >> 16) & 0xff, (sequence_number >> 8) & 0xff,
        sequence_number & 0xff,
        (acknowledgment_number >> 24) & 0xff, (acknowledgment_number >> 16) & 0xff, (acknowledgment_number >> 8) & 0xff,
        acknowledgment_number & 0xff,
        (flags >> 8) & 0xff, flags & 0xff,
        69, 0,  # Total Length
        0x00, 0x3d,  # Identification
        0x00, 0x01,  # Flags and Protocol
        0x00, 0x00,  # Fragment Offset
        0x40,  # Time to Live
        (checksum >> 8) & 0xff, checksum & 0xff,
        0xff,
        0xa, 0x01, 0x01, 0x07,  # Source IP Address
        0xa, 0x01, 0x01, 0x08,  # Destination IP Address
    ])

    packet.extend(bytes.fromhex(data))

    return packet

last_read_time = 0
while True:
    #Test_data = input('Enter the text to send to the interface:\n')


    current_dir = os.path.dirname(os.path.abspath(__file__))
    # current_dir = '/home/tot/FilePack'
    path_dir = os.path.join(current_dir, 'data_file_from_vb_to_host.txt')
    current_time = os.path.getmtime(path_dir)

    if current_time != last_read_time:
        last_read_time = current_time
        packet = read_packet_to_file(path_dir)
    else:
        TCP_packet = array('B', os.read(tun.fileno(), 2048))
        path_dir = os.path.join(current_dir, 'data_file.txt')
        write_packet_to_file(TCP_packet, path_dir)
    # TCP_packet = construct_tcp_packet(source_port, destination_port, sequence_number, acknowledgment_number, flags, checksum, Test_data)


    time.sleep(0.2)
tun.close()

