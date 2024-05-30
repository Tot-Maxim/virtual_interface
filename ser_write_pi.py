#!/usr/bin/env python3
import serial
import time
import base64

size_tx = 0
size_rx = 0
size_array = 1000
data_to_send = bytearray(size_array)

for i in range(size_array):
    data_to_send[i] = i % 256

port_write = '/dev/ttyACM0'
baud_rate = 115200


def add_padding(data):
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'=' * (4 - missing_padding)
    return data


while True:
    with serial.Serial(port_write, baud_rate) as ser_read:
        send_base64 = base64.b64encode(data_to_send)
        len_tx = ser_read.write(send_base64)
        size_tx += len_tx
        ts = (10 / baud_rate) * (len_tx + 50) * 5
        time.sleep(ts)

        len_rx = ser_read.in_waiting
        data_rx = ser_read.read(len_rx)
        receive_base64 = base64.b64decode(add_padding(data_rx))
        size_rx += len_rx
        if send_base64 != data_rx:
            print('Write ', send_base64)
            print('Read  ', data_rx)
            size_tx, size_rx = 0, 0
        else:
            print('OK')
