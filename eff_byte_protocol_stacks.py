

# This function calculates the effective data portion in bytes of a tcp/ip packet encapsulated in another packet
# @param pkt The whole packet (with encapsulation layers included)
# @param tunnel_layer The layer above the lowest IP layer (the tunnel layer)
# @return the effective bytes inside the encapsulated TCP/IP packet
#
def tcp_ip(pkt, tunnel_layer):

    bytes_in_header_word = 32 / 8

    # get total size from ip packet
    ip_total_len = pkt[tunnel_layer].getlayer("IP").len

    # get len field from ip header
    ip_header_len = pkt[tunnel_layer].getlayer("IP").ihl * bytes_in_header_word

    # get len field from tcp header
    tcp_header_len = pkt[tunnel_layer].getlayer("TCP").dataofs * bytes_in_header_word

    # subtract ip and tcp header size from the total packet size
    return ip_total_len - ip_header_len - tcp_header_len


# This function calculates the effective data portion in bytes of a udp/ip packet encapsulated in another packet
# @param pkt The whole packet (with encapsulation layers included)
# @param tunnel_layer The layer above the lowest IP layer (the tunnel layer)
# @return the effective bytes inside the encapsulated UDP/IP packet #
#
def udp_ip(pkt, tunnel_layer):

    # udp always has a header of 8 bytes
    udp_header_len = 8

    # get len field from udp header
    udp_packet_len = pkt[tunnel_layer].getlayer("UDP").len

    # subtract udp header size from the total packet size
    return udp_packet_len - udp_header_len

