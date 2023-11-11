from aiogram import Bot, Dispatcher, executor, types
import openai
openai.api_key = "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"
model_engine = 'text-davinci-003'
TOKEN = '6022362030:AAHQJs-LW-EI6Hci7AwP8m8reL8g7ZztFNc'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

async def on_startup(_):
    print('Бот запущен')

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text='Welcome to ChatGPT Bot! You can ask me anything!')

@dp.message_handler()
async def Respond(message: types.Message):
    completion = openai.Completion.create(
        engine='text-davinci-003',
        prompt=message.text,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    await message.answer(completion.choices[0].text)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
