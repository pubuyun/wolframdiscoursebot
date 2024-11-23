import asyncio

import aiohttp
from aiohttp import ClientConnectionError

import json
from urllib.parse import urljoin

class LoopMngr:
  def __init__(self, server_url, handle_post, loop):
    self.handle_msg = handle_post
    self.last_gotten_posts = []
    self.server_url = server_url
    self.asyncio_loop = loop
    self.processed_posts = set() 
  
  async def start(self):
    get_post_data_uri = urljoin(self.server_url, "/posts.json")
    if self.asyncio_loop is None:
        self.asyncio_loop = asyncio.get_event_loop()

    async with aiohttp.ClientSession() as session:
        first = True
        while True:
            try:
                async with session.get(get_post_data_uri) as resp:
                    if resp.status != 200:
                        print("Error:", resp.status)
                        await asyncio.sleep(10)
                        continue

                    data = await resp.json()
                    if first:
                        self.processed_posts.update(post['id'] for post in data['latest_posts'])
                        first = False

                    new_posts = [post for post in data['latest_posts'] if post['id'] not in self.processed_posts]
                    tasks = [asyncio.create_task(self.handle_msg(post)) for post in new_posts]
                    self.processed_posts.update(post['id'] for post in new_posts)
                    await asyncio.gather(*tasks)

            except asyncio.TimeoutError:
                print("Timeout")
            except ClientConnectionError:
                break
            except Exception as e:
                print(f"Error: {e}")
            finally:
                await asyncio.sleep(4)


__all__ = ['LoopMngr']