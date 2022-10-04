# Bin File Reader
Python scripts to parse the output of the profiler and calculate the run time of each task, the CPU utilization and the stack usage.

### How to use

* Run 'pip install -r requirements.txt' to install the required modules
* To use for CPU utilization/timing run the python script, application_timing.py 'file-name' 'sampling-time'\
Where file name is the name of the binary file and sampling time is sampling time for CPU utilization in ms (if unspecified, default value of 50ms is used)
* To use for Stack Usage, run the python script stack_memory_usage.py 'file-name' \
file-name: binary file of stack usage

### Schema for Application Timing
Header:
<pre>
    (uint64 | little-endian) - Start ID
    (uint64 | little-endian) - Block Amount Set
    (uint64 | little-endian) - Block Size
    (uint64 | little-endian) - Capture Type
    (uint64 | little-endian) - Clock Cycles Per Second
</pre>

Data:
<pre>
    (uint16 | little-endian)
        byte[7:6]   - ID
        byte[3:0]   - Clock (in cycles)
</pre>

## Schema for Stack Memory usage

Header:
<pre>
    (uint64 | little-endian) - Start ID
    (uint64 | little-endian) - Block Amount Set
    (uint64 | little-endian) - Block Size
    (uint64 | little-endian) - Capture Type
    (uint64 | little-endian)
        byte[7:4]   - User Stack 0 Frame ID
        byte[3:0]   - User Stack 0 Base Address
    (uint64 | little-endian)
        byte[7:4]   - User Stack 1 Frame ID
        byte[3:0]   - User Stack 1 Base Address     
</pre>

Data:
<pre>
    (uint16 | little-endian)
        byte[7:6]   - ID
        reserved    - 0xFFFB:0xFFFF
    (uint16 | little-endian)
        byte[5:4]   - PSW IS
    (uint32 | little-endian)
        byte[3:0]   - STACK_POINTER
</pre>

