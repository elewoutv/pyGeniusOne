##
# Experimental python implementation of some of the netScout statistics calculations
# Author: Elewout Vercaeren
# Released under GPL-3.0
#

import json
import argparse
import sys
import helpers
from scapy.all import *


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
    pcap_chunks = helpers.divide_in_chunks(pcap, 300.00)

    # amount of packets in upload/download direction in the session
    upload_count = 0
    download_count = 0

    # we need this to print the chunk number between the JSON's
    chunk_count = 0

    # We scan all packets and match the subscriber_ip from commandline to the src ip of the outer IP layer.
    # If we find a match we count it as upload, all other packets are counted as download

    for chunk in pcap_chunks:
        for pkt in chunk:
            if pkt["IP"].src == subscriber_ip:
                upload_count += 1
            else:
                download_count += 1
        data = {'userplane_upload_packets_count': upload_count, 'userplane_download_packets_count': download_count}
        print("time chunk", chunk_count)
        json_data = json.dumps(data)
        print(json_data)
        chunk_count += 1
        upload_count = 0
        download_count = 0


main()
