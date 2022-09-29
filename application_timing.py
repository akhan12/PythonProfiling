
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#https://www.geeksforgeeks.org/python-slicing-extract-k-bits-given-position/
def extractKBits(num,k,p):
 
     # convert number into binary first
     binary = bin(num)
 
     # remove first two characters
    
     binary = binary[2:]
 
     end = len(binary) - p
     start = end - k + 1
 
     # extract k  bit sub-string
     kBitSubStr = binary[start : end+1]
  
     print(int(kBitSubStr,2))
     return int(kBitSubStr,2)
 

#Application Dictionary
app_dict = {
    "OsTask_ASW_Period" : [10, 11],
    "OsTask_ASW" : [30, 31],
    "OsTask_BSW" : [50, 51],
    "OsTask_CDD_Period": [120, 121],
    "OsTask_EthTSyn" : [130, 131],
    "OsTask_MS" : [140, 141],
    "OsTask_SUM_DataRecv" : [160, 161],
    "OsTask_SUM_Period" : [200, 201], 
    "OsTask_SUM" : [280, 281]
}
#Header Datatype 
HEADER_dt = np.dtype([
    ("Start_ID", "<u8"),
    ("Block_Amt_Set", "<u8"),
    ("Block_Size", "<u8"),
    ("Capture_Type", "<u8"),
    ("Clocks_Per_Sec", "<u8")
])

#Timestamp Datatype
#Note how it is flipped compared to the C code/Schema when 
#taking 64 bits
TIMESTAMP_dt = np.dtype('<u8')


#To view data as hex
np.set_printoptions(formatter={ 'int': hex})

#Read bin file according to the schema
#Dump entire file into RAM 
try:
    with open('ecu_trace_final.bin', 'rb') as f:
        hdr_info = np.fromfile(f, dtype=HEADER_dt, count=1, sep="", offset=0)
        data_dump = np.fromfile(f, dtype=TIMESTAMP_dt, count=-1, sep="", offset=0)
        print(hdr_info[0:8])
        print(hdr_info[8:16])
        print(data_dump[0:5])
except IOError:
    print('Error While Opening file')

#if x!=0 used to remove anaomlies (found an all zeroes entry in bin file)
data_split = [[extractKBits(x,48,1),extractKBits(x,64,49)] for x in data_dump if x!=0]

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

ax = runtime_series.plot.hist(bins=50)
print(ax)
plt.show()







