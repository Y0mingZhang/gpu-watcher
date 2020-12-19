 gpu-watcher 
==============================
A tool that waits for available GPU(s) and run your job on them.
## setup
The code is tested with Python>=3.6
## usage
```
usage: watcher.py [-h] [--refresh-rate REFRESH_RATE] [--n-gpus N_GPUS] [--mem MEM] <CMD>

Waits for an available gpu and runs your job

positional arguments:
  CMD                   Command to run..

optional arguments:
  -h, --help            show this help message and exit
  --refresh-rate REFRESH_RATE
                        Check for available gpu every X seconds
  --n-gpus N_GPUS       Number of GPUs to wait for
  --mem MEM             Memory needed per GPU in MB
```
## example
```shell
$ python3 watcher.py "python3"
*** Start running python3 on GPU 0 ***
Python 3.8.2 (default, Apr 27 2020, 15:53:34) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```


```shell
$ python3.7 watcher.py --n-gpus 3 "python3.7 distilbert.py"
*** Start running "python3.7 distilbert.py" on GPU 2,4,7 ***
I1219 11:49:41.628771 140592451467008 file_utils.py:39] PyTorch version 1.5.0 available.
```
