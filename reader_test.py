import numpy as np
from statistics import mean

#Header Datatype 
HEADER_dt = np.dtype([
    ("CLOCKS_PER_SECOND", "<u8"),
    ("TIMESTAMP_AMOUNT_STEP", "<u8"),
])

#Timestamp Datatype
TIMESTAMP_dt = np.dtype([
    ("CLOCKS_SINCE_START", "<u4"),
    ("ID_TAG","<u4")
])

dtype = np.dtype('B')
np.set_printoptions(formatter={ 'int': hex})

#Read bin file according to the scheme
try:
    with open('ecu_trace.bin', 'rb') as f:
        numpy_data = np.fromfile(f, dtype=HEADER_dt, count=1, sep="", offset=0)
        numpy_data2 = np.fromfile(f, dtype=TIMESTAMP_dt, count=-1, sep="", offset=0)
    print(numpy_data[0:8])
    print(numpy_data[8:16])
    print(numpy_data2[0:5])
except IOError:
    print('Error While Opening file')

diff = []
for i in range(0,len(numpy_data2)-1):
    if numpy_data2[i]['ID_TAG'] == 0x140000:
        start = numpy_data2[i]['CLOCKS_SINCE_START']
    if numpy_data2[i+1]['ID_TAG'] == 0x1e0000:
        end = numpy_data2[i+1]['CLOCKS_SINCE_START']
    
    diff.append(end-start)


print(diff)

print(max(diff))

print(mean(diff))