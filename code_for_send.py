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

state = 1
temp_read = b''

current_dir = os.path.dirname(os.path.abspath(__file__))
#current_dir = '/home/tot/FilePack'

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
    lock_file_path = file_path + '.lock'

    for _ in range(2):
        try:
            with open(lock_file_path, 'w') as lock_file:
                fcntl.flock(lock_file, fcntl.LOCK_EX)  # Acquire an exclusive lock on the lock file

                with open(file_path, 'ab+') as file:
                    file.write(packet)
                    file.write(b'\t0t')
                    print(bcolors.WARNING + f'Write data in {file_path}: ' + bcolors.ENDC,
                          ''.join('{:02x} '.format(x) for x in packet))
                fcntl.flock(lock_file, fcntl.LOCK_UN)  # Release the lock on the lock file
        except Exception as e:
            time.sleep(0.1)
            print(f"Failed to write to file: {e}. Retrying...")
            continue
        finally:
            if os.path.exists(lock_file_path):
                os.remove(lock_file_path)
                return True
    return False


def read_packet(path_dir):
    global temp_read
    with open(path_dir, 'rb+') as file:
        content = file.read()
        index = content.find(b'\t0t')

        if index != -1:
            to_TCP = content[:index]
            content = content[index + 3:]

            if temp_read != to_TCP:
                temp_read = to_TCP
                print(bcolors.OKGREEN + f'Read_data in {path_dir}:' + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in to_TCP))
                return to_TCP
            else:
                pass
            file.seek(0)
            file.truncate()
            file.write(content)


while True:
    print('1', state)
    if state == 1:
        from_TCP = array('B', os.read(tun.fileno(), 2048))
        if from_TCP:
            state = 2
            print(bytes(from_TCP))
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

tun.close()

