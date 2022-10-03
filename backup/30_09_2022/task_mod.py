#################################
### This module contains ########
### all the user defined ########
### functions in the ############
### application_timing script ###
#################################


#this version uses the index matrix sorted_data
def taskRT_extraction(key,app_dict,sorted_data,data_time):
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