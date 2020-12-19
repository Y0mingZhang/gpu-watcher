#!/usr/bin/python3
import os
import time
import argparse
import subprocess
from subprocess import PIPE

nvidia_smi_check = [
    'nvidia-smi', '--query-gpu=utilization.gpu,memory.free',
    '--format=csv'
]


def get_utilizaiton_and_memory():
    def s2f(s):
        return float(s.strip().split()[0])
    proc = subprocess.run(nvidia_smi_check, check=True, stdout=PIPE)
    nvidia_output = proc.stdout

    GPUs = {}
    for line in nvidia_output.decode().split('\n'):
        try:
            util, mem = line.split(',')
            GPUs[len(GPUs)] = s2f(util) / 100, s2f(mem)
        except:
            continue

    return GPUs


def available_GPUs(mem_needed):
    GPUs = get_utilizaiton_and_memory()
    return [i for i, (util, mem) in GPUs.items() if
            util <= 0.05 and mem >= mem_needed]


def main():
    parser = argparse.ArgumentParser(
        description='Waits for an available gpu and runs your job')
    parser.add_argument('cmd', metavar='CMD', type=str,
                        help='Command to run..')
    parser.add_argument('--refresh-rate', type=float, default=120,
                        help="Check for available gpu every X seconds")
    parser.add_argument('--n-gpus', type=int, default=1,
                        help="Number of GPUs to wait for")
    parser.add_argument('--mem', type=int, default=8000,
                        help="Memory needed per GPU in MB")
    args = parser.parse_args()

    SYS_TOTAL_GPU_NUM = len(get_utilizaiton_and_memory())
    if args.n_gpus > SYS_TOTAL_GPU_NUM or args.n_gpus < 1:
        raise ValueError("Invalid number of GPUs")

    if args.refresh_rate < 0:
        raise ValueError("Invalid refresh rate")

    if args.mem < 0:
        raise ValueError("Invalid memory specified")

    while True:
        GPUs = available_GPUs(args.mem)
        if len(GPUs) >= args.n_gpus:
            break
        time.sleep(args.refresh_rate)

    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
    os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(
        [str(gpu_id) for gpu_id in GPUs[0:args.n_gpus]])
    print("*** Start running \"{}\" on GPU {} ***".format(args.cmd,
            os.environ["CUDA_VISIBLE_DEVICES"]))

    subprocess.run(args.cmd, check=True, env=os.environ.copy(), shell=True)


if __name__ == "__main__":
    main()
