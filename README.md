## WeiboBot

基于微博H5 API开发的机器人框架

WeiboBot 是一个基于微博H5 API开发的机器人框架，提供了一个简单的接口，可以让你的机器人更加简单的接入微博，并且提供了一些简单的指令，比如：转评赞，回复消息等

## 开始使用(事件驱动模式)

```python
from WeiboBot import Bot
from WeiboBot.message import Chat
from WeiboBot.weibo import Weibo
from WeiboBot.comment import Comment

from datetime import datetime

cookies = "your cookies"
myBot = Bot(cookies=cookies)


@myBot.onNewMsg  # 被私信的时候触发
async def on_msg(chat: Chat):
    for msg in chat.msg_list:  # 消息列表
        print(f"{msg.sender_screen_name}:{msg.text}")


@myBot.onNewWeibo  # 首页刷到新微博时触发
async def on_weibo(weibo: Weibo):
    if weibo.original_weibo is None:  # 是原创微博
        print(f"{weibo.text}")


@myBot.onMentionCmt  # 提及我的评论时触发
async def on_mention_cmt(cmt: Comment):
    print(f"{cmt.text}")


@myBot.onTick  # 每次循环触发
async def on_tick():
    print(datetime.now())


if __name__ == '__main__':
    myBot.run()

```

## 开始使用(主动模式)

```python
from WeiboBot import Bot
from WeiboBot.const import *
import asyncio

cookies = "your cookies"
myBot = Bot(cookies=cookies)


async def main():
    await asyncio.wait_for(myBot.login(), timeout=10)  # 先登录
    weibo_example1 = myBot.get_weibo(123456789)  # 获取微博
    weibo_example2 = myBot.post_weibo("发一条微博", visible=VISIBLE.ALL)
    # ...... 其他操作


if __name__ == '__main__':
    asyncio.run(main())

```

## .env.example

```shell
BOT_COOKIES="" # 被动模式 COOKIE
ACCOUNT1_COOKIES="" # 主动模式 COOKIE

GPT_API_URL="https://api.openai.com/v1/chat/completions" # GPT API EndPoint, 可替换为中转地址
GPT_API_KEY="sk-xxxxxxxx" # GPT API Key
```

## 如何获取cookie

登录m.weibo.cn

按F12查看请求头

![image](https://user-images.githubusercontent.com/37311477/164148500-c6a19f75-d1fd-48e6-9850-6c5380847dcd.png)
