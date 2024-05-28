import serial
import time

size = 0
data_to_send = bytearray()
for i in range(3000):
    data_to_send.append(i % 256)

while True:
    port_write = '/dev/ttyACM0'
    baud_rate = 115200  # Specify the baud rate
    ser_write = serial.Serial(port_write, baud_rate)
    data = ser_write.write(data_to_send)
    size += data
    print(f'Write {size} to {port_write}')
    ser_write.close()


