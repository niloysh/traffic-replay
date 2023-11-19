#!/usr/bin/python
from scapy.all import *
from scapy.layers.inet import Ether, IP
import sys

packets = rdpcap(sys.argv[1])
interface = "eth0"

dst_mac = "08:92:04:dd:43:a9"
dst_ip = "129.97.168.100"
payload = "hello, world"

def rewrite_headers(packet):
    # Check if Ether layer is present
    if Ether in packet:
        packet[Ether].src = get_if_hwaddr(interface)
        del packet[Ether].dst
    else:
        packet = Ether(src=get_if_hwaddr(interface)) / packet

    # Check if IP layer is present
    if IP in packet:
        packet[IP].src = get_if_addr(interface)
        packet[IP].dst = dst_ip

    # Remove checksums for all layers so that Scapy recalculates it
    # Does recalculation of checksums for ICMP, UDP, and TCP
    for layer in packet.layers():
        if hasattr(packet[layer], "chksum"):
            packet[layer].chksum = None

    return packet


def replay_pcap(packets):
    for packet in packets:
        rewrite_headers(packet)
        sendp(packet, iface=interface)

replay_pcap(packets)
