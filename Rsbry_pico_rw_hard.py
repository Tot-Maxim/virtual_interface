import select
from sys import stdin, stdout
from machine import UART, Pin

uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
led = Pin(25, Pin.OUT)

buffer_uart = bytearray()
buffer_stdin = bytearray()

while True:
    led.value(0)
    readable, writable, _ = select.select([uart, stdin], [uart, stdout], [])

    for fd in readable:
        if fd == uart:
            b = uart.read(1)
            if b:
                led.value(0)
                buffer_uart.append(ord(b))

        elif fd == stdin:
            b = stdin.buffer.read(1)
            if b:
                led.value(0)
                buffer_stdin.append(ord(b))

    for fd in writable:
        if fd == uart:
            if buffer_stdin:
                led.value(1)
                uart.write(buffer_stdin)
                buffer_stdin = bytearray()

        elif fd == stdout:
            if buffer_uart:
                led.value(1)
                stdout.buffer.write(buffer_uart)
                buffer_uart = bytearray()
