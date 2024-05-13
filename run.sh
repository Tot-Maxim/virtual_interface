#!/bin/bash

gnome-terminal --geometry=200x24 --title="Daemon for 10.1.1.7" -- bash -c "sudo python3 daemon_tap.py --src_ip 10.1.1.7 --dst_ip 10.1.1.8 ; exec bash"
#gnome-terminal --geometry=100x24 --title="Server" -- bash -c "sudo python3 server.py; exec bash"