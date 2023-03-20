import os
import sqlite3
import asyncio
import aiohttp

result_list=[]

async def check_keywords(session, url,file):
    print(url)
    response = await session.get(url, ssl=False)
    if '并行' in (await response.text()):
        file.write(url)


def get_list():
    # path to user's history database (Chrome)
    data_path = r'C:\Users\Ken\AppData\Local\Google\Chrome\User Data\Default'
    files = os.listdir(data_path)

    history_db = os.path.join(data_path, 'history')

    # querying the db
    c = sqlite3.connect(history_db)
    cursor = c.cursor()

    select_statement = "SELECT urls.url FROM urls WHERE last_visit_time > strftime('%s','now','-1 month');"
    cursor.execute(select_statement)
    browse_history = cursor.fetchall()  # tuple
    browse_history_list = []
    for r in browse_history:
        browse_history_list.append(r[0])

    return browse_history_list

async def main(file):
    # 找出时间段内的网址
    browser_history_list = get_list()
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(check_keywords(session, url, file)) for url in browser_history_list]
        await asyncio.wait(tasks)

if __name__ == '__main__':
    with open('list.txt','w') as file:
        asyncio.run(main(file))
