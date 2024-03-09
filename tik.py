from WeiboBot import Bot
from WeiboBot.message import Chat
from WeiboBot.weibo import Weibo
from WeiboBot.comment import Comment
from WeiboBot.util import *

import os
import time
from datetime import datetime
from dotenv import load_dotenv

from GPT.api import *


load_dotenv()
myBot = Bot(cookies=os.getenv("BOT_COOKIES"))


@myBot.onNewWeibo  # 首页刷到时触发
async def on_weibo(weibo: Weibo):
    print(weibo.weibo_id)
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
    reply_content = no_matter_bot(cmt.text)
    await myBot.reply_weibo(cmt.status["id"], cmt.mid, reply_content)


@myBot.onTick  # 每次循环触发
async def on_tick():
    if datetime.now().minute == 0:
        print("hit tik, post now")
        await myBot.login()
        reply = await search_weibo_and_reply()
        await myBot.post_weibo(reply)
        time.sleep(60)
    elif datetime.now().minute % 21 == 0: # every  xx:21 xx:42
        await myBot.login()
        await search_weibo_and_reply()
        time.sleep(60)


async def search_weibo_and_reply(message="累"):
    result_list = await myBot.search_weibo(message)
    for result in result_list:
        result.text = remove_html_tags_in(result.raw_text)
        result_len = len(result.text)
        if result_len > 10 and result_len < 100:
            reply_text = no_matter_bot(result.text, prompt=REPLY_PROMPT)
            # input(f"reply to {result.mid} {result.text} -> {reply_text}")
            cmt = await myBot.comment_weibo(result.mid, reply_text)
            print("search and reply done")
            return reply_text
            # if cmt.status == "ok":  # else 作者只允许粉丝评 etc.


if __name__ == "__main__":
    myBot.run()
