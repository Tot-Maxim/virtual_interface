#!/usr/bin/env python3
from tkinter import *
from socket import *
from struct import pack
import os


class ClientProtocol:

    def __init__(self):
        self.socket = None

    def connect(self, server_ip, server_port):
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.settimeout(3)
            self.socket.connect((server_ip, server_port))
        except:
            label.config(text="Connection timed out", fg='red')

    def close(self):
        self.socket.shutdown(SHUT_WR)
        self.socket.close()
        self.socket = None

    def send_image(self, image_data, file_name):
        # use struct to make sure
        length = pack('>Q', len(image_data))
        self.socket.sendall(length)
        lenname = pack('>Q', len(file_name))
        self.socket.sendall(lenname)

        self.socket.sendall(bytes(file_name.encode()))
        self.socket.sendall(image_data)
        label.config(text="Файл успешно отправлен", fg='white')
        ack = self.socket.recv(1)


def send_file():
    cp = ClientProtocol()
    file_copy = file_entry.get()
    if file_entry.get():
        path_label.config(text=f'Отправка файла {file_copy}', fg='white')
    else:
        path_label.config(text=f'Введите имя файла', fg='red')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_dir = os.path.join(current_dir, file_copy)


    image_data = None
    try:
        with open(path_dir, 'rb') as file:
            image_data = file.read()
        assert (len(image_data))
    except:
        path_label.config(text=f'Файл не найден', fg='red')

    address = address_entry.get()
    port = port_entry.get()
    if address_entry.get():
        label_addr.config(text=f'Ip-адрес: {address}', fg='white')
    else:
        label_addr.config(text=f'Введите IP-адрес', fg='red')
    if port_entry.get():
        label_port.config(text=f'TCP порт: {port}', fg='white')
    else:
        label_port.config(text=f'Введите TCP-порт', fg='red')

    cp.connect(address, int(port))
    cp.send_image(image_data, file_copy)
    cp.close()
    print('Отправка завершена')


def create_label(text='', row: int = 0, column: int = 0):
    item = Label(window, text=text, fg='white', bg='black')
    item.grid(row=row, column=column, padx=10, pady=(30, 10), sticky="w")
    return item


def create_entry(row: int = 0, column: int = 0, show=''):
    item = Entry(window, show=show)
    item.grid(row=row, column=column, padx=10, pady=(50, 10), sticky="ew")
    return item


window = Tk()
window.geometry("820x450")
window.title('TAP TAP')
window.config(background='black')

icon = PhotoImage(file='logo.png')
window.iconphoto(True, icon)

button_send = Button(window, text="Нажмите, чтобы отправить файл", command=send_file, bg='black', fg='white')
button_send.grid(row=0, column=0, padx=10, pady=10, sticky="ew")


path_label = create_label('Введите имя файла', 2, 1)
file_entry = create_entry(2, 0)
file_entry.insert(0, 'logo.png')

label_addr = create_label('Введите IP-адрес', 3, 1)
address_entry = create_entry(3, 0)
address_entry.insert(0, '10.1.1.8')

label_port = create_label('Введите порт', 4, 1)

port_entry = create_entry(4, 0)
port_entry.insert(0, '5050')

label = create_label('', 5, 0, )

window.mainloop()
