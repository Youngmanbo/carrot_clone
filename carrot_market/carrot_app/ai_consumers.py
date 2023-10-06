import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .chatbot import gpt_view

class AiConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        question= text_data_json.get('question', '')
        
        response_generator = gpt_view(question)
        try:
            message_content = response_generator['choices'][0]['message']['content']
            json_message = json.dumps(message_content, ensure_ascii=False)
            print(json_message)
            await asyncio.sleep(0.05)
            await self.send(text_data=json_message)
        except Exception :
            print('생성 완료')