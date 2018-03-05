"""
Subroutines are: functions
Co-routines are: asyncronous functions

"""
import asyncio
import concurrent.futures
import requests
import time


NUM_REQ = 15
ENDPOINT = 'https://jsonplaceholder.typicode.com/posts/1'


def time_synced():
    begin = time.time()
    for i in range(1, NUM_REQ):
        start = time.time()
        [requests.get(ENDPOINT) for _ in range(i)]
        time_bars = int((time.time() - start) * 10)
        print(f"{i}\t{'#' * time_bars}")
    total = time.time() - begin
    return total


async def time_asynced_loop():
    for i in range(1, NUM_REQ):
        start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            loop = asyncio.get_event_loop()
            futures = [
                loop.run_in_executor(executor, requests.get, ENDPOINT)
                for _ in range(i)
            ]
            responses = [resp.json() for resp in await asyncio.gather(*futures)]
            print(len(responses))
        time_bars = int((time.time() - start) * 10)
        print(f"{i}\t{'#' * time_bars}")


def time_asynced():
    begin = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(time_asynced_loop())
    total = time.time() - begin
    return total


if __name__ == '__main__':
    print(f'Synced total time: {time_synced():.2f} seconds\n')
    print(f'Asynced total time: {time_asynced():.2f} seconds\n')

