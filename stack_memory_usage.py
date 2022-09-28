
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Header Datatype 
HEADER_dt = np.dtype([
    ("Start_ID", "<u8"),
    ("Block_Amt_Set", "<u8"),
    ("Block_Size", "<u8"),
    ("Capture_Type", "<u8"),
    ("USTACK0_Base_Addr", "<u8"),
    ("ISTACK0_Base_Addr", "<u8")
])

#Timestamp Datatype
#Note how it is flipped in this compared to the C code
STACK_dt = np.dtype([
    ("STACK_POINTER", "<u4"),
    ("PSW IS","<u2"),
    ("ID_TAG", "<u2")
])


#To view data as hex
np.set_printoptions(formatter={ 'int': hex})

#Read bin file according to the schema
#Dump entire file into RAM 
try:
    with open('ecu_trace_stack.bin', 'rb') as f:
        hdr_info = np.fromfile(f, dtype=HEADER_dt, count=1, sep="", offset=0)
        data_dump = np.fromfile(f, dtype=STACK_dt, count=-1, sep="", offset=0)
        print(hdr_info)
     
        print(data_dump[0:5])
except IOError:
    print('Error While Opening file')


#Calculation of run times








