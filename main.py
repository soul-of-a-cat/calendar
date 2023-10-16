import time
import schedule
from telebot.async_telebot import AsyncTeleBot
from threading import Thread
import asyncio

with open('bot.txt') as f:
    TOKEN = f.read()

bot = AsyncTeleBot(TOKEN)
chats = []


@bot.message_handler(commands=['start'])
async def start(message):
    chat_id = message.chat.id
    if chat_id not in chats:
        chats.append(chat_id)
    await bot.send_message(chat_id, 'Вы подписались на рассылку')


@bot.message_handler(commands=['calendar'])
async def start(message):
    from parse import text
    await bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['stop'])
async def stop(message):
    chat_id = message.chat.id
    if chat_id in chats:
        del chats[chat_id]
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
    schedule.every(1).day.at('00:01:10').do(send)
    Thread(target=run).start()
    asyncio.run(bot.polling(none_stop=True, interval=0))
