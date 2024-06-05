#!/usr/bin/env python3
from mytuntap import TAP_Manager  # Импорт класса TAP_Manager из mytuntap
import select
import argparse

parser = argparse.ArgumentParser(description='TAP Manager Script')
parser.add_argument('--serial_port', type=str, default='/dev/ttyACM0', help='Serial port to pico')
parser.add_argument('--baud_rate', type=int, default=115200, help='baud_rate for serial port')
parser.add_argument('--src_ip', type=str, default='10.1.1.7', help='Source IP address')
parser.add_argument('--dst_ip', type=str, default='10.1.1.8', help='Destination IP address')
args = parser.parse_args()

tap_manager = TAP_Manager(args.src_ip, args.dst_ip, args.serial_port,
                          args.baud_rate)  # Инициализация класса TAP_Manager
tun = tap_manager.tun_setup()  # Инициализация tap интерфейса
ser = tap_manager.serial_setup()  # Инициализация последовательного порта


class Bcolors:  # Класс с константами для цветовой кодировки в консоли
    WARNING = '\033[93m'
    ENDC = '\033[0m'


# Буферы для данных TCP и UART
buffer_tcp = bytearray()
buffer_uart = bytearray()

while True:
    readable, writable, _ = select.select([tun.fileno(), ser.fileno()], [tun.fileno(), ser.fileno()], [], 0)

    for fd in readable:
        if fd == tun.fileno():   # Если доступны данные с tap-интерфейса
            bt = tap_manager.read_from_tcp()
            if bt:
                buffer_tcp.extend(bt)  # Добавляем данные в буфер buffer_tcp

        elif fd == ser.fileno():  # Если доступны данные с серийного порта
            bu = tap_manager.read_from_serial()
            if bu:
                buffer_uart.extend(bu)  # Добавляем данные в буфер buffer_uart

    for fd in writable:
        if fd == tun.fileno():  # Если возможна запись в tap-интерфейс
            if buffer_uart:
                tap_manager.write_to_tcp(buffer_uart)  # Записываем данные из буфера buffer_uart
                buffer_uart.clear()  # Очищаем буфер buffer_uart

        elif fd == ser.fileno():  # Если возможна запись в серийный порт
            if buffer_tcp:
                tap_manager.write_to_uart(buffer_tcp)  # Записываем данные из буфера buffer_tcp
                buffer_tcp.clear()  # Очищаем буфер buffer_tcp
