import asyncio
import concurrent.futures
import time


def blocks(n):
    print('running')
    time.sleep(0.1)
    print('done')
    return n ** 2


async def run_blocking_tasks(executor, i):
    loop = asyncio.get_event_loop()
    print('waiting for executor tasks')
    result = await loop.run_in_executor(executor, blocks, i)
    return result



async def main():

    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    futures = [run_blocking_tasks(executor, i) for i in range(6)]
    results = await asyncio.gather(*futures)
    print(results)


asyncio.run(main())