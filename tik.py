import os
import random
from WeiboBot import Bot
from WeiboBot.message import Chat
from WeiboBot.weibo import Weibo
from WeiboBot.comment import Comment
from dotenv import load_dotenv

import os
import time
from datetime import datetime


load_dotenv()
myBot = Bot(cookies=os.getenv("BOT_COOKIES"))

message_list = [
    "没关系，能写几行代码已经很厉害了",
    "没关系，今天也在学习英文，你是最棒的",
    "没关系，能保持微笑已经很厉害了",
    "没关系，能留些时间给自己独处，好厉害呀",
    "没关系，一个人也能观赏电影，很厉害了",
    "没关系，跑了几步已经很厉害了",
    "没关系，能吃到自己喜欢的食物，真的很厉害了",
    "没关系，认识到自己需要休息，这很厉害",
    "没关系，在办公室又坚持了一天，很厉害了",
    "没关系，能打开PowerPoint已经很厉害了",
    "没关系，起身出门走了一小段，已经很厉害了",
    "没关系，整理出一份待办清单，很厉害了",
    "没关系，敢于面对自己的情绪，真的很厉害",
    "没关系，给朋友打了个电话，这太厉害了",
    "没关系，学习接受自己的不完美，很厉害了",
    "没关系，能读一篇科技文章，很厉害了",
    "没关系，对着镜子给自己微笑，你很棒",
    "没关系，能舒舒服服的睡一觉，很厉害了",
    "没关系，看了一本书，很好的",
    "没关系，给自己下了个单，这很奇妙，很厉害",
    "没关系，尝试学习画画已经很厉害了",
    "没关系，能照顾自己，这真的很厉害",
    "没关系，尽管沮丧，你还在持续，这真的很厉害",
]


@myBot.onNewMsg  # 被私信的时候触发
async def on_msg(chat: Chat):
    for msg in chat.msg_list:  # 消息列表
        print(f"{msg.sender_screen_name}:{msg.text}")


@myBot.onNewWeibo  # 首页刷到时触发
async def on_weibo(weibo: Weibo):
    if weibo.original_weibo is None:  # 原创
        print(f"{weibo.text}")


@myBot.onMentionCmt  # 提及我的评论时触发
async def on_mention_cmt(cmt: Comment):
    print(cmt)


@myBot.onTick  # 每次循环触发
async def on_tick():
    if datetime.now().minute == 30:
        print("hit tik, post now")
        await myBot.post_weibo(random.choice(message_list))
        time.sleep(60)


if __name__ == "__main__":
    myBot.run()
