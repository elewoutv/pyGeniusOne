##
# Experimental python implementation of some of the netScout statistics calculations
# Author: Elewout Vercaeren
# Released under GPL-3.0
#

import argparse
import ipaddress

# Calculation parameter defaults
RESOLUTION_TIME_DEFAULT = 1000
SILENCE_PERIOD_DEFAULT = 4
MINIMUM_REPORT_TIME_DEFAULT = 1


def main():

    parser = argparse.ArgumentParser(description='Calculate netScout subscriber session statistics')
    # Optional arguments
    parser.add_argument('-f',
                        help="file to write output to")
    parser.add_argument('--resolution-time',
                        type=int,
                        default=RESOLUTION_TIME_DEFAULT,
                        dest='resolution_time',
                        help="resolution time in ms")
    parser.add_argument('--silence-period',
                        type=int,
                        default=SILENCE_PERIOD_DEFAULT,
                        dest='silence_period',
                        help="silence period time in s")
    parser.add_argument('--minimum-report-time',
                        type=int,
                        default=MINIMUM_REPORT_TIME_DEFAULT,
                        dest='min_report_time',
                        help="minimum report time in ms")
    parser.add_argument('-u', '--up',
                        help="calculate only upload stats",
                        default=False,
                        dest='up',
                        action="store_true")
    parser.add_argument('-d', '--down',
                        help="calculate only download stats",
                        default=False,
                        dest='down',
                        action="store_true")
    # Required arguments
    parser.add_argument('filename.pcap',
                        help="subscriber session pcap file")
    required_group = parser.add_argument_group(title="required arguments")
    required_group.add_argument('-i', '--ip-adress',
                                help="ip adress of the subsciber (the client)",
                                dest='ip',
                                type=is_ip_address(),
                                required=True)
    # Output arguments
    output_group = parser.add_argument_group(title="output options",
                                             description="pyGeniousOne will output all available statistics by default,"
                                             " you can limit the output with these options")
    output_group.add_argument('-C', '--count-packets',
                              help="Include packet count in output",
                              default=False,
                              dest='packetCount',
                              action="store_true")
    output_group.add_argument('-c', '--count-bytes',
                              help="Include total byte count in output",
                              default=False,
                              dest='bytes',
                              action="store_true")
    output_group.add_argument('-e', '--effective-bytes',
                              help="Include GTP-U byte count in output",
                              default=False,
                              dest='effectieBytes',
                              action="store_true")
    output_group.add_argument('-a', '--active-millis',
                              help="Include total transmission time in a specific direction in output",
                              default=False,
                              dest='activeMillis',
                              action="store_true")
    output_group.add_argument('-t', '--max-throughput',
                              help="Include highest throughput reached in specific direction in output",
                              default=False,
                              dest='maxThroughput',
                              action="store_true")
    args = parser.parse_args()

    # Get silence period
    silence_period = args.silencePeriod

    # Get minimum report time
    min_report_time = args.minReportTime

    # Get resolution time
    resolution_time = args.resolutionTime

    # Get subscriber
    subscriber_ip = args.ip


def is_ip_address(ip):
    try:
        check_ip = ipaddress.ip_address(ip)
        return ip
    except ValueError:
        raise argparse.ArgumentTypeError("invalid ip address")


main()


# Set subscriber IP
# Check options
# Set options
# Parse packets
# Subdivide packets in chunks of 5 min.

# Calculate byte count
# count = 0
# foreach packet in packets
# if (packet.direction() == direction)
# count += packet.length()
# return count

# Calculate packet count
# return packets.length()

# Calculate active milliseconds
# activeTime = 0
# foreach packet in packets
# if (packet.direction() == direction)
# delta = packets.calculateDeltaTime(packet)
# if (delta > silence period)
# delta = 1 ms
# activeTime += delta
# return activeTime

# Calculate effective bytes
# count = 0
# foreach packet in packets
# if (packet.direction() == direction)
# count += packet.payload.length()
# return count

# Calculate max throughput
# throughputs[] = new []
# cumulative active time = 0
# foreach packet in packets
#
