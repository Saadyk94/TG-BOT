import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot =Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(Message: types.Message):
    await Message.reply("Дорообо! Ханнык куорат халлаан туругун интириэhиргииргин суруй миэхэ")


@dp.message_handler()
async def get_weather(Message: types.Message):
    try:
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={Message.text}&appid={open_weather_token}&units=metric&lang=ru"
        )
        data = r.json()
       

        city = data["name"]
        cur_weather = data["main"]["temp"]
        humidity = data ["main"]["humidity"]
        pressure = data ["main"]["pressure"]
        wind = data ["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data ["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data ["sys"]["sunset"])
        Length_of_the_day = datetime.datetime.fromtimestamp(data ["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data ["sys"]["sunrise"])
        await Message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
        f"Погода в городе: {city}\nТемпература: {cur_weather}С°\n"
        f"Влажность: {humidity}%\nАтмосферное давление: {pressure} мм.рт.ст.\nСкорость ветра: {wind} м/с\n"
        f"Рассвет: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность светового дня: {Length_of_the_day}\n "
        f"Хорошего вам дня!"
        )


    except:
        await Message.reply("проверьте название города")



if __name__=='__main__':
    executor.start_polling(dp)