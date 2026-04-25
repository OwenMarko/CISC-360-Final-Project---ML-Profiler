This will work on MacOS and Linux.

Mac requires the powermetrics package.
Linux requires nvidia-smi and turbostat packages.

On line 55 in main you must select the type of device to run the test on, either cpu, cuda, or mps. mps is for apple gpu, cuda for linux gpu, and cpu for cpu.


Required ENV variable:

SUDO_PASSWORD = password to execute admin commands in terminal.