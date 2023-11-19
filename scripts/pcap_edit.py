import argparse
from scapy.all import *
from scapy.layers.inet import Ether, IP, fragment
import time


def get_args():
    parser = argparse.ArgumentParser(description="Edit pcap for replay. Modifies L2 and L3 headers.")
    parser.add_argument("interface", help="Name of interface which will be used to replay the pcap.")
    parser.add_argument("input_pcap", help="Path to pcap file.")
    parser.add_argument("output_pcap", help="Path to output pcap file.")
    parser.add_argument("--dst_ip", default="129.97.168.100", help="Destination IP address (default: 129.97.168.100)")
    parser.add_argument("--dry-run", action="store_true", help="Process only the first 50 packets")
    return parser.parse_args()

def rewrite_headers(packet, interface, dst_ip):
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

def process_pcap(input_file, output_file, interface, dst_ip, dry_run=False):
    packets = PcapReader(input_file)
    pcap_out = PcapWriter(output_file, append=True)
    count = 0
    start = time.time()
    for packet in packets:
        timestamp = packet.time
        modified_packet = rewrite_headers(packet, interface, dst_ip)
        modified_packet.time = timestamp

        # fragment large packets > MTU size
        fragments = fragment(modified_packet, fragsize=1400)
        for frag in fragments:
            pcap_out.write(frag)
        count += 1

        now = time.time()
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(now - start))

        if dry_run and count >= 50:
            print(f"Processed packets: {count} | Elapsed time (HH:MM:SS): {elapsed_time}")
            break

        if count % 500 == 0:
            print(f"Processed packets: {count}  | Elapsed time (HH:MM:SS): {elapsed_time}")

    pcap_out.close()

if __name__ == "__main__":
    args = get_args()
    process_pcap(args.input_pcap, args.output_pcap, args.interface, args.dst_ip, dry_run=args.dry_run)
