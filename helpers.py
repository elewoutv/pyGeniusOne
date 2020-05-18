import ipaddress
from scapy.all import *


def check_commandline_params(parser):

    # Calculation parameter defaults
    resolution_time_default = 1000
    silence_period_default = 4
    minimum_report_time_default = 1

    # Optional arguments
    parser.add_argument('-f',
                        help="file to write output to",
                        dest='file',
                        default="")
    parser.add_argument('--resolution-time',
                        type=int,
                        default=resolution_time_default,
                        dest='resolution_time',
                        help="resolution time in ms")
    parser.add_argument('--silence-period',
                        type=int,
                        default=silence_period_default,
                        dest='silence_period',
                        help="silence period time in s")
    parser.add_argument('--minimum-report-time',
                        type=int,
                        default=minimum_report_time_default,
                        dest='min_report_time',
                        help="minimum report time in ms")
    # Required arguments
    parser.add_argument('pcap',
                        help="subscriber session pcap file")
    required_group = parser.add_argument_group(title="required arguments")
    required_group.add_argument('-i', '--ip-adress',
                                help="ip adress of the subsciber (the client)",
                                dest='ip',
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
                              dest='effectiveBytes',
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
    output_group.add_argument('-T', '--ttfb',
                              help="Include the time difference between the first syn packet and first data packet",
                              default=False,
                              dest='ttfb',
                              action="store_true")
    output_group.add_argument('-r', '--retransmitted-packets',
                              help="Include the ammount of tcp retransmissions",
                              default=False,
                              dest='retransmitted_packets',
                              action="store_true")
    output_group.add_argument('-d', '--direction',
                              help="Specify the direction (up, down, both) of the stats that will be included in output",
                              default="both",
                              dest='direction',)


def file_exists(file):
    try:
        with open(file):
            return True
    except IOError:
        return False


def is_ip_address(ip):
    try:
        check_ip = ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# Takes a pcap file and divides it into chunks
# @param pcap the pcap file to "chunkify"
# @param chunk_duration the size/duration of each chunk in seconds. Best use a float for this parameter.
# @return a list of lists of packets. Each sublist represents a chunk of chunk_duration seconds.
#
def divide_in_chunks(pcap, chunk_duration):
    interval_time = chunk_duration
    print("pcap load started", datetime.now())
    pkts = rdpcap(pcap)
    print("pcap loaded", datetime.now())
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

    return pcap_chunks
