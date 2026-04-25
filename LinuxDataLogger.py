import re
import subprocess
import threading
import time

class Sampler:
    def __init__(self):
        # sample arrays
        self.cpu_utilization = {}
        self.gpu_utilization = {}
        self.gpu_frequency = {}
        self.cpu_clock = {}
        self.power = {}

        self._thread = None
        self._stop_event = threading.Event()

    # start sampling on a new thread
    def start(self):
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._analysis_loop, daemon=True)
        self._thread.start()

    # stop sampling
    def stop(self):
        self._stop_event.set()
        self._thread.join()

    # reset the arrays
    def reset(self):
        self.cpu_utilization = {}
        self.gpu_utilization = {}
        self.gpu_frequency = {}
        self.cpu_clock = {}
        self.power = {}

    def _analysis_loop(self):
        pass

    def get_gpu_stats(self):
        result = subprocess.run([
            "nvidia-smi",
            "--query-gpu=utilization.gpu,power.draw,clocks.sm",
            "--format=csv,noheader,nounits"
        ],
            capture_output=True, text=True
        )
        gpu_utilization, gpu_power, gpu_frequency = result.stdout.split(", ")
        return float(gpu_utilization), float(gpu_power), float(gpu_frequency)

    # get the average metrics over a time interval
    def average_interval(self, start: time, end: time) -> dict:
        # CPU Utilization
        reduced_cpu_utilization = {read_time: cpu_data for read_time, cpu_data in self.cpu_utilization.items() if
                                   start <= read_time <= end}
        # variables for calculating average
        count = 0
        average_cpu_utilization = {}

        # loop through and parse each CPU core
        for cpu_dict in reduced_cpu_utilization.values():
            count += 1

            for key, value in cpu_dict.items():
                if key not in average_cpu_utilization.keys():
                    average_cpu_utilization[key] = value
                else:
                    average_cpu_utilization[key] = (average_cpu_utilization[key] * (count - 1) + value) / count

        # CPU Clock
        reduced_cpu_clock = {read_time: cpu_data for read_time, cpu_data in self.cpu_clock.items() if
                             start <= read_time <= end}
        average_cpu_clock = {}

        # loop through and parse each CPU core
        for cpu_dict in reduced_cpu_clock.values():
            count += 1

            for key, value in cpu_dict.items():
                if key not in average_cpu_clock.keys():
                    average_cpu_clock[key] = value
                else:
                    average_cpu_clock[key] = (average_cpu_clock[key] * (count - 1) + value) / count

        # Average Power
        reduced_cpu_power = [value["CPU"] for read_time, value in self.power.items() if start <= read_time <= end]
        reduced_gpu_power = [value["GPU"] for read_time, value in self.power.items() if start <= read_time <= end]
        try:
            average_cpu_power = sum(reduced_cpu_power) / len(reduced_cpu_power)
            average_gpu_power = sum(reduced_gpu_power) / len(reduced_gpu_power)
        except ZeroDivisionError:
            print("No values for this interval")
            return

        # Average GPU utilization
        reduced_gpu_utilization = [value for read_time, value in self.gpu_utilization.items() if
                                   start <= read_time <= end]
        average_gpu_utilization = sum(reduced_gpu_utilization) / len(reduced_gpu_utilization)

        # Average GPU Clock
        reduced_gpu_frequency = [value for read_time, value in self.gpu_frequency.items() if
                                 start <= read_time <= end]
        average_gpu_frequency = sum(reduced_gpu_frequency) / len(reduced_gpu_frequency)

        return {
            "cpu-utilization": average_cpu_utilization,
            "cpu-frequency": average_cpu_clock,
            "cpu-power": average_cpu_power,
            "gpu-power": average_gpu_power,
            "gpu-utilization": average_gpu_utilization,
            "gpu-frequency": average_gpu_frequency,
        }