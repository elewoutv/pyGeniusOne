import ipaddress


def check_commandline_params(parser):

    # Calculation parameter defaults
    resolution_time_default = 1000
    silence_period_default = 4
    minimum_report_time_default = 1

    # Optional arguments
    parser.add_argument('-f',
                        help="file to write output to")
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
