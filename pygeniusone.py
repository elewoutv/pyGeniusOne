# Set silence period
# Set minimum report time
# Set resolution time
# Set direction
# Set outgoing IP
# Check options
# Set options
# Parse packets
# Subdivide packets in chunks of 5 min.

# Calculate byte count
    # count = 0
    # foreach packet in packets
        # if (packet.direction() == direction)
            #count += packet.length()
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