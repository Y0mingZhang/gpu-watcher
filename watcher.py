import os
import time
import argparse
import subprocess
from subprocess import PIPE

nvidia_smi_check = [
    'nvidia-smi', '--query-gpu=utilization.gpu,utilization.memory',
    '--format=csv'
]


def get_utilizaiton_and_memory():
    def p2f(p):
        return float(''.join(p.split()).strip('%')) / 100
    proc = subprocess.run(nvidia_smi_check, check=True, stdout=PIPE)
    nvidia_output = proc.stdout

    GPUs = {}
    for line in nvidia_output.decode().split('\n'):
        try:
            util, mem = line.split(',')
            GPUs[len(GPUs)] = p2f(util), p2f(mem)
        except:
            continue

    return GPUs


def available_GPUs(util_max=0.01, mem_max=0.25):
    GPUs = get_utilizaiton_and_memory()
    return [i for i, (util, mem) in GPUs.items() if
            util <= util_max and mem <= mem_max]


def main():
    parser = argparse.ArgumentParser(
        description='Waits for an available gpu and runs your job')
    parser.add_argument('cmd', metavar='CMD', type=str,
                        help='Command to run..')
    parser.add_argument('--refresh-rate', type=float, default=120,
                        help="Check for available gpu every X seconds")
    parser.add_argument('--n-gpus', type=int, default=1,
                        help="Number of GPUs to wait for")
    args = parser.parse_args()

    SYS_TOTAL_GPU_NUM = len(get_utilizaiton_and_memory())
    if args.n_gpus > SYS_TOTAL_GPU_NUM or args.n_gpus < 1:
        raise ValueError("Invalid number of GPUs")

    if args.refresh_rate < 0:
        raise ValueError("Invalid refresh rate")

    while True:
        GPUs = available_GPUs()
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
