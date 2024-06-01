# Прошивка для платы Raspberry Pi Pico
import select
from sys import stdin, stdout
from machine import UART, Pin

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
led = Pin(25, Pin.OUT)
p = select.poll()
p.register(uart, select.POLLIN | select.POLLOUT)
p.register(stdin, select.POLLIN)
p.register(stdout, select.POLLOUT)

buffer_std = bytearray()
buffer_uart = bytearray()

while True:
    events = p.poll()
    for fd, event in events:
        if fd == uart:
            if event & select.POLLIN:
                led.value(0)
                b = ord(uart.read(1))
                buffer_uart.append(b)

            if event & select.POLLOUT:
                if buffer_std:
                    uart.write(buffer_std)
                    buffer_std = bytearray()

        if fd == stdin:
            if event & select.POLLIN:
                led.value(1)
                b = ord(stdin.buffer.read(1))
                buffer_std.append(b)

        if fd == stdout:
            if event & select.POLLOUT:
                if buffer_uart:
                    stdout.buffer.write(buffer_uart)
                    buffer_uart = bytearray()
