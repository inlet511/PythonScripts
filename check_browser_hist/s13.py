import asyncio
async def func(inNum):
    return inNum

async def main():
    task_list = [asyncio.create_task(func(i)) for i in range(5)]
    # done, pending = await asyncio.wait(task_list)
    ret = await asyncio.gather(*task_list)
    print(ret)

asyncio.run(main())