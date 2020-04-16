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
	    - ammount of transmitted packets in upload/download direction.
	- ```userplane_[upload|download]_bytes_count```
	    - ammount of transmitted bytes in upload/download direction. Includes all GTP traffic.
	- ```userplane_[upload|download]_effective_bytes_count```
	    - ammount of transmitted bytes in upload/download direction. Includes only GTP-U payload.
	    (only the user data sent through the tunnel). If the data in the tunnel is encapsulated in a supported protocol
	    stack, pyGeniousOne will not account the headers of this stack but only the payload (for example: if you run tcp/
	    ip in the tunnel, only the bytes after the ip and tcp header will be counted as effective bytes)
	    Supported protocol stacks: TCP/IP, UDP/IP
	- ```userplane_[upload|download]_active_millis```
	    - total time during which bytes were being transmitted in upload/download direction.
    - ```userplane_[upload|download]_max_throughput_kbps```
        - highest throughput reached during the interval in upload/download direction.
    
### Underlying calculations
#### Additional definitions
- **Delta time**
    - The time between two packets in the trace.
- **Silence period**
    - Treshold to determine which data to report as active time. If the delta between two packets
    exceeds 4 seconds, this will be interpreted as silence; instead of counting the full delta as active time, nGeniousOne
    will report only one millisecond.
- **Minimum report time**
    - The time that will be reported as delta time when the actual delta time exceeds 4 seconds.
- **Resolution time**
    - The time unit that will be used to express the active time. The resolution time defaults to 1 second.
- **Throughput**
    - Throughput is calculated everytime the total active time exceeds the resolution time (1 second).

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

## Usage
```
pygeniousone [options] filename.pcap
```
### Options

By default pyGeniusOne will output all available statistics with default parameters. You can use these options to limit the output to a subset of
stats or change the calculation parameters. You can also write output to a file.

```
-C, --count-packets
```
Include userplane_[upload|download]_packets_count in output.
```
-c, --count-bytes
```
Include userplane_[upload|download]_bytes_count in output.
```
-e, --effective-bytes
```
Include userplane_[upload|download]_effective_bytes_count in output.
```
-a, --active-millis
```
Include userplane_[upload|download]_active_millis in output.
```
-t, --max-throughput
```
Include userplane_[upload|download]_max_throughput in output.
```
--resolution-time
```
Resolution time (see above)
```
--silence-period
```
Silence period (see above)
```
--minimum-report-time
```
Minimum report time (see above)
```
-i --ip-adress x.x.x.x
```
The address of the subscriber (the client). This is used to determine which packets to count in "upload" and "download"
direction.
```
-f
```
Specify file to write output to.

## Development
### Effective bytes protocol stacks

You can implement additional methods for other protocol stacks to calculate the effective bytes inside the tunnel. 
You'll have to add a filter in the eff_byte_protocol_stacks.py file and add an additional branch in the effective bytes 
function.
