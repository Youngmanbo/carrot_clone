from pathlib import Path
from bardapi import Bard
import openai
import json
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRETS_DIR = BASE_DIR / '.secrets'
secrets = json.load(open(os.path.join(SECRETS_DIR, 'secrets.json')))

# def bard(question):
#     token = secrets['GOOGLE_AI_KEY']
#     b = Bard(token=token)
#     response = b.get_answer(question)
#     return response

def gpt_view(question):
    
    print(question)
    api_key = secrets['OPEN_AI_API_KEY']
                
    response_generator = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
            "role": "system",
            "content": "묻는 말에 정확한 답변을 해줘 "},
            {"role": "user", "content": f"'{question}'에 대해서 친절히 답변해줘"},
        ],
        temperature=0.5,
        max_tokens=400,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        api_key=api_key,
    )

    return response_generator

# print(bard("오늘 날씨는?"))


# import requests

# # Set the __Secure-1PSID cookie value.
# def test():
#     cookie = {"__Secure-1PSID": "bgjPZzlpYGo9L-KGjOBuxEDshFal-E_eYbP0P5RGmZV1D_xGW5D0FVSsZA9wvUHF_7mpkw."}

#     # Call the Bard API.
#     response = requests.post(
#         "https://bard.google.com/api/",
#         cookies=cookie,
#         json={"text": "This is a sentence."},
#     )
#     print(response)
# test()