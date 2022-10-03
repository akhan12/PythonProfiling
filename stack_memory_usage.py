
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

from task_mod import extractKBits
from constants import app_list, app_dict

n = len(sys.argv)

try:
    file_name = sys.argv[1]
except:
    print("No filename passed, code will fail")

#Header Datatype 
HEADER_dt = np.dtype([
    ("Start_ID", "<u8"),
    ("Block_Amt_Set", "<u8"),
    ("Block_Size", "<u8"),
    ("Capture_Type", "<u8"),
    ("USTACK0_Base_Addr", "<u4"),
    ("USTACK0_frameID", "<u4"),
    ("ISTACK0_Base_Addr", "<u4"),
    ("ISTACK0_frameID", "<u4")
])

#Timestamp Datatype
#Note how it is flipped in this compared to the C code
STACK_dt = np.dtype([
    ("STACK_POINTER", "<u4"),
    #Legacy from old format, exclude
    ("PSW IS","<u2"),
    ("ID_TAG", "<u2")
])


#To view data as hex
np.set_printoptions(formatter={ 'int': hex})

bin_base = "bin_files"
bin_file_path = os.path.join(bin_base,file_name)
#Read bin file according to the schema
#Dump entire file into RAM 
try:
    with open(bin_file_path, 'rb') as f:
        hdr_info = np.fromfile(f, dtype=HEADER_dt, count=1, sep="", offset=0)
        data_dump = np.fromfile(f, dtype=STACK_dt, count=-1, sep="", offset=0)
        print(hdr_info["USTACK0_Base_Addr"])
        print(hdr_info["ISTACK0_Base_Addr"])
        print(hex(data_dump[0]["STACK_POINTER"]))
except IOError:
    print('Error While Opening file')


#Calculation of stack usage

UStack_b_addr= hdr_info["USTACK0_Base_Addr"]
IStack_b_addr = hdr_info["ISTACK0_Base_Addr"]
stack_usage = []
outliers = 0
for idx in range(len(app_list)):
    key = app_list[idx]
    end_id = app_dict[key][1]
    temp_stack = []
    for data in data_dump:
        if data["ID_TAG"] == end_id:
            stack_pointer = data["STACK_POINTER"]
            if end_id>1000:
                mem_usage = IStack_b_addr - stack_pointer
                #temp_stack.append(mem_usage)
            else:
                mem_usage = UStack_b_addr - stack_pointer
                #temp_stack.append(mem_usage)
            if mem_usage<1e9:
                temp_stack.append(mem_usage[0])
            
    stack_usage.append(temp_stack)

print("Done")
    
            










