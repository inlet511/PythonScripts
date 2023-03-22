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
    result1 = await func1()
    print(result1)
    result2 = await func2()
    print(result2)
    print('main function end')

asyncio.run(main())
