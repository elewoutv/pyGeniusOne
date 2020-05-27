# pyGeniusOne
Experimental python implementation of some of the netScout statistics calculations

## Description
This program takes a pcap file as input and calculates subscriber session statistics (see below) from the given packet trace in 
chunks of 5 minutes. It will output this to STDOUT or a file in JSON format.
These statistics are calculated using the netScout algorithms. The software can be used to compare capture data from 
a probe system directly to detect irregularities in bigdata feed output.

### nGeniusOne available statistics
- **available**
	- ```userplane_[upload|download]_packets_count```
	    - amount of transmitted packets in upload/download direction.
	- ```userplane_[upload|download]_bytes_count```
	    - amount of transmitted bytes in upload/download direction. Includes all GTP traffic.
	- ```userplane_[upload|download]_effective_bytes_count```
	    - amount of transmitted bytes in upload/download direction. Includes only GTP-U payload.
	    (only the user data sent through the tunnel). If the data in the tunnel is encapsulated in a supported protocol
	    stack, pyGeniusOne will not account the headers of this stack but only the payload (for example: if you run tcp/
	    ip in the tunnel, only the bytes after the ip and tcp header will be counted as effective bytes)
	    Supported protocol stacks: TCP/IP, UDP/IP
	- ```userplane_[upload|download]_active_millis```
	    - total time during which bytes were being transmitted in upload/download direction.
    - ```userplane_[upload|download]_max_throughput_kbps```
        - highest throughput reached during the interval in upload/download direction.
    - ```userplane_[upload|download]_retransmitted_packets_count```
        - amount of tcp retransmissions during the interval in upload/download direction.
    - ```userplane_ttfb_usec```
        - time difference in milliseconds between the first tcp syn of a connection and the first data packet.
        
    
### Underlying calculations
#### Additional definitions
- **Delta time**
    - The time between two packets in the trace.
- **Silence period**
    - Threshold to determine which data to report as active time. If the delta between two packets
    exceeds 4 seconds, this will be interpreted as silence; instead of counting the full delta as active time, nGeniousOne
    will report only one millisecond.
- **Minimum report time**
    - The time that will be reported as delta time when the actual delta time exceeds 4 seconds.
- **Resolution time**
    - The time unit that will be used to express the active time. The resolution time defaults to 1 second.
- **Throughput**
    - Throughput is calculated every time the total active time exceeds the resolution time (1 second).

#### Algorithms

##### Throughput
```
throughput = userplane_effective_bytes_count / userplane_active_millis / 125
```

##### userplane_[upload|download]_max_throughput_kbps
```
maxThroughput = max(allThroughputs)
```

##### userplane_[upload|download]_active_millis
```
calculate delta for each packet
filter packets based on up/download

for each deltaTime in packets

    if deltaTime > 4s
        activeTime += 1 millisecond
    else
        activeTime += deltaTime

return activeTime
```
Please note that the active millis function ignores UDP and TCP packets inside the tunnel with an empty payload
(like naked TCP ACK's).

If the first packet of a trace is considered, its deltatime is equal to the minimum_report_time.

## Usage
```
pygeniusone [options] filename.pcap
```
### Options

To list all options and a description of what they do use:
```
pygeniusone -h
```

## Development
### Effective bytes protocol stacks

You can implement additional methods for other protocol stacks to calculate the effective bytes inside the tunnel. 
You'll have to add a filter in the eff_byte_protocol_stacks.py file and add an additional branch in the effective bytes 
function.
