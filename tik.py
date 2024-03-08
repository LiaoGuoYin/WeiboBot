from WeiboBot import Bot
from WeiboBot.message import Chat
from WeiboBot.weibo import Weibo
from WeiboBot.comment import Comment
from dotenv import load_dotenv

import os
import time
from datetime import datetime

from GPT.api import *


load_dotenv()
myBot = Bot(cookies=os.getenv("BOT_COOKIES"))


@myBot.onNewWeibo  # 首页刷到时触发
async def on_weibo(weibo: Weibo):
    if weibo.original_weibo is None:  # 原创
        print(f"{weibo.text}")


@myBot.onNewMsg  # 被私信的时候触发
async def on_msg(chat: Chat):
    for msg in chat.msg_list:  # 消息列表
        await myBot.login()
        print(f"{msg.sender_screen_name}:{msg.text}")
        reply = no_matter_bot(msg.text, prompt=REPLY_PROMPT)
        print(msg.text, reply)
        await myBot.send_message(msg.sender_id, reply)


@myBot.onMentionCmt  # 提及我的评论时触发
async def on_mention_cmt(cmt: Comment):
    reply = no_matter_bot(cmt.text)
    await myBot.comment_weibo(cmt.mid, reply)
    print(cmt.text, reply)


@myBot.onTick  # 每次循环触发
async def on_tick():
    if datetime.now().minute == 0:
        print("hit tik, post now")
        await myBot.login()
        await myBot.post_weibo(no_matter_bot(message=AUTO_PROMPT, prompt=''))
        time.sleep(60)


if __name__ == "__main__":
    myBot.run()
