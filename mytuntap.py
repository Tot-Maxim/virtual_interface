import fcntl
import os
import struct
import subprocess
import serial


class Bcolors:  # Класс с константами для цветовой кодировки в консоли
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class TAP_Manager:
    def __init__(self, src_ip, dst_ip, port_read, baud_rate):  # Инициализируем значения переменных
        self.tun_in = None
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.serial_port = port_read
        self.baud_rate = baud_rate
        self.tun_setup()

    def tun_setup(self):
        # Коды для настройки интерфейса
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

    def read_from_tcp(self):
        try:
            from_tcp = os.read(self.tun_in.fileno(), 2048)
        except OSError as e:
            print(Bcolors.FAIL + f"Ошибка при записи в tap интерфейс: {e}" + Bcolors.ENDC)
        else:
            ser_write = serial.Serial(self.serial_port, self.baud_rate)
            ser_write.write(from_tcp)
            print(Bcolors.OKGREEN + f'Записанные данные в {self.serial_port}:' + Bcolors.ENDC,
                  ' '.join('{:02x}'.format(x) for x in from_tcp))
            ser_write.close()

    def read_from_serial(self):
        try:
            content = b''
            with serial.Serial(self.serial_port, self.baud_rate, timeout=1) as ser_read:
                while ser_read.in_waiting > 0:
                    content += ser_read.read(ser_read.in_waiting)

                print(Bcolors.WARNING + f'Прочитанные данные из {self.serial_port}:' + Bcolors.ENDC,
                      ' '.join('{:02x}'.format(x) for x in content))
                os.write(self.tun_in.fileno(), bytes(content))
        except Exception as e:
            pass
            #print(f"An error occurred: {e}")
