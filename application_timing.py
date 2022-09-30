import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

from task_mod import extractKBits, task_separator, sortFunc, taskRT_extraction

n = len(sys.argv)

units ={
    "ms": 1000,
    "uS": 1e6
}

try:
    file_name = sys.argv[1]
except:
    print("No filename passed, code will fail")

try:
    unit = units[sys.argv[2]]
except:
    print("Wrong or no units specified, default milliseconds")
    unit = units["ms"]

#Application list for naming
app_list = ['OsTask_ASW_Period',
            'OsTask_ASW',
            'OsTask_BSW',
            'OsTask_CDD_Period',
            'OsTask_EthTSyn',
            'OsTask_MS',
            'OsTask_SUM_DataRecv',
            'OsTask_SUM_Period',
            'OsTask_SUM']

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
    with open(file_name, 'rb') as f:
        hdr_info = np.fromfile(f, dtype=HEADER_dt, count=1, sep="", offset=0)
        data_dump = np.fromfile(f, dtype=TIMESTAMP_dt, count=-1, sep="", offset=0)
        print(hdr_info[0:8])
        print(hdr_info[8:16])
        print(data_dump[0:5])
except IOError:
    print('Error While Opening file')

clocks_per_sec = extractKBits(hdr_info['Clocks_Per_Sec'][0],48,1)


footer = data_dump[-4:]
if extractKBits(footer[0],16,49)==0xFFFC:
    print("footer is fine")
    #remove footer from data_dump
    for i in range(4):
        print(len(data_dump))
        data_dump = np.delete(data_dump,(len(data_dump)-1))
#data splitting into timestamps and id
#data_split = [[extractKBits(x,48,1),extractKBits(x,0,49)] for x in data_dump if x!=0]
#refactoring the above into two separate lists
data_id = [extractKBits(x,0,49) for x in data_dump if x!=0]
data_time = [extractKBits(x,48,1) for x in data_dump if x!=0]


sorted_indices = []
for i in app_dict:
    print(i)
    comb_nodup = task_separator(i,app_dict,data_id,data_time)
    sorted_indices.extend(comb_nodup)


sorted_indices.sort(key=sortFunc)

diff = []
for i in app_dict:
    indv_diff = taskRT_extraction(i,app_dict,sorted_indices,data_time)
    indv_diff = [unit*x/clocks_per_sec for x in indv_diff]
    diff.append(indv_diff)

#Calculation of run times
diff_series = []
for i in range(len(diff)):
    diff_series.append(pd.Series(diff[i]))
#Example barchar
for i in range(len(diff)):
    print(diff_series[i].describe())
    
#Paths
basepath = './timing_csv'
os.makedirs(basepath, exist_ok=True)

timing_path = os.path.join(basepath,'timing')
os.makedirs(timing_path, exist_ok=True)

stat_path = os.path.join(basepath,'stat')
os.makedirs(stat_path, exist_ok=True)

imgs_path = "./images"
os.makedirs(imgs_path, exist_ok=True)

for i in range(len(diff)):
    data_path = os.path.join(timing_path,f'timing_{app_list[i]}.csv')
    st_path = os.path.join(stat_path,f'stats_{app_list[i]}.csv')
    (diff_series[i]).to_csv(data_path)
    stats_ser = diff_series[i].describe()
    stats_ser.to_csv(st_path)
    fig1 = plt.figure(i)
    diff_series[i].plot.hist(bins=50)
    img_path = os.path.join(imgs_path, f'hist_{app_list[i]}.png')
    plt.savefig(img_path)
    
    







