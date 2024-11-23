import os
import asyncio

import aiohttp
from aiohttp import ClientConnectionError
from .loop import LoopMngr


from urllib.parse import urljoin
import json

import datetime

class API:
  def __init__(self, loop:LoopMngr, token, username):
    self.loop = loop
    self.session = None
    self.base_url = loop.server_url
    self._token = token
    self._username = username

  async def async_init(self):
    self.session = aiohttp.ClientSession(loop=self.loop.asyncio_loop, headers={
      'Api-Key':self._token.strip(), 
      "Api-Username":self._username.strip() 
    })
  
  async def send_post(self, msg, where=None, extra_data=None):
    try:
      data= {
        "raw": msg,
        "topic_id": where,
        "created_at": str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"))
      }

      if data['topic_id'] is None:
        del data["topic_id"]
        
      if extra_data is not None:
        data.update(extra_data)

      async with self.session.post(urljoin(self.base_url, "/posts.json"), json=data) as resp:
        if resp.status == 200:
          return await resp.json()
        else:
          print(await resp.text())
          return None
                  
    except asyncio.TimeoutError:
      pass #ignore 

    except ClientConnectionError:
      pass #ignoreing 

    except Exception as e:
       print(f'Error: {e.__class__.__name__}: {e}') 


  async def create_topic(self, title, post, category, extra_data=None):
      data= {
        "title": title,
        "category": category,
      }
  
      if extra_data is not None:
        data.update(extra_data)

      return await self.send_post(post, 0, extra_data=data)

  async def send_private(self, msg, users, extra_data=None):
    data= {
      "target_recipients":",".join(users)
    }
    if extra_data is not None:
      data.update(extra_data)

    return await self.send_post(msg, None, data)

  async def create_private(self, msg, users, extra_data=None):
    data= {
      "archetype": "private"
    }
    
    if extra_data is not None:
      data.update(extra_data)
    
    return await self.send_private(msg, users, data)

  async def upload_image(self, image_path):
        """
        上传图片到服务器
        Args:
            image_path (str): 图片的本地路径
        Returns:
            dict: 上传结果，包括 id 和 url
        """
        upload_url = urljoin(self.base_url, "/uploads.json")
        try:
            with open(image_path, 'rb') as image_file:
                # 构建 multipart/form-data 数据
                data = aiohttp.FormData()
                data.add_field("type", "composer")
                data.add_field("synchronous", "true")
                data.add_field("file", image_file, filename=image_path)

                async with self.session.post(upload_url, data=data) as response:
                    if response.status == 200:
                        return await response.json()  # 返回响应中的 JSON 数据
                    else:
                        print(f"Image upload failed: {response.status}, {await response.text()}")
                        return None
        except Exception as e:
            print(f"Error uploading image: {e}")
            return None
__all__ = [
  'API'
]