##
# Experimental python implementation of some of the netScout statistics calculations
# Author: Elewout Vercaeren
# Released under GPL-3.0
#

import argparse
import sys
from scapy.all import *
import helpers


def main():

    # Read user arguments from the commandline
    parser = argparse.ArgumentParser(description='Calculate netScout subscriber session statistics')
    helpers.check_commandline_params(parser)
    args = parser.parse_args()

    # Get silence period
    silence_period = args.silence_period

    # Get minimum report time
    min_report_time = args.min_report_time

    # Get resolution time
    resolution_time = args.resolution_time

    # Get subscriber ip
    if helpers.is_ip_address(args.ip):
        subscriber_ip = args.ip
    else:
        sys.exit("ERROR: invalid ip address")

    # Get capture file location
    if helpers.file_exists(args.pcap):
        pcap = args.pcap
    else:
        sys.exit("ERROR: invalid pcap file")

    # The netscout calculations expect chunks of 5 minutes so we subdivide the pcap in chunks of 5 minutes
    # Each interval is 5 minutes. Currently hardcoded
    interval_time = 300.00

    pkts = rdpcap(pcap)
    pcap_chunks = []

    chunk_counter = 0
    chunk_start_time = pkts[0].time

    for pkt in pkts:
        # pkt.time is time since epoch
        if pkt.time - chunk_start_time < interval_time:
            try:
                pcap_chunks[chunk_counter].append(pkt)
            except IndexError:
                pcap_chunks.append([pkt])
        else:
            chunk_counter += 1
            chunk_start_time = pkt.time
            pcap_chunks.append([pkt])


main()
