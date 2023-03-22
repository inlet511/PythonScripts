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
    task1 = asyncio.create_task(func1())
    task2 = asyncio.create_task(func2())
    result1 = await task1
    result2 = await task2
    print(result1)
    print(result2)
    print("main function end")

asyncio.run(main())