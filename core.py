

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
