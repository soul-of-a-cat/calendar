import time
import schedule
from telebot.async_telebot import AsyncTeleBot
from threading import Thread
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = AsyncTeleBot(TOKEN)
chats = []


@bot.message_handler(commands=['start'])
async def start(message):
    chat_id = message.chat.id
    if chat_id not in chats:
        chats.append(chat_id)
    await bot.send_message(chat_id, 'Вы подписались на рассылку')


@bot.message_handler(commands=['calendar'])
async def calendar(message):
    from parse import text
    await bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['stop'])
async def stop(message):
    chat_id = message.chat.id
    if chat_id in chats:
        del chats[chats.index(chat_id)]
        await bot.send_message(chat_id, 'Вы отписались от рассылки')
    else:
        await bot.send_message(chat_id, 'Вы уже отписаны')


async def send():
    from parse import text

    for chat_id in chats:
        await bot.send_message(chat_id, text)


def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    schedule.every(1).day.at('00:00:10').do(send)
    Thread(target=run).start()
    asyncio.run(bot.polling(none_stop=True, interval=0))
