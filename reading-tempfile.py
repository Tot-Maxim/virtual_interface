import os
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
path_dir = os.path.join(current_dir, 'from_host.docx')


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def read_packet(path_dir):
    with open(path_dir, 'rb+') as file:
        content = file.read()
        index = content.find(b'\tot')

        if index != -1:
            to_TCP = content[:index]
            content = content[index + 3:]
            print(bcolors.OKGREEN + f'Read_data in {path_dir}:' + bcolors.ENDC, ''.join('{:02x} '.format(x) for x in to_TCP))
            file.seek(0)
            file.truncate()
            file.write(content)
            return to_TCP
    return False


while True:
    to_TCP = read_packet(path_dir)
    if to_TCP:
        print(to_TCP)
    else:
        time.sleep(0.3)