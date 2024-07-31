import time
import schedule
from telebot.async_telebot import AsyncTeleBot
from threading import Thread
import asyncio
import os
from dotenv import load_dotenv
from db_tables import Chats
import db_session
from parse import text

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = AsyncTeleBot(TOKEN)

send_text = text


@bot.message_handler(commands=['start'])
async def start(message):
    chat_id = message.chat.id
    session = db_session.create_session()
    chats = [chat.chat for chat in session.query(Chats).all()]
    if chat_id not in chats:
        chat = Chats(chat=chat_id)
        session.add(chat)
        session.commit()
        await bot.send_message(chat_id, 'Вы подписались на рассылку!')
    else:
        await bot.send_message(chat_id, 'Вы уже подписаны!')


@bot.message_handler(commands=['calendar'])
async def calendar(message):
    await bot.send_message(message.chat.id, send_text)


@bot.message_handler(commands=['stop'])
async def stop(message):
    chat_id = message.chat.id
    session = db_session.create_session()
    chat = session.query(Chats).filter(Chats.chat == chat_id).first()
    if chat:
        session.delete(chat)
        session.commit()
        await bot.send_message(chat_id, 'Вы отписались от рассылки!')
    else:
        await bot.send_message(chat_id, 'Вы уже отписаны!')


async def send():
    global send_text
    from parse import text
    send_text = text

    session = db_session.create_session()
    chats = [chat.chat for chat in session.query(Chats).all()]
    for chat_id in chats:
        await bot.send_message(chat_id, send_text)


def run():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    db_session.global_init("db/db.sqlite3")
    schedule.every(1).day.at('00:00:10').do(send)
    Thread(target=run).start()
    asyncio.run(bot.polling(none_stop=True, interval=0))
