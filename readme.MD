# Bin File Reader
A simple python script to read the output of the profiler and calculate the time to run a task

## How it works

Issues to check for:
* Missing Header
* Ensure that start/stop ID of corresponding rows are for that run

## Schema for Application Timing
 Populate with Schema info and data types

## Schema for Stack Memory usage

(uint16 | little-endian)\
    byte[7:6]   - ID\
    reserved    - 0xFFFB:0xFFFF\
(uint16 | little-endian)\
    byte[5:4]   - PSW IS\
(uint32 | little-endian)\
    byte[3:0]   - STACK_POINTER\
