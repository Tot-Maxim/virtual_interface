#!/usr/bin/env python3
from mytuntap import TAP_Manager
import select
import argparse
import serial

# CURRENT_DIR_TOT = '/home/tot/FilePack'
# CURRENT_DIR_OEM = '/home/oem/PycharmProjects/virtual_interface'
parser = argparse.ArgumentParser(description='TAP Manager Script')
parser.add_argument('--current_dir', type=str, default='/home/tot/FilePack',
                    help='Shared folder path')
parser.add_argument('--serial_port', type=str, default='/dev/ttyACM0', help='Serial port to pico')
parser.add_argument('--baud_rate', type=int, default=115200, help='baud_rate for serial port')
parser.add_argument('--src_ip', type=str, default='10.1.1.7', help='Source IP address')
parser.add_argument('--dst_ip', type=str, default='10.1.1.8', help='Destination IP address')
args = parser.parse_args()

tap_manager = TAP_Manager(args.src_ip, args.dst_ip, '/dev/ttyACM0')  # Инициализация класса TAP_Manager
tun = tap_manager.tun_setup()  # Инициализация tap интерфейса
ser = serial.Serial(args.serial_port, args.baud_rate)

while True:
    read_tun, _, _ = select.select([tun.fileno(), ser], [], [], 0)
    if tun.fileno() in read_tun:
        tap_manager.read_from_tcp()

    if ser in read_tun:
        tap_manager.read_from_serial()

