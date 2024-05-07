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
        self.socket.connect((server_ip, server_port))

    def close(self):
        self.socket.shutdown(SHUT_WR)
        self.socket.close()
        self.socket = None

    def send_image(self, image_data):
        # use struct to make sure we have a consistent endianness on the length
        length = pack('>Q', len(image_data))

        # sendall to make sure it blocks if there's back-pressure on the socket
        self.socket.sendall(length)
        self.socket.sendall(image_data)
        label.config(text="Send file successful", fg='white')
        ack = self.socket.recv(1)


def run_shell_script():
    try:
        password = password_entry.get()
        command = f"echo {password} | sudo -S ./run.sh"
        rc = subprocess.Popen(command, shell=True)
        if password:
            label.config(text="Start sh file successful", fg='white')
        else:
            label.config(text="Input sudo password", fg='red')
    except Exception as e:
        label.config(text=f"Error: {e}", fg='red')


def send_file():
    cp = ClientProtocol()
    file_copy = file_entry.get()
    if file_entry.get():
        path_label.config(text=f'Sending file {file_copy}', fg='white')
    else:
        path_label.config(text=f'Input file name', fg='red')

    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_dir = os.path.join(current_dir, file_copy)

    image_data = None
    with open(path_dir, 'rb') as file:
        image_data = file.read()
    assert (len(image_data))

    address = address_entry.get()
    port = port_entry.get()
    if address_entry.get():
        label_addr.config(text=f'Ip address: {address}', fg='white')
    else:
        label_addr.config(text=f'Input IP address', fg='red')
    if port_entry.get():
        label_port.config(text=f'TCP port: {port}', fg='white')
    else:
        label_port.config(text=f'Input port TCP', fg='red')

    cp.connect(address, int(port))
    cp.send_image(image_data)
    cp.close()
    print('Send is over')


def create_label(text='', row: int = 0, column: int = 0):
    item = Label(window, text=text, fg='white', bg='black')
    item.grid(row=row, column=column, padx=10, pady=(30, 10), sticky="w")
    return item


def create_entry(row: int = 0, column: int = 0, show=''):
    item = Entry(window, show=show)
    item.grid(row=row, column=column, padx=10, pady=(30, 10), sticky="ew")
    return item


window = Tk()
window.geometry("820x450")
window.title('Test GUI program')
window.config(background='black')

icon = PhotoImage(file='logo.png')
window.iconphoto(True, icon)

button_connect = Button(window, text="Press to run sh", command=run_shell_script, bg='black', fg='white')
button_connect.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

button_send = Button(window, text="Press to send file", command=send_file, bg='black', fg='white')
button_send.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

create_label('Enter sudo password', 1, 1)
password_entry = create_entry(1, 0, '*')

path_label = create_label('Enter path to file', 2, 1)
file_entry = create_entry(2, 0)
file_entry.insert(0, 'logo.png')

label_addr = create_label('Enter IP address', 3, 1)
address_entry = create_entry(3, 0)
address_entry.insert(0, '10.1.1.7')

label_port = create_label('Enter port', 4, 1)

port_entry = create_entry(4, 0)
port_entry.insert(0, '5050')

label = create_label('', 5, 0, )

window.mainloop()
