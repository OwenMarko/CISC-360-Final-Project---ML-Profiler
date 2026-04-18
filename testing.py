import re
import time
import datalogger
import pandas as pd

data = """
*** Sampled system activity (Sat Apr  4 13:20:22 2026 -0400) (516.35ms elapsed) ***


**** Processor usage ****

E-Cluster Online: 100%
E-Cluster HW active frequency: 1208 MHz
E-Cluster HW active residency:  20.40% (1020 MHz:  18% 1404 MHz:   0% 1788 MHz:   0% 2112 MHz: .36% 2352 MHz: 1.8% 2532 MHz: .61% 2592 MHz: .09%)
E-Cluster idle residency:  79.60%
E-Cluster down residency:   0.00%
CPU 0 frequency: 1259 MHz
CPU 0 active residency:  13.23% (1020 MHz:  11% 1404 MHz:   0% 1788 MHz:   0% 2112 MHz: .24% 2352 MHz: 1.5% 2532 MHz: .51% 2592 MHz: .05%)
CPU 0 idle residency:  86.77%
CPU 0 down residency:   0.00%
CPU 1 frequency: 1133 MHz
CPU 1 active residency:   9.66% (1020 MHz: 8.8% 1404 MHz:   0% 1788 MHz:   0% 2112 MHz: .13% 2352 MHz: .54% 2532 MHz: .08% 2592 MHz: .06%)
CPU 1 idle residency:  90.34%
CPU 1 down residency:   0.00%
CPU 2 frequency: 1153 MHz
CPU 2 active residency:   4.59% (1020 MHz: 4.1% 1404 MHz:   0% 1788 MHz:   0% 2112 MHz: .11% 2352 MHz: .33% 2532 MHz: .03% 2592 MHz: .01%)
CPU 2 idle residency:  95.41%
CPU 2 down residency:   0.00%
CPU 3 frequency: 1209 MHz
CPU 3 active residency:   2.68% (1020 MHz: 2.3% 1404 MHz:   0% 1788 MHz:   0% 2112 MHz: .14% 2352 MHz: .18% 2532 MHz: .07% 2592 MHz:   0%)
CPU 3 idle residency:  97.32%
CPU 3 down residency:   0.00%

P0-Cluster Online: 0%
P0-Cluster HW active frequency: 0 MHz
P0-Cluster HW active residency:   0.00% (1260 MHz:   0% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz:   0% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
P0-Cluster idle residency:   0.00%
P0-Cluster down residency: 100.00%
CPU 4 frequency: 0 MHz
CPU 4 active residency:   0.00% (1260 MHz:   0% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz:   0% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 4 idle residency:   0.00%
CPU 4 down residency: 100.00%
CPU 5 frequency: 0 MHz
CPU 5 active residency:   0.00% (1260 MHz:   0% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz:   0% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 5 idle residency:   0.00%
CPU 5 down residency: 100.00%
CPU 6 frequency: 0 MHz
CPU 6 active residency:   0.00% (1260 MHz:   0% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz:   0% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 6 idle residency:   0.00%
CPU 6 down residency: 100.00%
CPU 7 frequency: 0 MHz
CPU 7 active residency:   0.00% (1260 MHz:   0% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz:   0% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 7 idle residency:   0.00%
CPU 7 down residency: 100.00%
CPU 8 frequency: 0 MHz
CPU 8 active residency:   0.00% (1260 MHz:   0% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz:   0% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 8 idle residency:   0.00%
CPU 8 down residency: 100.00%

P1-Cluster HW active frequency: 2806 MHz
P1-Cluster HW active residency:   5.57% (1260 MHz: 2.9% 1512 MHz:   0% 1800 MHz: .02% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz: .01% 3996 MHz: .28% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz: .01% 4512 MHz: 2.4%)
P1-Cluster idle residency:  39.98%
P1-Cluster down residency:  54.45%
CPU 9 frequency: 1342 MHz
CPU 9 active residency:   0.09% (1260 MHz: .08% 1512 MHz:   0% 1800 MHz: .00% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz: .00% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 9 idle residency:  45.51%
CPU 9 down residency:  54.40%
CPU 10 frequency: 1260 MHz
CPU 10 active residency:   0.08% (1260 MHz: .08% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz:   0% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 10 idle residency:  45.52%
CPU 10 down residency:  54.40%
CPU 11 frequency: 2915 MHz
CPU 11 active residency:   0.26% (1260 MHz: .10% 1512 MHz:   0% 1800 MHz: .01% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz: .16% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 11 idle residency:  45.34%
CPU 11 down residency:  54.40%
CPU 12 frequency: 4385 MHz
CPU 12 active residency:   2.49% (1260 MHz: .09% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz: .06% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz: 2.3%)
CPU 12 idle residency:  43.11%
CPU 12 down residency:  54.40%
CPU 13 frequency: 1260 MHz
CPU 13 active residency:   0.08% (1260 MHz: .08% 1512 MHz:   0% 1800 MHz:   0% 2088 MHz:   0% 2352 MHz:   0% 2616 MHz:   0% 2868 MHz:   0% 3096 MHz:   0% 3300 MHz:   0% 3468 MHz:   0% 3624 MHz:   0% 3756 MHz:   0% 3852 MHz:   0% 3924 MHz:   0% 3996 MHz:   0% 4044 MHz:   0% 4104 MHz:   0% 4416 MHz:   0% 4512 MHz:   0%)
CPU 13 idle residency:  45.52%
CPU 13 down residency:  54.40%

CPU Power: 41 mW
GPU Power: 2 mW
ANE Power: 0 mW
Combined Power (CPU + GPU + ANE): 43 mW

**** GPU usage ****

GPU HW active frequency: 338 MHz
GPU HW active residency:   1.21% (338 MHz: 1.2% 618 MHz:   0% 796 MHz:   0% 924 MHz:   0% 952 MHz:   0% 1056 MHz:   0% 1062 MHz:   0% 1182 MHz:   0% 1182 MHz:   0% 1312 MHz:   0% 1242 MHz:   0% 1380 MHz:   0% 1326 MHz:   0% 1470 MHz:   0% 1578 MHz:   0%)
GPU SW requested state: (P1 : 100% P2 :   0% P3 :   0% P4 :   0% P5 :   0% P6 :   0% P7 :   0% P8 :   0% P9 :   0% P10 :   0% P11 :   0% P12 :   0% P13 :   0% P14 :   0% P15 :   0%)
GPU SW state: (SW_P1 : 1.2% SW_P2 :   0% SW_P3 :   0% SW_P4 :   0% SW_P5 :   0% SW_P6 :   0% SW_P7 :   0% SW_P8 :   0% SW_P9 :   0% SW_P10 :   0% SW_P11 :   0% SW_P12 :   0% SW_P13 :   0% SW_P14 :   0% SW_P15 :   0%)
GPU idle residency:  98.79%
GPU Power: 2 mW
"""

pattern = "CPU [0-9]+ frequency: ([0-9]+)|CPU [0-9]+ active residency: +([0-9]+\.[0-9]+)"
raw_cpu = re.findall(pattern, data)

fetch_time = time.time()

cpu_utilization = {}
cpu_clock = {}
power = {}
gpu_utilization = {}
gpu_frequency = {}

# Parse the CPU utilization and clock rate
pattern = "CPU [0-9]+ frequency: ([0-9]+)|CPU [0-9]+ active residency: +([0-9]+\.[0-9]+)"
raw_cpu = re.findall(pattern, data)

temp_utilization = {}
temp_clock = {}

# parse each match
for i in range(0, len(raw_cpu), 2):
    cpu = i // 2
    temp_utilization[cpu] = raw_cpu[i + 1][1]
    temp_clock[cpu] = raw_cpu[i][0]

cpu_utilization[fetch_time] = temp_utilization
cpu_clock[fetch_time] = temp_clock

# Parse the power
pattern = "(CPU|GPU) Power: ([0-9]+)"
raw_power = re.findall(pattern, data)

power[fetch_time] = {"CPU": raw_power[0][1], "GPU": raw_power[1][1]}

# Parse the GPU
pattern = "GPU HW active frequency: ([0-9]+)|GPU HW active residency:   ([0-9]+.[0-9]+)"
raw_gpu = re.findall(pattern, data)

gpu_frequency[fetch_time] = raw_gpu[0][0]
gpu_utilization[fetch_time] = raw_gpu[1][1]

print(cpu_utilization)
print(cpu_clock)
print(power)
print(gpu_utilization)
print(gpu_frequency)


test = datalogger.Sampler()
test.start()

start = time.time()

time.sleep(10)


results = test.average_interval(start, time.time())
test.stop()

print(results)
df = pd.DataFrame(results)

print(df)



