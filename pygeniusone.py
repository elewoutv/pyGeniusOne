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

    # this is very ugly. I'm so sorry
    if not args.packetCount and not args.bytes and not args.effectiveBytes and not args.activeMillis and not args.maxThroughput:

        calc_packet_count = True
        calc_bytes_count = True
        calc_eff_bytes_count = True
        calc_active_millis = True
        calc_max_throughput = True

    else:
        calc_packet_count = args.packetCount
        calc_bytes_count = args.bytes
        calc_eff_bytes_count = args.effectiveBytes
        calc_active_millis = args.activeMillis
        calc_max_throughput = args.maxThroughput

    for chunk in pcap_chunks:

        # Calculate stats and print a JSON
        data = {}

        if calc_packet_count:
            data.update(core.userplane_packets_count(chunk, subscriber_ip))

        if calc_bytes_count:
            data.update(core.userplane_bytes_count(chunk, subscriber_ip))

        if calc_eff_bytes_count:
            data.update(core.userplane_effective_bytes_count(chunk, subscriber_ip))

        if calc_active_millis:
            data.update(core.userplane_active_millis(chunk, subscriber_ip, resolution_time, silence_period, min_report_time))

        if calc_max_throughput:
            data.update(core.userplane_max_throughput_kbps(chunk, min_report_time, resolution_time, silence_period, subscriber_ip))

        # if the -f option is specified, write to file instead of STDOUT
        if args.file == "":
            print("chunk", chunk_count)
            print(json.dumps(data))

        else:
            file = open(args.file, "w")
            file.write("chunk" + " " + str(chunk_count) + "\n")
            file.write(json.dumps(data))

        chunk_count += 1


main()

