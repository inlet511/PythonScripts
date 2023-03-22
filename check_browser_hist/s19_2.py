import time
import asyncio
from concurrent.futures import ThreadPoolExecutor

def download_img(url):
    print("下载图片:{}".format(url))
    time.sleep(1)
    print("下载完成:{}".format(url))

def main():
    executer = ThreadPoolExecutor(5)
    loop = asyncio.get_event_loop()
    tasks=[]
    for i in range(10):
        t = loop.run_in_executor(executer, download_img, i)
        tasks.append(t)

    await asyncio.wait(tasks)

asyncio.run(main())