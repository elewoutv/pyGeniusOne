import math

import eff_byte_protocol_stacks


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

            # if tcp/ip is detected in the tunnel, calculate only the tcp/ip payload
            count = eff_byte_protocol_stacks.tcp_ip(pkt, tunnel_layer)

        elif pkt[tunnel_layer].haslayer("UDP"):

            # if udp/ip is detected in the tunnel, calculate only the udp/ip payload
            count = eff_byte_protocol_stacks.udp_ip(pkt, tunnel_layer)

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

    tunnel_layer = 5
    upload_chunk = []
    download_chunk = []

    # split the chunk in two separate chunks: one with all uploaded packets, one with all downloaded packets
    for pkt in chunk:

        # netscout seems to ignore empty UDP and TCP packets
        # (mostly just ACK's in the case of TCP) so we filter them out
        if pkt[tunnel_layer].haslayer("TCP"):
            tcp_payload = eff_byte_protocol_stacks.tcp_ip(pkt, tunnel_layer)
            if tcp_payload == 0.0:
                continue

        if pkt[tunnel_layer].haslayer("UDP"):
            udp_payload = eff_byte_protocol_stacks.udp_ip(pkt, tunnel_layer)
            if udp_payload == 0.0:
                continue

        if pkt["IP"].src == subscriber_ip:
            upload_chunk.append(pkt)

        else:
            download_chunk.append(pkt)

    upload_active_time = _active_time(upload_chunk, min_report_time, resolution_time, silence_period)
    upload_active_time = int(round(upload_active_time))

    download_active_time = _active_time(download_chunk, min_report_time, resolution_time, silence_period)
    download_active_time = int(round(download_active_time))

    return {'userplane_upload_active_millis': upload_active_time,
            'userplane_download_active_millis': download_active_time}


def _active_time(chunk, min_report_time, resolution_time, silence_period):

    active_time = 0

    for i in range(0, len(chunk)):

        if i == 0:
            delta_time = 1
        else:
            # subtract unix time from previous packet from the unix time of the current packet
            delta_time = (chunk[i].time - chunk[i - 1].time) * resolution_time

        # if the delta time is greater than the silence period in milliseconds,
        # count the minimum report time as active time
        if delta_time > (silence_period * resolution_time):
            delta_time = min_report_time

        active_time += delta_time

        # only now do we cast from decimal to integer to make the result as accurate as possible
    return active_time


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
    first_pkt = chunk[0]

    # we use a list instead of a set because the pkt type is not hashable >:(
    packets_for_throughput = []

    # initialize the sets with a default value of 0. If the dataset is shorter than the resolution time, there is at
    # least one value in the set.
    upload_througputs = set([0])
    download_throughputs = set([0])

    for i in range(0, len(chunk) - 1):

        pkt = chunk[i]
        packets_for_throughput.append(pkt)

        # we calculate the througput roughly every time the resolution_time has passed
        if pkt.time - first_pkt.time > resolution_time / millseconds_in_second or i == len(chunk) - 1:

            # get the upload time
            upload_time_sent = userplane_active_millis(packets_for_throughput,
                                                              subscriber_ip,
                                                              resolution_time,
                                                              silence_period,
                                                              min_report_time).get(
                'userplane_upload_active_millis')

            # get the effective bytes
            upload_bytes_sent = userplane_effective_bytes_count(packets_for_throughput,
                                                                           subscriber_ip).get(
                'userplane_upload_effective_byte_count')

            # same as above
            download_time_sent = userplane_active_millis(packets_for_throughput,
                                                                subscriber_ip,
                                                                resolution_time,
                                                                silence_period,
                                                                min_report_time).get(
                'userplane_download_active_millis')

            # same as above
            download_bytes_sent = userplane_effective_bytes_count(packets_for_throughput, subscriber_ip).get(
                'userplane_download_effective_byte_count')

            # calculate result in kpbs
            if upload_time_sent != 0:
                upload_througputs.add(upload_bytes_sent / upload_time_sent / 125)
            else:
                upload_througputs.add(0)

            if download_time_sent != 0:
                download_throughputs.add(download_bytes_sent / download_time_sent / 125)
            else:
                download_throughputs.add(0)

            first_pkt = chunk[i + 1]
            packets_for_throughput = []

    return {'userplane_upload_max_throughput_kbps': math.ceil(max(upload_througputs)),
            'userplane_download_max_throughput_kbps': math.ceil(max(download_throughputs))}
