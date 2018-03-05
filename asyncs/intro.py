"""
Async-Await are: fancy generators that we call coroutines and there is some
support for awaitable objects and turning plain generators in to coroutines
Co-routines are: asynchronous functions defined by `async def`
Subroutines are: functions

asyncio is: an event loop / message dispatcher framework
~ similar to promises in JS, reduces use of callbacks with await
"""
import asyncio
import concurrent.futures
import datetime
import logging
import sys
import time

import aiofiles
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(threadName)10s %(name)18s: %(message)s',
    stream=sys.stderr,
)


async def load_file(path):
    async with aiofiles.open(path, 'r') as f:
        contents = await f.read()
        return contents


# p3.4 Decorators - use `yield from` to call an `async def` function
@asyncio.coroutine
def get_json_decorator(client, url):
    # for x in iterator:
    #     yield x
    file_content = yield from load_file('.gitignore')


# p3.5 Async-await
async def get_json(client, url):
    # await is called on an Awaitable object:
    # coroutine or an object that defines an __await__() method
    # which returns an iterator which is not a coroutine itself
    return await load_file('.gitignore')


# hello world
async def hello_world_async(sec):
    print(f'In {sec} sec..')
    await asyncio.sleep(sec)
    print("Hello World!")


async def display_date(loop, sec):
    end_time = loop.time() + sec
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

# chain
async def chain_async():
    async def inner_chain(sec):
        await hello_world_async(sec)
    await inner_chain(2)


# multi-threaded (shown in logs)
def blocking_get(n):
    log = logging.getLogger('blocks({})'.format(n))
    url = f'https://jsonplaceholder.typicode.com/posts/{n}'
    log.info('running')
    time.sleep(0.1 * (3-n))
    response = requests.get(url)
    log.info('done')
    return response

async def run_blocking_tasks(exc, n):
    print('entering inner loop')
    inner_loop = asyncio.get_event_loop()
    # use blocking in run_in_executor
    futures = [inner_loop.run_in_executor(exc, blocking_get, i)
               for i in range(n)]
    # blocks until all futures finish
    responses = await asyncio.gather(*futures)
    # print(responses)
    results = [response.json() for response in responses]
    print('exiting inner loop')
    return results


if __name__ == '__main__':
    outer_loop = asyncio.get_event_loop()
    # `run_until_complete` takes in a coroutine / called async function
    outer_loop.run_until_complete(hello_world_async(1))
    # Blocks next line until coroutine is done
    outer_loop.run_until_complete(display_date(outer_loop, 2))

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            # Can't use async in `run_in_executor`
            # outer_loop.run_in_executor(executor, hello_world_async, 1)
            res = outer_loop.run_until_complete(run_blocking_tasks(executor,3))
            print(res)
        print('closing')
    finally:
        outer_loop.close()
