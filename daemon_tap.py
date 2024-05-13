#!/usr/bin/env python3
from mytuntap import TAP_Manager
import threading
import argparse

parser = argparse.ArgumentParser(description='TAP Manager Script')
parser.add_argument('--current_dir', type=str, default='/home/oem/PycharmProjects/virtual_interface',
                    help='Current directory path')
parser.add_argument('--file_from_host', type=str, default='from_virtual', help='File from host')
parser.add_argument('--file_from_virtual', type=str, default='from_virtual', help='File from virtual')
parser.add_argument('--src_ip', type=str, default='10.1.1.7', help='Source IP address')
parser.add_argument('--dst_ip', type=str, default='10.1.1.8', help='Destination IP address')

args = parser.parse_args()
# CURRENT_DIR = '/home/tot/FilePack'
# CURRENT_DIR = '/home/oem/PycharmProjects/virtual_interface'

# Инициализация класса TAP_Manager
tap_manager = TAP_Manager(args.src_ip, args.dst_ip)
tap_lock = threading.Lock()

read_thread = threading.Thread(target=tap_manager.read_from_file,
                               args=(tap_lock, args.current_dir, args.file_from_virtual))
write_thread = threading.Thread(target=tap_manager.read_from_TCP, args=(tap_lock, args.current_dir,
                                                                        args.file_from_host))

read_thread.start()
write_thread.start()
