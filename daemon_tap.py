from mytuntap import TAP_Manager
import threading


CURRENT_DIR = '/home/tot/FilePack'
FILE_FROM_HOST = 'from_host'
FILE_FROM_VIRTUAL = 'from_virtual'

# Инициализация класса TAP_Manager
tap_manager = TAP_Manager()
tap_lock = threading.Lock()

read_thread = threading.Thread(target=tap_manager.read_from_file, args=(tap_lock, CURRENT_DIR, FILE_FROM_VIRTUAL))
write_thread = threading.Thread(target=tap_manager.read_from_TCP, args=(tap_lock, CURRENT_DIR, FILE_FROM_HOST))

read_thread.start()
write_thread.start()
