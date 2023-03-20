import asyncio
import aiohttp

async def downloadImg(session, url):
    file_name = url.split('/')[-1]
    print(f"下载图片{file_name}")
    response = await session.get(url, ssl=False)
    content = await response.content.read()
    with open(file_name, mode='wb') as file:
        file.write(content)
    print(f"下载完成{file_name}")

async def main():
    urls=[
        "http://p0.ssl.qhmsg.com/t01da1e4ef25adfd30a.jpg",
        "http://p0.ssl.qhmsg.com/t01b7147847671571d5.jpg",
        "http://alifei05.cfp.cn/creative/vcg/veer/1600water/veer-326829994.jpg"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(downloadImg(session,url)) for url in urls]
        await asyncio.wait(tasks)

if __name__ == '__main__':
    asyncio.run(main())
