
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


#To view data as hex
np.set_printoptions(formatter={ 'int': hex})

#Read bin file according to the schema
#Dump entire file into RAM 
try:
    with open('ecu_trace.bin', 'rb') as f:
        hdr_info = np.fromfile(f, dtype=HEADER_dt, count=1, sep="", offset=0)
        data_dump = np.fromfile(f, dtype=TIMESTAMP_dt, count=-1, sep="", offset=0)
        print(hdr_info[0:8])
        print(hdr_info[8:16])
        print(data_dump[0:5])
except IOError:
    print('Error While Opening file')


#Calculation of run times
diff = []
for i in range(0,len(data_dump)-1):
    if data_dump[i]['ID_TAG'] == 0x140000:
        start = data_dump[i]['CLOCKS_SINCE_START']
    if data_dump[i+1]['ID_TAG'] == 0x1e0000:
        end = data_dump[i+1]['CLOCKS_SINCE_START']
    
    diff.append(end-start)


#Example barchar

runtime_series = pd.Series(diff)

print(runtime_series.describe())

ax = runtime_series.plot.hist(bins=50, range=(runtime_series.min(),500))
print(ax)
plt.show()







