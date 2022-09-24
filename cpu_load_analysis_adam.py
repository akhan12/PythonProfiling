# Please refer to PROFILE.md to understand schema

import os
import numpy as np

# Create HEADER dtype
HEADER_dt = np.dtype([
    ("CLOCKS_PER_SECOND", "<u8"),
    ("STORE_AMOUNT", "<u4"),
    ("RECORD_AMOUNT", "<u4")
])

# Create STORE dtype
""" STORE_dt = np.dtype([
    ("STORE_START", "<u8"),
    ("TIMESTAMP", "<u8"),
    ("EXE_TIME_PAIR", "<u8", RECORD_AMOUNT - 1),
    ("STORE_END", "<u8")
]) """

# Get COLLECTION from cpu profile bin file
COLLECTION = open("ecu_trace", "rb")

# Get HEADER
[(CLOCKS_PER_SECOND, STORE_AMOUNT, RECORD_AMOUNT)] = np.fromfile(COLLECTION, dtype=HEADER_dt, count=1, sep="", offset=0)

# Get stores into lists
# Puts all stores into ram
# Should be modified to an iterative approach if ram resources are limited
# Iterative example idea: 1 store in ram at a time
store_start_list = []
time_snap_list = []
task_exe_time_list = []
store_end_list = []
for i in range(number_stores):
    [(store_start, time_snap, task_exe_times, store_end)] = np.fromfile(file, dtype=store_dt, count=1, sep="", offset=0)
    store_start_list.append(store_start)
    time_snap_list.append(time_snap)
    task_exe_time_list.append([])
    task_exe_time_list[i] = task_exe_times
    store_end_list.append(store_end)
[time_snap] = np.fromfile(file, dtype="<u8", count=1, sep="", offset=0)
time_snap_list.append(time_snap)

# #############################################################################################
# Single store example
# Should be done across all stores
# Proper statistical analysis should be done on data
# This is is purely for demonstration purposes

import matplotlib.pyplot as plt

# Store index
store_i = 100

# Get statistics for store i
load_exe_time_list = []
idle_exe_time_list = []
time_start = time_snap_list[store_i]
time_end = (time_snap_list[store_i+1]-1).astype(np.uint64)
load_exe_time_list = task_exe_time_list[store_i][::2]
total_load_exe_time = np.sum(load_exe_time_list)
maximum_load_exe_time = np.amax(load_exe_time_list)
idle_exe_time_list = task_exe_time_list[store_i][1::2]
total_idle_exe_time = np.sum(idle_exe_time_list)
maximum_idle_exe_time = np.amax(idle_exe_time_list)
total_store_time = time_end - (time_start + total_load_exe_time + total_idle_exe_time)
avg_cpu_utilization = (total_load_exe_time / total_idle_exe_time) * 100

print(f"Store {store_i}:")
print(f"    Time Window      (cpu clocks): {time_start} - {time_end}")
print(f"    Total load time  (cpu clocks): {total_load_exe_time}")
print(f"    Maximum load time  (cpu clocks): {maximum_load_exe_time}")
print(f"    Total idle time  (cpu clocks): {total_idle_exe_time}")
print(f"    Maximum idle time  (cpu clocks): {maximum_idle_exe_time}")
print(f"    Total store time (cpu clocks): {total_store_time}")
print(f"    Average CPU Utilization   (%): {avg_cpu_utilization}")

# Build load sequence for all stores
# 10 - load | 0 - idle | 5 - store
load_sequence = np.zeros(store_length-4, dtype="<u1")
load_sequence[::2] = 10
load_sequence = np.insert(load_sequence, 0, 10)
load_sequence = np.append(load_sequence, 5)
load_sequence = load_sequence.astype(np.uint8)

# Build time sequence for store i
time_snap = time_start
time_sequence = task_exe_time_list[store_i].astype(np.uint64)
time_sequence = np.insert(time_sequence, 0, time_snap)
time_sequence = np.append(time_sequence, total_store_time)
time_sequence = np.cumsum(time_sequence)

# Plot step graph for store i
fig, ax = plt.subplots()
ax.step(time_sequence, load_sequence, linewidth=0.5)
plt.show()
# #############################################################################################
