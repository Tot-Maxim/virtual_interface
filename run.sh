#!/bin/bash

gnome-terminal --geometry=200x24 --title="Code for send" -- bash -c "sudo python3 code_for_send.py; exec bash"
gnome-terminal --geometry=100x24 --title="Server" -- bash -c "sudo python3 server.py; exec bash"
gnome-terminal --geometry=100x24 --title="Client" -- bash -c "sudo python3 client.py; exec bash"