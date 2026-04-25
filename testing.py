import time

import LinuxDataLogger


testLogger = LinuxDataLogger.Sampler()

now = time.time()

testLogger.get_cpu_stats(now)
testLogger.get_gpu_stats(now)
print(testLogger.average_interval(now, now))