#!/bin/bash
cd http_file/
gnome-terminal --geometry=200x24 --title="HOST TAP MANAGER" -- bash -c "python3 http-serv-tes.py; exec bash"