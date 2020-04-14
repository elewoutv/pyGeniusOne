

# This function calculates the ammount of packets sent in upload/download direction
# @param chunk A list of packets from the desired time frame to perform calculations on.
# @param subscriber_ip The IP of the subscriber. This will be used to determine the meaning of "upload" and "download".
# @return Returns a dictionary with results. Can easily be serialized to JSON.
#
def userplane_packets_count(chunk, subscriber_ip):

    # amount of packets in upload/download direction in the session
    upload_count = 0
    download_count = 0

    for pkt in chunk:
        if pkt["IP"].src == subscriber_ip:
            upload_count += 1
        else:
            download_count += 1

    return {'userplane_upload_packets_count': upload_count, 'userplane_download_packets_count': download_count}


# This function calculates the ammount of bytes sent in upload/download direction
# @param chunk A list of packets from the desired time frame to perform calculations on.
# @param subscriber_ip The IP of the subscriber. This will be used to determine the meaning of "upload" and "download".
# @return Returns a dictionary with results. Can easily be serialized to JSON.
#
def userplane_bytes_count(chunk, subscriber_ip):

    # bytecount in upload/download direction during the session
    upload_byte_count = 0
    download_byte_count = 0

    for pkt in chunk:
        if pkt["IP"].src == subscriber_ip:
            upload_byte_count += len(pkt)
        else:
            download_byte_count += len(pkt)

    return {'userplane_upload_byte_count': upload_byte_count, 'userplane_download_byte_count': download_byte_count}


# This function calculates the effective bytes (the GTP-U payload) sent in upload/download direction
# @param chunk A list of packets from the desired time frame to perform calculations on.
# @param subscriber_ip The IP of the subscriber. This will be used to determine the meaning of "upload" and "download".
# @return Returns a dictionary with results. Can easily be serialized to JSON.
#
def userplane_effective_bytes_count(chunk, subscriber_ip):

    # effective bytecount in upload/download direction during the session
    upload_effective_bytes_count = 0
    download_effective_bytes_count = 0

    for pkt in chunk:

        tunnel_layer = 5
        count = 0

        if pkt[tunnel_layer].haslayer("TCP"):

            bytes_in_header_word = 32 / 8

            # get total size from ip packet
            ip_total_len = pkt[tunnel_layer].getlayer("IP").len

            # get len field from ip header
            ip_header_len = pkt[tunnel_layer].getlayer("IP").ihl * bytes_in_header_word

            # get len field from tcp header
            tcp_header_len = pkt[tunnel_layer].getlayer("TCP").dataofs * bytes_in_header_word

            # subtract ip and tcp header size from the total packet size
            count = ip_total_len - ip_header_len - tcp_header_len

        elif pkt[tunnel_layer].haslayer("UDP"):

            # udp always has a header of 8 bytes
            udp_header_len = 8

            # get len field from udp header
            udp_packet_len = pkt[tunnel_layer].getlayer("UDP").len

            # subtract udp header size from the total packet size
            count = udp_packet_len - udp_header_len

        else:
            # if we cannot identify the protocol stack used in the tunnel, we simply calculate the GTP-U payload length
            # as a whole
            count = len(pkt["GTP_U_Header"])

        # cast result to int
        count = int(round(count))

        if pkt["IP"].src == subscriber_ip:
            upload_effective_bytes_count += count
        else:
            download_effective_bytes_count += count

    return {'userplane_upload_effective_byte_count': upload_effective_bytes_count,
            'userplane_download_effective_byte_count': download_effective_bytes_count}


# This function calculates the estimated time during which data was sent in upload/download direction
# @param chunk A list of packets from the desired time frame to perform calculations on.
# @param subscriber_ip The IP of the subscriber. This will be used to determine the meaning of "upload" and "download".
# @param resolution_time The time unit to express the active_time parameter
# @param silence_period Treshold to determine which delta's to report as active time
# @param min_report_time Time that will be counted as active time when silence_period is exceeded
# @return Returns a dictionary with results. Can easily be serialized to JSON.
#
def userplane_active_millis(chunk, subscriber_ip, resolution_time, silence_period, min_report_time):

    # one second in milliseconds, used to convert the silence period to milliseconds
    millisec = 1000

    upload_active_time = 0
    download_active_time = 0

    for i in range(0, len(chunk)):

        # if it is the first packet of the chunk, it has no delta time because there is no previous packet
        if i == 0:
            delta_time = 0

        # subtract unix time from previous packet from the unix time of the current packet
        else:
            delta_time = chunk[i].time - chunk[i - 1].time
            delta_time = delta_time * resolution_time

        # if the delta time is greater than the silence period in milliseconds,
        # count the minimum report time as active time
        if delta_time > (silence_period * millisec):
            delta_time = min_report_time

        # split the delta's based on the direction of the packet and calculate grand total for upload/download
        if chunk[i]["IP"].src == subscriber_ip:
            upload_active_time += delta_time
        else:
            download_active_time += delta_time

        # only now do we cast from decimal to integer to make the result as accurate as possible
        upload_active_time = int(round(upload_active_time))
        download_active_time = int(round(download_active_time))

    return {'userplane_upload_active_millis': upload_active_time,
            'userplane_download_active_millis': download_active_time}


# This function calculates the estimated highest throughput reached during a chunk in upload/download direction
# @param chunk A list of packets from the desired time frame to perform calculations on.
# @param subscriber_ip The IP of the subscriber. This will be used to determine the meaning of "upload" and "download".
# @param resolution_time The time unit to express the active_time parameter
# @param silence_period Treshold to determine which delta's to report as active time
# @param min_report_time Time that will be counted as active time when silence_period is exceeded
# @return Returns a dictionary with results. Can easily be serialized to JSON.
#
def userplane_max_throughput_kbps(chunk, min_report_time, resolution_time, silence_period, subscriber_ip):

    millseconds_in_second = 1000
    bits_in_byte = 8

    first_pkt = chunk[0]

    # we use a list instead of a set because the pkt type is not hashable >:(
    packets_for_throughput = []

    upload_througputs = set()
    download_throughputs = set()

    for pkt in chunk:

        packets_for_throughput.append(pkt)

        # we calculate the througput roughly every time the resolution_time has passed
        if pkt.time - first_pkt.time > resolution_time / millseconds_in_second:

            # get the upload time and convert it to seconds
            upload_time_sent_in_sec = userplane_active_millis(packets_for_throughput,
                                                              subscriber_ip,
                                                              resolution_time,
                                                              silence_period,
                                                              min_report_time).get(
                'userplane_upload_active_millis') / millseconds_in_second

            # get the effective bytes and convert it to Kb
            upload_bytes_sent_in_kilobit = userplane_effective_bytes_count(packets_for_throughput,
                                                                           subscriber_ip).get(
                'userplane_upload_effective_byte_count') * bits_in_byte / millseconds_in_second

            # same as above
            download_time_sent_in_sec = userplane_active_millis(packets_for_throughput,
                                                                subscriber_ip,
                                                                resolution_time,
                                                                silence_period,
                                                                min_report_time).get(
                'userplane_download_active_millis') / millseconds_in_second

            # same as above
            download_bytes_sent_in_kilobit = userplane_effective_bytes_count(packets_for_throughput,
                                                                             subscriber_ip).get(
                'userplane_download_effective_byte_count') * bits_in_byte / millseconds_in_second

            # calculate result in kpbs
            upload_througputs.add(upload_bytes_sent_in_kilobit / upload_time_sent_in_sec)
            download_throughputs.add(download_bytes_sent_in_kilobit / download_time_sent_in_sec)

            first_pkt = pkt

    return {'userplane_upload_max_throughput_kbps': int(round(max(upload_througputs))),
            'userplane_download_max_throughput_kbps': int(round(max(download_throughputs)))}