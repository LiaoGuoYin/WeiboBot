import os
import requests
from dotenv import load_dotenv

load_dotenv()

MODEL = "gpt-3.5-turbo"
# https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo
REPLY_PROMPT = """
你是没关系Bot。你的风格是没脸没皮、调侃自黑，明知道屁也不是，硬要说很厉害了的感觉。
当我给你一段文字时，你需要提取出一件普通但是正向的事情xxxx，硬要把它说得很厉害。
回答不能超过20个字，回答格式：没关系，xxxx，已经很厉害了。需要替换其中的xxxx
"""

AUTO_PROMPT = """
生成一句不多于20字的积极鼓励的冷幽默短句, 不要人称代词, 不要比喻, 不要形容词, 需要客观简单些
风格是没脸没皮、调侃自黑，明知道啥也不是，但就是要说得很厉害的感觉。
这些短句应该强调即便是看似微小的行为或成就。成就可能是解决了工作、学习、日常生活中的小挑战、或心理上的负担。
请确保每个短句都以“没关系，”开头，并在结尾强调“已经很厉害了”
"""


def no_matter_bot(
    message="今天一下午的时间全用来搞AI了，论文一个字没写",
    prompt=REPLY_PROMPT,
    model=MODEL,
):
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
                    "content": prompt,
                },
                {"role": "user", "content": message},
            ],
            # "temperature": 0.7
        },
    )
    response_json = response.json()
    # print(response_json)
    print(response_json["choices"][0]["message"]["content"], response_json["usage"])
    return response_json["choices"][0]["message"]["content"]


# 对比效果
if __name__ == "__main__":
    GPT_MODEL_LIST = [
        "gpt-3.5-turbo",
        # "gpt-4-turbo",
        # "gpt-4",
        # "gpt-3.5",
    ]
    for _ in range(3):
        for each in range(len(GPT_MODEL_LIST)):
            print(
                GPT_MODEL_LIST[each],
                no_matter_bot(
                    message=AUTO_PROMPT, prompt="", model=GPT_MODEL_LIST[each]
                ),
            )
        print("*" * 10)
