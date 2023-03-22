import os
import sqlite3
import asyncio
import aiohttp

# 一次同时访问的url数量
BATCH_SIZE = 20

# 超时时间
TIMEOUT = 15

# 不要检查这些域名，确定他们中没有我想要的内容
exclude_domains = [
    'google.com',
    'youtube.com',
    'bilibili.com',
    'baidu.com',
    'chat.openai.com',
    'chat.forchange.cn',
    'xxxxx520.com',
    'shadowsocks.au',
    'taobao.com',
    'tmall.com',
    'jd.com',
    'github.com',
    'gitee.com',
    'download.qt.io',
    'opencascade.org',
    'opencascade.com',
    'courser.org',
    'inlet511.github.io',
    'unrealengine.com',
    'nvidia.com',
    'ke.qq.com',
    'pytorch.org',
    'ddys.art',
    'githubusercontent.com',
    'download-archive',
    'bybit.com',
    'coursera.org',
    'epicgames.com',
    'rrcg.cn',
    'toutiao.com',
    'civitai.com',
    'huggingface.co',
    'opencv.org',

]

async def check_keywords(session, url, result_file, skipped_file):
    print(f"访问URL:{url}")
    proxy = "http://127.0.0.1:7890"
    try:
        response = await asyncio.wait_for(session.get(url, ssl=False, proxy=proxy),
                                          timeout=TIMEOUT)  # Adjust timeout as needed
        response_text = await response.read()
        if '并行' in response_text.decode('utf-8', 'ignore') and '并发' in response_text.decode('utf-8', 'ignore'):
            result_file.write(f"{url}\n")
    except asyncio.TimeoutError:
        print(f"超时跳过: {url}")
        skipped_file.write(f"{url}\n")




def get_list():
    # path to user's history database (Chrome)
    data_path = r'C:\Users\Ken\AppData\Local\Google\Chrome\User Data\Default'
    files = os.listdir(data_path)

    history_db = os.path.join(data_path, 'history')

    # querying the db
    try:
        c = sqlite3.connect(history_db)
        cursor = c.cursor()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        cursor = None

    select_statement = "SELECT urls.url FROM urls WHERE last_visit_time > strftime('%s','now','-1 month');"
    cursor.execute(select_statement)
    browse_history = cursor.fetchall()  # tuple
    browse_history_list = []
    for r in browse_history:
        # 跳过一些域名
        if not any(domain in r[0] for domain in exclude_domains):
            browse_history_list.append(r[0])

    return browse_history_list


async def main(result_file, skipped_file):
    # 找出时间段内的网址
    browser_history_list = get_list()
    list_count = len(browser_history_list)
    batch_count = (list_count + BATCH_SIZE - 1) // BATCH_SIZE

    async with aiohttp.ClientSession() as session:
        for i in range(batch_count):
            start_index = i * BATCH_SIZE
            end_index = min((i + 1) * BATCH_SIZE, list_count)
            batch_urls = browser_history_list[start_index:end_index]
            tasks = [asyncio.create_task(check_keywords(session, url, result_file, skipped_file)) for url in batch_urls]
            await asyncio.wait(tasks)
            print(f"Total URLs: {list_count}")
            print(f"Batch {i + 1} completed. {batch_count - i - 1} batches remaining. Batch size:{BATCH_SIZE}")



if __name__ == '__main__':
    with open('list.txt', 'w') as file, open('skipped.txt', 'w') as skipped_file:
        asyncio.run(main(file, skipped_file))
