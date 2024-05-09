import fcntl
import os
import struct
import subprocess
import time

temp_read = b''
file_from_virtual = 'from_virtual'
file_from_host = 'from_host'
DST_IP = '10.1.1.8'
SRC_IP = '10.1.1.7'


class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class TAP_Manager:
    def __init__(self):
        self.file_from_host = file_from_host
        self.file_from_virtual = file_from_virtual
        self.temp_read = temp_read
        self.src_ip = SRC_IP
        self.dst_ip = DST_IP
        self.tun_setup()

    def tun_setup(self):
        TUNSETIFF = 0x400454ca
        TUNSETOWNER = TUNSETIFF + 2
        IFF_TUN = 0x0001
        IFF_TAP = 0x0002
        IFF_NO_PI = 0x1000

        self.tun_in = open('/dev/net/tun', 'r+b', buffering=0)
        ifr = struct.pack('16sH', b'tap0', IFF_TAP | IFF_NO_PI)
        fcntl.ioctl(self.tun_in, TUNSETIFF, ifr)
        fcntl.ioctl(self.tun_in, TUNSETOWNER, 1000)
        subprocess.check_call(f'ifconfig tap0 {self.src_ip} pointopoint {self.dst_ip} up', shell=True)
        return self.tun_in

    def write_packet_to_file(self, packet, file_path):
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
            except:
                time.sleep(0.1)
                continue
            finally:
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)
                    return True
        return False

    def read_packet(self, path_dir):
        global temp_read

        if not os.path.exists(path_dir):
            print('Server not found')
            return True

        with open(path_dir, 'rb+') as file:
            content = file.read()
            index = content.find(b'\t0t')

            if index != -1:
                to_TCP = content[:index]
                after_content = content[index + 3:]

                if temp_read != to_TCP:
                    temp_read = to_TCP
                    print(bcolors.OKGREEN + f'Read_data in {path_dir}:' + bcolors.ENDC,
                          ''.join('{:02x} '.format(x) for x in to_TCP))
                    os.write(self.tun_in.fileno(), bytes(to_TCP))
                    return False
                else:
                    pass
                file.seek(0)
                file.truncate()
                file.write(after_content)
            else:
                return True
