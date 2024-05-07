from array import array
import fcntl
import os
import struct
import subprocess
import tempfile
import time

try:
    subprocess.check_call('sudo ip route delete 10.0.0.0/7 dev tap0 proto kernel scope link src 10.1.1.7', shell=True)
except:
    pass

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
state = 1

temp_read = b''

#current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = '/home/tot/FilePack'

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


def write_packet_to_file(packet, file_path):
    global state
    lock_file_path = file_path + '.lock'

    try_count = 0
    while try_count < 2:
        try:
            with open(lock_file_path, 'w') as lock_file:
                fcntl.flock(lock_file, fcntl.LOCK_EX)  # Acquire an exclusive lock on the lock file

                with open(file_path, 'wb') as file:
                    file.write(packet)
                    # Output the content of the packet array after the write operation
                    print(bcolors.WARNING + "raw_write_data:" + bcolors.ENDC,
                          ''.join('{:02x} '.format(x) for x in packet))
                fcntl.flock(lock_file, fcntl.LOCK_UN)  # Release the lock on the lock file
        except Exception as e:
            try_count += 1
            time.sleep(0.1)
            print(f"Failed to write to file: {e}. Retrying...")
            continue
        finally:
            if os.path.exists(lock_file_path):
                os.remove(lock_file_path)
                return True
    else:
        return False


def read_packet(path_dir):
    global temp_read
    with open(path_dir, 'rb') as file:
        to_TCP = file.read()
        if temp_read != to_TCP:
            temp_read = to_TCP
            print(bcolors.OKGREEN + "raw_read_data:" + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in to_TCP))
            return to_TCP
        else:
            pass


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


while True:
    #Test_data = input('Enter the text to send to the interface:\n')
    print('1', state)
    if state == 1:
        from_TCP = array('B', os.read(tun.fileno(), 2048))
        if from_TCP:
            state = 2
    print('2', state)
    if state == 2:
        path_dir = os.path.join(current_dir, 'from_host.docx')
        if write_packet_to_file(from_TCP, path_dir):
            state = 3
    print('3', state)
    if state == 3:
        path_dir = os.path.join(current_dir, 'from_virtual.docx')
        to_TCP = read_packet(path_dir)
        if to_TCP:
            state = 4
        else:
            state = 1
    print('4', state)
    if state == 4:
        os.write(tun.fileno(), bytes(to_TCP))
        state = 1
    time.sleep(0.3)


    # TCP_packet = construct_tcp_packet(source_port, destination_port, sequence_number, acknowledgment_number, flags, checksum, Test_data)

tun.close()

