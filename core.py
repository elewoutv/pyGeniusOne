

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
        if pkt["IP"].src == subscriber_ip:
            upload_effective_bytes_count += len(pkt["GTP_U_Header"])
        else:
            download_effective_bytes_count += len(pkt["GTP_U_Header"])

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

    return {'userplane_upload_active_millis': upload_active_time,
            'userplane_download_active_millis': download_active_time}


