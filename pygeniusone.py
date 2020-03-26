##
# Experimental python implementation of some of the netScout statistics calculations
# Author: Elewout Vercaeren
# Released under GPL-3.0
#

import json
import argparse
import helpers
import core
from scapy.all import *
from scapy.contrib.gtp import *


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

    # we need this to print the chunk number between the JSON's
    chunk_count = 0

    for chunk in pcap_chunks:

        # Calculate stats and print a JSON
        data = {}

        data.update(core.userplane_packets_count(chunk, subscriber_ip))
        data.update(core.userplane_bytes_count(chunk, subscriber_ip))
        data.update(core.userplane_effective_bytes_count(chunk, subscriber_ip))
        data.update(core.userplane_active_millis(chunk, subscriber_ip, resolution_time, silence_period, min_report_time))

        print("chunk", chunk_count)
        print(json.dumps(data))

        chunk_count += 1

    for chunk in pcap_chunks:
        first_pkt = chunk[0]

        # we use a list instead of a set because the pkt type is not hashable
        packets_for_throughput = []

        upload_througputs = set()
        download_throughputs = set()

        for pkt in chunk:

            packets_for_throughput.append(pkt)

            if pkt.time - first_pkt.time > resolution_time/1000:

                upload_time_sent_in_sec = core.userplane_active_millis(packets_for_throughput, subscriber_ip, resolution_time, silence_period, min_report_time).get('userplane_upload_active_millis') / 1000
                upload_bytes_sent_in_kilobit = core.userplane_effective_bytes_count(packets_for_throughput, subscriber_ip).get('userplane_upload_effective_byte_count') * 8 / 1000

                download_time_sent_in_sec = core.userplane_active_millis(packets_for_throughput, subscriber_ip, resolution_time, silence_period, min_report_time).get('userplane_download_active_millis') / 1000
                download_bytes_sent_in_kilobit = core.userplane_effective_bytes_count(packets_for_throughput, subscriber_ip).get('userplane_download_effective_byte_count') * 8 / 1000

                upload_througputs.add(upload_bytes_sent_in_kilobit/upload_time_sent_in_sec)
                download_throughputs.add(download_bytes_sent_in_kilobit/download_time_sent_in_sec)

                first_pkt = pkt

        print(int(round(max(upload_througputs))))
        print(int(round(max(download_throughputs))))


main()

