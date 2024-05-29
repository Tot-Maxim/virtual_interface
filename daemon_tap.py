#!/usr/bin/env python3
from mytuntap import TAP_Manager
import select
import argparse
import serial
import os

# CURRENT_DIR_TOT = '/home/tot/FilePack'
# CURRENT_DIR_OEM = '/home/oem/PycharmProjects/virtual_interface'
parser = argparse.ArgumentParser(description='TAP Manager Script')
parser.add_argument('--serial_port', type=str, default='/dev/ttyACM0', help='Serial port to pico')
parser.add_argument('--baud_rate', type=int, default=115200, help='baud_rate for serial port')
parser.add_argument('--src_ip', type=str, default='10.1.1.7', help='Source IP address')
parser.add_argument('--dst_ip', type=str, default='10.1.1.8', help='Destination IP address')
args = parser.parse_args()

tap_manager = TAP_Manager(args.src_ip, args.dst_ip, args.serial_port,
                          args.baud_rate)  # Инициализация класса TAP_Manager
tun = tap_manager.tun_setup()  # Инициализация tap интерфейса
ser = serial.Serial(args.serial_port, args.baud_rate)


class Bcolors:  # Класс с константами для цветовой кодировки в консоли
    WARNING = '\033[93m'
    ENDC = '\033[0m'


while True:
    read_tun, write_tun, _ = select.select([tun.fileno(), ser], [], [], 0)

    if tun.fileno() in read_tun:
        tap_manager.read_from_tcp()

    # if ser in read_tun:
    #     #tap_manager.read_from_serial()
    #     try:
    #         if ser.in_waiting > 0:
    #             data = ser.read(ser.in_waiting)
    #             print(Bcolors.WARNING + f'Прочитанные данные из {args.serial_port}:' + Bcolors.ENDC,
    #                   ' '.join('{:02x}'.format(x) for x in data))
    #
    #     except KeyboardInterrupt:
    #         ser.close()
    #         print('Serial port is closed')
