#!/usr/bin/env python3
import serial
import time


size_tx = 0
size_rx = 0
data_to_send = bytearray('*Text test*', 'ascii')

while True:
    port_write = '/dev/ttyACM1'
    baud_rate = 115200  # Specify the baud rate
    ser = serial.Serial(port_write, baud_rate, timeout=0.02)
    len_tx = ser.write(data_to_send)
    size_tx += len_tx
    print(f'Write {size_tx} {data_to_send}')
    time.sleep(0.05)

    len_rx = ser.in_waiting
    data_rx = ser.read(len_rx)
    size_rx += len_rx
    print(f'Read {size_rx} {data_rx}')

    ser.close()




