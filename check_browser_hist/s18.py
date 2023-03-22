from concurrent.futures import Future
from concurrent.futures import ThreadPoolExecutor
import time

def task(a,b):
    time.sleep(2)
    return a+b

def callback(f:Future):
    print(f.result())

pool = ThreadPoolExecutor(5)

for i in range(5):
    pool.submit(task,i,i).add_done_callback(callback)
