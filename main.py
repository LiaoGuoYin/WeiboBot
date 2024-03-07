import asyncio
import os

from fastapi import FastAPI
from WeiboBot import Bot
from WeiboBot.const import VISIBLE
from WeiboBot.message import Chat
from WeiboBot.weibo import Weibo
from WeiboBot.comment import Comment
from dotenv import load_dotenv
import uvicorn

from datetime import datetime

load_dotenv()
app = FastAPI()


async def post_handle(message, visible=VISIBLE.ALL):
    bot = Bot(cookies=os.getenv("ACCOUNT1_COOKIES"))
    await asyncio.wait_for(bot.login(), timeout=10)  # 先登录
    not_problem_message = f"没关系，{message}，已经很厉害了[开学季]"
    return await bot.post_weibo(not_problem_message, visible=visible)


@app.get("/")
def read_root():
    return {"Hello, Coin": datetime.now()}


@app.get("/p/{bot_message}")
async def post_weibo(bot_message="没什么的"):
    result = await post_handle(bot_message)
    return {"message": result.raw_text}


@app.get("/m/{bot_message}")
async def post_weibo(bot_message="没什么的"):
    result = await post_handle(bot_message, visible=VISIBLE.ONLY_ME)
    return {"message": result.raw_text}


if __name__ == "__main__":
    # asyncio.run(post_handle("会用GPT了"))
    uvicorn.run("main:app", host="0.0.0.0", port=3900, log_level="info")
