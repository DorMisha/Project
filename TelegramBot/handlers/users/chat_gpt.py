from loader import dp
from filters import IsPrivate
from aiogram import types

import openai

openai.api_key = "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"
model_engine = 'text-davinci-003'

@dp.message_handler()
async def respond(message: types.Message):
    completed = openai.Completion.create(
        engine=model_engine,
        prompt=message.text,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    await message.answer(completed.choices[0].text)




