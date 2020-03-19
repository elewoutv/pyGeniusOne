##
# Experimental python implementation of some of the netScout statistics calculations
# Author: Elewout Vercaeren
# Released under GPL-3.0
#

import argparse
import sys
import pyshark
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

    cap = pyshark.FileCapture(pcap)
    print(cap[0])


main()
