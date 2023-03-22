import asyncio
from functools import partial
async def func(num):
    await asyncio.sleep(2)
    return num

def callback(some_str_param, task):
    print("from callback:{}, other param:{}".format(task.result(), some_str_param))

async def main():
    tasks = [
        asyncio.create_task(func(i)) for i in range(5)
    ]
    for task in tasks:
        task.add_done_callback(callback)

    await asyncio.wait(tasks)
    print("main function end")



asyncio.run(main())