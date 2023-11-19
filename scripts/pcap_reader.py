"""
Read pcap. This script loads the entire pcap into memory. Use it for small pcaps only.
"""
import sys
from scapy.all import *
packets = rdpcap(sys.argv[1])
packets.summary()
