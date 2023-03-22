import asyncio

async def func1():
    print('func1 started')
    await asyncio.sleep(2)
    print('func1 end')
    return 1

async def func2():
    print('func2 started')
    await asyncio.sleep(2)
    print('func2 end')
    return 2

async def main():
    task_list = [
        asyncio.create_task(func1()),
        asyncio.create_task(func2())
    ]
    done, pending = await asyncio.wait(task_list)

    for t in done:
        print(t.result())

asyncio.run(main())