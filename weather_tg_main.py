import requests
import datetime
from config import tg_bot_token, open_weather_token, tg_chatgpt_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Дорообо! Ханнык куорат халлаан туругун интириэhиргииргин суруй миэхэ")

@dp.message_handler(commands=["chatgpt"])
async def get_chatgpt(message: types.Message):
    try:
        user_text = message.text.split('/chatgpt', 1)[1].strip()

        headers = {
            'Authorization': f'Bearer {tg_chatgpt_token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'gpt-3.5-turbo',  # Используем актуальную модель (пример: text-davinci-1-3-0)
            'prompt': user_text,
            'max_tokens': 50
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=payload)
        data = response.json()
        print("API Response:", data)

        if 'choices' in data and len(data['choices']) > 0:
            generated_text = data['choices'][0]['text']
            await message.reply(generated_text)
        else:
            await message.reply("Не удалось получить ответ от ChatGPT")

    except IndexError:
        await message.reply("Пожалуйста, укажите текст для обработки после команды /chatgpt")
    except Exception as e:
        await message.reply(f"Ошибка при обработке запроса: {e}")

@dp.message_handler()
async def get_weather(message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = sunset_timestamp - sunrise_timestamp
        await message.reply(f"*{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*\n"
                            f"Нэьилиэк: {city}\nТемпература: {cur_weather}°C\n"
                            f"Салгын сиигэ: {humidity}%\nСалгын баттааьына: {pressure} мм.рт.ст.\nТыал тургэнэ: {wind} м/с\n"
                            f"Кун тахсыыта: {sunrise_timestamp}\nКун киириитэ: {sunset_timestamp}\nКун уьуна: {length_of_the_day}\n"
                            f"Учугэй куну!\nАтын нэьилиэги корорго нэьилиэк аатын хаттаан суруй"
                            )

    except Exception as e:
        await message.reply("Арааста сыыьа баар, хаттаан нэьилиэк аатын нууччалы, английскайдыы эбэтэр транскрипцияннан суруй")

if _name_ == '_main_':
    executor.start_polling(dp)