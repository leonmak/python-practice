import asyncio
from aiohttp import ClientSession, TCPConnector

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.json()

async def run(r):
    futures = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    connector = TCPConnector(verify_ssl=False)
    async with ClientSession(connector=connector) as session:
        for i in range(r):
            url = f'https://jsonplaceholder.typicode.com/posts/{i}'
            future = asyncio.ensure_future(fetch(url, session))
            futures.append(future)
        responses = await asyncio.gather(*futures)
        print(responses)
        return responses

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(4))