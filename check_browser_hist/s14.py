import asyncio

async def func(num):
    return num

async def main():
    tasklist=[
        asyncio.ensure_future(func(i)) for i in range(5)
    ]

    result = asyncio.gather(*tasklist)
    print(result)

if __name__=='__main__':
    asyncio.run(main())