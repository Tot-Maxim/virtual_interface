#!/usr/bin/env python3
import serial
import select

port_read = '/dev/ttyACM1'  # Specify the correct serial port name
baud_rate = 115200  # Specify the baud rate
ser_read = serial.Serial(port_read, baud_rate)
while True:
    read_tun, _, _ = select.select([ser_read], [], [], 0)

    if ser_read in read_tun:
        try:
            print("Reading data stream...")
            if ser_read.in_waiting > 0:
                data = ser_read.read(ser_read.in_waiting)
                print(data)

        except KeyboardInterrupt:
            ser_read.close()
            print('Serial port is closed')
