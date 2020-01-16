import queue
import time
from flask import Flask
from pynvml import *

AVAILABLE_GPUs = queue.Queue()
MAX_GPUs = 3

app = Flask(__name__)

def get_available_gpu(gpu_queue):
    nvmlInit()
    deviceCount = nvmlDeviceGetCount()

    available_ids = []

    for i in range(0, deviceCount):
        handle = nvmlDeviceGetHandleByIndex(i)
        if nvmlDeviceGetMemoryInfo(handle).free > int(1.1 * 1e10) \
           and gpu_queue.qsize() < MAX_GPUs:
            print(i, nvmlDeviceGetMemoryInfo(handle).free)
            gpu_queue.put(i)

    nvmlShutdown()

    print('Available GPUs:', gpu_queue.qsize())


@app.route('/allocate_gpu', methods=['GET'])
def allocate_gpu():
    retry_times = 3
    while AVAILABLE_GPUs.empty() and retry_times > 0:
        get_available_gpu(AVAILABLE_GPUs)
        if AVAILABLE_GPUs.empty():
            time.sleep(1)
        retry_times -= 1

    if AVAILABLE_GPUs.empty():
        return '-1', 408
    else:
        return str(AVAILABLE_GPUs.get()), 200
        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=2048)
