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

try:
    sample_period = int(sys.argv[2])
except:
    print("No sample period specified, default 50ms")
    sample_period = 50
    

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
#added in start_times to taskRT_extraction
start_times = []
#for zero time reference utilization
initial_flag = 0

#Units in ms
for i in app_dict:
    [indv_diff, indv_start] = taskRT_extraction(i,app_dict,sorted_indices,data_time)
    indv_diff = [unit*x/clocks_per_sec for x in indv_diff]
    indv_start = [unit*x/clocks_per_sec for x in indv_start]
    diff.append(indv_diff)
    start_times.append(indv_start)
    if len(indv_start)!=0:
        temp = min(indv_start)
    if initial_flag == 0:
        zero_ref = temp
        initial_flag = 1
    elif temp<zero_ref:
        zero_ref = temp
    
    
start_times_zero_ref = [[y-zero_ref for y in x] for x in start_times]


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
total_rt_div = floor(total_rt/sample_period)
end_time = total_rt_div *sample_period

util_div = []
for i in range(0,end_time,sample_period):
    util_div.append(i)

util = [] 
temp_stime = start_times_zero_ref 
temp_diff = diff
#no duplicate searches, moving window
idy_init = [0 for x in range(0,len(temp_stime))]
for i in range(0,len(util_div)):
    shift_series = [[y-util_div[i] for y in x] for x in temp_stime]
    run_time = 0
    for idx in range(len(shift_series)):
        for idy in range(len(shift_series[idx])):
            idy_last = idy_init[idx]
            if shift_series[idx][idy]>=0 and shift_series[idx][idy]<=sample_period:
                run_time = run_time + temp_diff[idx][idy]
            elif shift_series[idx][idy]>sample_period:
                break

    #100/50ms for percent
    util.append(100*run_time/sample_period)

plt.plot(util)
plt.ylim(0,100)
util_ds = pd.Series(util)
utilization_path = os.path.join(basepath,'utilization')
os.makedirs(utilization_path, exist_ok=True)
util_stat = util_ds.describe()
print(util_stat)
util_stat.to_csv(os.path.join(utilization_path,'util_stat.csv'))
plt.savefig(os.path.join(utilization_path,'util.png'))
print('done')
    




    
