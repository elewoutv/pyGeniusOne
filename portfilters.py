def filter_tcp(pcap_chunks, tcp_port):
    for chunk in pcap_chunks:
        for pkt in chunk:
            if not pkt[5].getlayer("TCP").sport == tcp_port and not pkt[5].getlayer("TCP").dport == tcp_port:
                chunk.remove(pkt)


def filter_udp(pcap_chunks, udp_port):
    for chunk in pcap_chunks:
        for pkt in chunk:
            if not pkt[5].getlayer("TCP").sport == udp_port and not pkt[5].getlayer("TCP").dport == udp_port:
                chunk.remove(pkt)
