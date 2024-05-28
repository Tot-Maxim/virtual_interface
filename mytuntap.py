import fcntl
import os
import struct
import subprocess
import serial

#port_read = '/dev/ttyACM0'  # Specify the correct serial port name
baud_rate = 115200  # Specify the baud rate


class Bcolors:  # Класс с константами для цветовой кодировки в консоли
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class TAP_Manager:
    def __init__(self, src_ip, dst_ip, port_read):  # Инициализируем значения переменных
        self.tun_in = None
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.serial_port = port_read
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
            ser_write = serial.Serial(self.serial_port, baud_rate)
            data = ser_write.write(from_tcp)
            print(f'Write {data} to {self.serial_port}')
            ser_write.close()



    def read_from_serial(self):
        ser_read = serial.Serial(self.serial_port, baud_rate)

        try:
            print("Reading data stream...")
            while True:
                if ser_read.in_waiting == 0:
                    continue
                content = ser_read.read(ser_read.in_waiting)
                try:
                    print(Bcolors.WARNING + f'Прочитанные данные из {self.serial_port}:' + Bcolors.ENDC,
                          ' '.join('{:02x}'.format(x) for x in content))
                    os.write(self.tun_in.fileno(), bytes(content))
                except OSError as e:
                    print(Bcolors.FAIL + f"Ошибка при прочтении tap интерфейса: {e}" + Bcolors.ENDC)

        except KeyboardInterrupt:
            ser_read.close()
            print('Serial port is closed')

        except Exception as e:
            print(f"Error: {e}")


