import asyncio
import aiohttp

urls = ['http://www.google.com', 'http://www.python.org', 'http://duckduckgo.com']

async def call_url(url):
    print(f'Starting {url}')
    responce = await aiohttp.ClientSession().get(url)
    data = await responce.text()
    print(f'{url} bytes:{len(data)} {data[:200]}')
    return data


loop = asyncio.get_event_loop()

futures = [call_url(url) for url in urls]

results = loop.run_until_complete(asyncio.gather(*futures))
print(f'futures: {futures}')
print(f'asyncio.gather(*futures): {asyncio.gather(*futures)}')
print(f"results: {results}")
loop.close()