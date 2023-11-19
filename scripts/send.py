#!/usr/bin/python
from scapy.layers.inet import Ether, IP, UDP, TCP, fragment
from scapy.utils import rdpcap
from scapy.layers.l2 import get_if_hwaddr, get_if_addr
from scapy.all import send, sendp, sendpfast


interface = "eth0"

dst_mac = "08:92:04:dd:43:a9"
next_mac = "86:99:e1:f3:83:fd"
dst_ip = "129.97.168.100"
payload = "hello, world"


pkt = (
    Ether(src=get_if_hwaddr(interface))
    / IP(dst=dst_ip)
    / UDP(sport=8001, dport=8002)
    / payload
)

pkt.show2()
sendp(pkt, iface=interface)

