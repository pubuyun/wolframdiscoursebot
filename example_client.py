from src import bot
from src import wolfram
from os import environ as env


Bot = bot("discourse_account_name", "discourse_api_name")

async def reply_to_mentions(args, raw, bot: bot = Bot):
    # 获取帖子内容和作者
    post = raw
    username = post['username']
    raw_content = post['raw']
    print("post detected")
    # 检查是否被提到
    if bot.username in raw_content or f"@{bot.username}" in raw_content:
        print(f"被提到: {username} 说: {raw_content}")
        index = raw_content.find(f"@{bot.username}")
        # 提取 @bot.username 后的内容，去掉多余的空格
        prompt = raw_content[index + len(f"@{bot.username} "):].strip()
        # api 
        imagepath = wolfram.query_simple_api(prompt)
        if imagepath is not None:
            # 回复
            image_path = imagepath  # 替换为你的图片路径
            image_url = await bot.api.upload_image(image_path)
            print(image_url)
            image_url = image_url.get("url")
            reply_content = f"![Result]({image_url})"
            await bot.api.send_post(reply_content, post['topic_id'])
        else:
            await bot.api.send_post("请求错误，请稍后再试", post['topic_id'])

# 注册回调
Bot.callback(reply_to_mentions, "post")

# 启动机器人
Bot.run()


