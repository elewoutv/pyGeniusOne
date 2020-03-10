# pyGeniusOne
Experimental python implementation of some of the nGeniusOne statistics algorithms

## Description
This program takes a pcap file as input and calculates network statistics (see below) from the given packet trace in 
chunks of 5 minutes.
These statistics are calculated using the nGeniusOne algorithms. The software can be used to compare capture data from 
a probe system directly to detect irregularities in nGeniousOne.

### nGeniusOne available statistics
- **available**
	- none
- **planned**
	- ```userplane_[upload|download]_bytes_count```
	    - ammount of transmitted bytes in upload/download direction. Includes all GTP traffic.
	- ```userplane_[upload|download]_packets_count```
	    - ammount of transmitted packets in upload/download direction.
	- ```userplane_[upload|download]_active_millis```
	    - total time during which bytes were being transmitted in upload/download direction.
	- ```userplane_[upload|download]_effective_bytes_count```
	    - ammount of transmitted bytes in upload/download direction. Includes only GTP payload.
	    (so only user data)
    - ```userplane_[upload|download]_max_throughput_kbps```
        - highest throughput reached during the interval in upload/download direction.
    
### Underlying algorithms
#### Additional definitions
- **Delta time**
    - The time between two packets in the same flow. (sender <-> receiver)
- **Silence period**
    - Treshold to determine which data to report as active time. If the delta between two packets
    exceeds 4 seconds, this will be interpreted as silence; instead of counting the full delta as active time, nGeniousOne
    will report only one microsecond. (presumeably to account for the average time of a terminating syn-ack?)
- **Minimum report time**
    - The time that will be reported as delta time when the actual delta time exceeds 4 seconds.
- **Resolution time**
    - The time unit that will be used to express the active time. The resolution time defaults to 1 second.
- **Throughput**
    - Throughput is calculated everytime the (total?) delta time exceeds the resolution time (1 second)

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
it doesn't exist :D

