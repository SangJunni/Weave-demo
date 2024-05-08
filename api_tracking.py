import weave
import json
import os
import urllib3
from openai import OpenAI, api_key
from dotenv import load_dotenv, find_dotenv
urllib3.disable_warnings()

# .env 파일에서 환경 변수 로드
_ = load_dotenv()

# OpenAI API 키/ 모델 설정 가져오기
api_key = os.getenv('OPENAI_API_KEY')

@weave.op()
def extract_fruit(sentence: str) -> dict:
    client = OpenAI(api_key = api_key)

    response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {
            "role": "system",
            "content": "You will be provided with unstructured data, and your task is to parse it one JSON dictionary with fruit, color and flavor as keys."
        },
        {
            "role": "user",
            "content": sentence
        }
        ],
        temperature=0.7,
        response_format={ "type": "json_object" }
    )
    extracted = response.choices[0].message.content
    return json.loads(extracted)

weave.init('intro-example')
sentence = "There are many fruits that were found on the recently discovered planet Goocrux. There are neoskizzles that grow there, which are purple and taste like candy."
extract_fruit(sentence)