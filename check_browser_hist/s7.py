import requests
import time

def downloadImg(url):
    file_name = url.split('/')[-1]
    print(f"下载图片{file_name}")
    time.sleep(2)
    response = requests.get(url)
    with open(file_name, mode='wb') as file:
        file.write(response.content)
    print(f"下载完成{file_name}")

def main():
    urls=[
        "http://p0.ssl.qhmsg.com/t01da1e4ef25adfd30a.jpg",
        "http://p0.ssl.qhmsg.com/t01b7147847671571d5.jpg",
        "http://alifei05.cfp.cn/creative/vcg/veer/1600water/veer-326829994.jpg"
    ]
    for item in urls:
        downloadImg(item)

main()