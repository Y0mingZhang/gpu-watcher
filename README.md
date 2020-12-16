 gpu-watcher 
==============================
A tool that waits for available GPU(s) and run your job on them.
## setup
The code is tested with Python>=3.6
## usage
```shell
python3 watcher.py [--refresh-rate REFRESH_RATE] [--n-gpus N_GPUS] <CMD>
```
## example
```
$ python3 watcher.py "python3"
*** Start running python3 on GPU 0 ***
Python 3.8.2 (default, Apr 27 2020, 15:53:34) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```


