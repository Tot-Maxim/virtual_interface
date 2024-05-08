from tkinter import *
import subprocess
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

    def send_image(self, image_data):
        # use struct to make sure
        length = pack('>Q', len(image_data))

        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(image_data)
        label.config(text="Файл успешно отправлен", fg='white')
        ack = self.socket.recv(1)


def run_shell_script():
    try:
        password = password_entry.get()
        command = f"echo {password} | sudo -S ./run.sh"
        rc = subprocess.Popen(command, shell=True)
        if password:
            label.config(text="Запуск tap интерфейса", fg='white')
        else:
            label.config(text="Введите пароль ОС", fg='red')
    except Exception as e:
        label.config(text=f"Ошибка: {e}", fg='red')


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
    cp.send_image(image_data)
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

button_connect = Button(window, text="Нажмите, чтобы запустить tap", command=run_shell_script, bg='black', fg='white')
button_connect.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

button_send = Button(window, text="Нажмите, чтобы отправить файл", command=send_file, bg='black', fg='white')
button_send.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

create_label('Введите пароль', 1, 1)
password_entry = create_entry(1, 0, '*')

path_label = create_label('Введите имя файла', 2, 1)
file_entry = create_entry(2, 0)
file_entry.insert(0, 'logo.png')

label_addr = create_label('Введите IP-адрес', 3, 1)
address_entry = create_entry(3, 0)
address_entry.insert(0, '10.1.1.7')

label_port = create_label('Введите порт', 4, 1)

port_entry = create_entry(4, 0)
port_entry.insert(0, '5050')

label = create_label('', 5, 0, )

window.mainloop()
