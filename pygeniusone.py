import argparse

# Calculation parameter defaults
RESOLUTION_TIME_DEFAULT = 1000
SILENCE_PERIOD_DEFAULT = 4
MINIMUM_REPORT_TIME_DEFAULT = 1

parser = argparse.ArgumentParser(description='Calculate netScout subscriber session statistics')

# Optional arguments
parser.add_argument('-f',
                    help="file to write output to")
parser.add_argument('--resolution-time',
                    type=int,
                    default=RESOLUTION_TIME_DEFAULT,
                    dest='resolutionTime',
                    help="resolution time in ms")
parser.add_argument('--silence-period',
                    type=int,
                    default=SILENCE_PERIOD_DEFAULT,
                    dest='silencePeriod',
                    help="silence period time in s")
parser.add_argument('--minimum-report-time',
                    type=int,
                    default=MINIMUM_REPORT_TIME_DEFAULT,
                    dest='minReportTime',
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

requiredGroup = parser.add_argument_group(title="required arguments")

requiredGroup.add_argument('-i', '--ip-adress',
                           help="ip adress of the server (the receiver)",
                           dest='ip',
                           required=True)

# Output arguments
outputGroup = parser.add_argument_group(title="output options",
                                        description="pyGeniousOne will output all available statistics by default,"
                                                    " you can limit the output with these options")
outputGroup.add_argument('-C', '--count-packets',
                         help="Include packet count in output",
                         default=False,
                         dest='packetCount',
                         action="store_true")
outputGroup.add_argument('-c', '--count-bytes',
                         help="Include total byte count in output",
                         default=False,
                         dest='bytes',
                         action="store_true")
outputGroup.add_argument('-e', '--effective-bytes',
                         help="Include GTP-U byte count in output",
                         default=False,
                         dest='effectieBytes',
                         action="store_true")
outputGroup.add_argument('-a', '--active-millis',
                         help="Include total transmission time in a specific direction in output",
                         default=False,
                         dest='activeMillis',
                         action="store_true")
outputGroup.add_argument('-t', '--max-throughput',
                         help="Include highest throughput reached in specific direction in output",
                         default=False,
                         dest='maxThroughput',
                         action="store_true")
args = parser.parse_args()

# Set silence period
SILENCE_PERIOD = args.silencePeriod

# Set minimum report time
MINIMUM_REPORT_TIME = args.minReportTime

# Set resolution time
RESOLUTION_TIME = args.resolutionTime

# Set direction to calculate
# Set receiver IP
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
