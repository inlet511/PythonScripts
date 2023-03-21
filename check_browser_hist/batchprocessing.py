import asyncio
import aiohttp

async def fetch_urls(session, urls):
    results = []
    for url in urls:
        async with session.get(url) as response:
            result = await response.text()
            results.append(result)
    return results

async def process_batches(session, urls, batch_size):
    num_batches = (len(urls) + batch_size - 1) // batch_size
    for i in range(num_batches):
        start = i * batch_size
        end = min((i + 1) * batch_size, len(urls))
        batch_urls = urls[start:end]
        batch_results = await fetch_urls(session, batch_urls)
        # do something with batch_results, such as write to a file or database

async def main():
    urls = ['http://example.com/' + str(i) for i in range(10000)]
    async with aiohttp.ClientSession() as session:
        await process_batches(session, urls, batch_size=50)

if __name__ == '__main__':
    asyncio.run(main())
