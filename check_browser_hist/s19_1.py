import time
from concurrent.futures import ThreadPoolExecutor

def download_img(url):
    print("下载图片:{}".format(url))
    time.sleep(1)
    print("下载完成:{}".format(url))

def main():
    executer = ThreadPoolExecutor(5)
    for i in range(10):
        executer.submit(download_img,i)

main()