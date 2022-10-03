import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
from math import floor

from task_mod import extractKBits, task_separator, sortFunc, taskRT_extraction

from constants import app_list, app_dict

n = len(sys.argv)

units ={
    "ms": 1000,
    "uS": 1e6
}

try:
    file_name = sys.argv[1]
except:
    print("No filename passed, code will fail")


unit = units["ms"]


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
bin_base = "bin_files"
bin_file_path = os.path.join(bin_base,file_name)
try:
    with open(bin_file_path, 'rb') as f:
        hdr_info = np.fromfile(f, dtype=HEADER_dt, count=1, sep="", offset=0)
        data_dump = np.fromfile(f, dtype=TIMESTAMP_dt, count=-1, sep="", offset=0)
        print(hdr_info[0:8])
        print(hdr_info[8:16])
        print(data_dump[0:5])
except IOError:
    print('Error While Opening file')

clocks_per_sec = extractKBits(hdr_info['Clocks_Per_Sec'][0],48,1)


footer = data_dump[-1:]
if extractKBits(footer[0],16,49)==0xFFFF:
    print("footer is fine")
    #remove footer from data_dump 
    for i in range(1):
        print(len(data_dump))
        data_dump = np.delete(data_dump,(len(data_dump)-1))
#data splitting into timestamps and id
#Units in clock cycles
data_id = [extractKBits(x,0,49) for x in data_dump if x!=0]
data_time = [extractKBits(x,48,1) for x in data_dump if x!=0]

#first separate each task using task_separate which also calls 
#the duplicate finder function and then creates a list without duplicates
#for all start/stop ids
sorted_indices = []
for i in app_dict:
    comb_nodup = task_separator(i,app_dict,data_id,data_time)
    sorted_indices.extend(comb_nodup)

#Values added sequentially 
#so a sort function to sort by idx is added
sorted_indices.sort(key=sortFunc)

diff = []
#Units in ms
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
    print(app_list[i])
    print(diff_series[i].describe())
    print("")
    
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
    plt.close()
    
#################################
#####CPU Utilization Section#####
#################################
    
total_rt =unit*(data_time[-1] - data_time[0])/clocks_per_sec

sum_rt = 0

for i in diff:
    if len(i)!=0:
        sum_rt = sum_rt + sum(i)

print(f'CPU Utilization: {(sum_rt/total_rt)*100:.2f} %')

#divide into 50ms windows
total_rt_div = floor(total_rt/50)
end_time = total_rt_div *50

util_div = []
for i in range(0,end_time,50):
    util_div.append(i)
    
print('done')
    




    
