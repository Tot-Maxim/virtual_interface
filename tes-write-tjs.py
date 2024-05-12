from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP
from scapy.packet import Raw

packets = []
packet = (Ether(dst="0a:1a:de:3c:f0:5d", src="0a:1a:de:3c:f0:5d") / IP(dst="10.1.1.8", src="10.1.1.7") /
          TCP(dport=5050, sport=5050) / Raw(load='Test text for example'))

# Отправка пакета на интерфейс TAP
sendp(packet, iface="tap0")
