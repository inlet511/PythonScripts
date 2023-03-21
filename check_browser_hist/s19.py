import time

def download_img(url):
    print("下载图片:{}".format(url))
    time.sleep(1)
    print("下载完成:{}".format(url))

def main():
    for i in range(10):
        download_img(i)

main()