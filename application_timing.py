
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#this version uses the index matrix sorted_data
def taskRT_extraction2(key,app_dict,sorted_data,data_time):
    diff = []
    start_id = app_dict[key][0]
    stop_id = app_dict[key][1]
    other_start_stop = []
    #find other start_stop values
    for other_key in app_dict:
        if other_key!=key:
            other_start_stop.append(app_dict[other_key])
    
    for idx in range(len(sorted_data)-1):
        if sorted_data[idx][1] != start_id:
            continue
        #if next value is the stop/end value
        if sorted_data[idx][1] == start_id and sorted_data[idx+1][1]== stop_id:
            next_data = data_time[sorted_data[idx+1][0]]
            current_data = data_time[sorted_data[idx][0]]
            diff.append(next_data-current_data)
        
        else: 
            for idy in range(idx+1,len(sorted_data)-1):
                if sorted_data[idx][1] == start_id and sorted_data[idy][1]== stop_id:
                    next_data = data_time[sorted_data[idy][0]]
                    current_data = data_time[sorted_data[idx][0]]
                    temp_diff = next_data - current_data
                    #end checker for other task
                    other_start_id = sorted_data[idx+1][1]
                    other_end_id = other_start_id + 1
                    for oidx in range(idx+2,idy):
                        if sorted_data[oidx][1] == other_end_id:
                            other_current = data_time[sorted_data[idx+1][0]]
                            other_next = data_time[sorted_data[oidx][0]]
                            other_diff = other_next - other_current
                            diff.append(temp_diff - other_diff)
                            break
                    break
                        
    return diff   

def taskRT_extraction(key,app_dict,data_split):
    diff = []
    start_id = app_dict[key][0]
    stop_id = app_dict[key][1]
    other_start_stop  = []
    
    #find other start_stop values
    for other_key in app_dict:
        if other_key!=key:
            other_start_stop.append(app_dict[other_key])
    
    for idx in range((len(data_split))-1):
        #no preemption
        if data_split[idx][1] == start_id and data_split[idx+1][1] == stop_id:
            diff.append(data_split[idx+1][0]-data_split[idx][0])
        #check preemption
        elif data_split[idx][1] == start_id:
            start = data_split[idx][0]
            for idy in range(idx+2,(data_split.size)-1):
                if data_split[idy][1] == stop_id:
                    end = data_split[idy][0]
        #check run time for higher priority task runtimes


def all_list_indices(data_list, value):
     
     indices = []
     for i in range(len(data_list)):
         if data_list[i] == value:
             indices.append(i)
     return indices        

def sortFunc(e):
    return e[0]
     
def task_separator(key,app_dict,data_id,data_time):
    start_id = app_dict[key][0]
    end_id = app_dict[key][1]
    
    start_indices = all_list_indices(data_id,start_id)
    end_indices = all_list_indices(data_id,end_id)
    #length of both combined
    start_stop_comb = []
    max_ind = max(len(start_indices),len(end_indices))
    len_start = len(start_indices)
    len_end = len(end_indices)
    
    #keep track of where in the sort each array is
    start_ind = 0
    end_ind = 0
    #testing of refecatoring of below code
    start_stop_comb_refactor = []
    for i in start_indices:
        start_stop_comb_refactor.append([i,start_id])
    
    for i in end_indices:
        start_stop_comb_refactor.append([i,end_id])
    
    start_stop_comb_refactor.sort(key=sortFunc)
        
    
    
    
    #loop to combine
    # for i in range(len_start+len_end):
    #     if start_ind >= len_start and end_ind<len_end:
    #         start_stop_comb.append([end_indices[end_ind],end_id])
    #         end_ind = end_ind + 1
    #     elif end_ind >= len_end and start_ind<len_start:
    #         start_stop_comb.append([start_indices[start_ind],start_id])
    #         start_ind = start_ind + 1
    #     else:
    #         if start_indices[start_ind] < end_indices[end_ind]:
    #             start_stop_comb.append([start_indices[start_ind],start_id])
    #             start_ind = start_ind + 1
    #         else:
    #             start_stop_comb.append([end_indices[end_ind],end_id])
    #             end_ind = end_ind + 1
                
    comb_nodup = duplicate_finder(start_stop_comb_refactor,start_id, end_id)
    
  
    
    return comb_nodup
            

#find duplicates in tasks separated out in the task separate function
def duplicate_finder(comb,start_id, stop_id):
    
    comb_len = len(comb)
    comb_nodup = []
    dup_flag = 0
    for i in range(comb_len-1):
        if dup_flag == 1:
            dup_flag = 0
        #edge case (end)
        elif dup_flag ==1 and i==(comb_len-2):
            comb_nodup.append(comb[i+1])
        elif comb[i][1]==comb[i+1][1]:
            dup_flag = 1
            # print("duplicate_detected")
            # print(comb[i])
            # print(comb[i+1])
            #if a start then take the second if end take the first
            #assume first start does not have a matching end and 
            #second end does not have a matching start 
            if comb[i][1] == start_id:
                comb_nodup.append(comb[i+1])
            else: comb_nodup.append(comb[i])
        elif i==(comb_len-2) and comb[i][1]!=comb[i+1][1]:
                comb_nodup.append(comb[i])
                comb_nodup.append(comb[i+1])
        else: comb_nodup.append(comb[i])
   
    return comb_nodup
    
        
    
    
        
    
    
    
    
           

                    
    
    

#https://www.geeksforgeeks.org/python-slicing-extract-k-bits-given-position/
def extractKBits(num,k,p):
 
     # convert number into binary first
     binary = bin(num)
 
     # remove first two characters
    
     binary = binary[2:]
 
     end = len(binary) - p
     #modfied to specify up to the MSb
     if k == 0:
         start = 0
     else: 
        start = end - k + 1
 
     # extract k  bit sub-string
     kBitSubStr = binary[start : end+1]
  
   
     return int(kBitSubStr,2)
 
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
    with open('ecu_trace_final.bin', 'rb') as f:
        hdr_info = np.fromfile(f, dtype=HEADER_dt, count=1, sep="", offset=0)
        data_dump = np.fromfile(f, dtype=TIMESTAMP_dt, count=-1, sep="", offset=0)
        print(hdr_info[0:8])
        print(hdr_info[8:16])
        print(data_dump[0:5])
except IOError:
    print('Error While Opening file')

#if x!=0 used to remove anaomlies (found an all zeroes entry in bin file)
#issues to add to readme
#1. anomaly values of all zeroes (currently does this but if the entire 8 bytes are zero)
#if they are not as in the footer then extractbits throws an error
#2. footer extraction (avoids zero detection ) is the solution

#footer extraction (assumption that the footer is present)

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



test = all_list_indices(data_id, 50)
test2 = all_list_indices(data_id, 51)

sorted_indices = []
for i in app_dict:
    print(i)
    comb_nodup = task_separator(i,app_dict,data_id,data_time)
    sorted_indices.extend(comb_nodup)
#comb_nodup = duplicate_finder(comb,10,11)

sorted_indices.sort(key=sortFunc)
diff = []
for i in app_dict:
    indv_diff = taskRT_extraction2(i,app_dict,sorted_indices,data_time)
    diff.append(indv_diff)

#Calculation of run times
diff_series = []
for i in range(len(diff)):
    diff_series.append(pd.Series(diff[i]))
#Example barchar
for i in range(len(diff)):
    print(diff_series[i].describe())
    
# runtime_series = pd.Series(diff)
# print(runtime_series.describe())

# ax = runtime_series.plot.hist(bins=50)
# print(ax)
# plt.show()
for i in range(len(diff)):
    (diff_series[i]).to_csv(f'timing_{app_list[i]}.csv')
    stats_ser = diff_series[i].describe()
    stats_ser.to_csv(f'stats_{app_list[i]}.csv')

fig, axes = plt.subplots(nrows=2, ncols=2)

diff_series[0].plot.hist(bins=50,ax=axes[0,0])
diff_series[1].plot.hist(bins=50,ax=axes[0,1])
diff_series[2].plot.hist(bins=50,ax=axes[1,0])
diff_series[3].plot.hist(bins=50,ax=axes[1,1])

plt.show()








