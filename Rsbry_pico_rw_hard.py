from sys import stdin, stdout
from machine import UART, Pin
import time
import select

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
led = Pin(25, Pin.OUT)

while True:
    try:
        readable, _, _ = select.select([uart, stdin], [], [])
        led.value(0)
        time.sleep(0.01)

        if uart in readable:
            led.value(1)
            data_from_uart = uart.read(1)
            stdout.buffer.write(data_from_uart)
            print('Write data: ', data_from_uart)

        if stdin in readable:
            led.value(1)
            data_from_std = stdin.buffer.read(1)
            uart.write(data_from_std)
            print('Read data: ', data_from_std)

    except KeyboardInterrupt:
        print("Program interrupted. Exiting...")
        break