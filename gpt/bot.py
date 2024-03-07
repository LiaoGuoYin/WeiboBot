import os
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL = "gpt-4-turbo-preview"
PROMPT = """
你是没关系Bot。你的风格是没脸没皮、调侃自黑，明知道屁也不是，硬要说很厉害了的感觉。
当我给你一段文字时，你需要提取出一件普通但是正向的事情xxxx，硬要把它说得很厉害，回答不能超过20个字。
回答格式：没关系，xxxx，已经很厉害了。需要你替换其中的xxxx
"""


def no_matter_bot(message="今天一下午的时间全用来搞AI了，但是论文一个字没写"):
    # https://platform.openai.com/docs/api-reference/making-requests
    response = requests.post(
        os.getenv("GPT_API_URL"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.getenv('GPT_API_KEY')}",
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": PROMPT,
                },
                {"role": "user", "content": message},
            ],
            # "temperature": 0.7
        },
    )
    response_json = response.json()
    print(response_json["choices"][0]["message"]["content"], response_json["usage"])
    return response_json["choices"][0]["message"]["content"]
