from datetime import timedelta, datetime

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

chat_id = -1001770861632
white_list = {323159485, 210944655, 1815156681, 1219634645, 1584413605, 5443619563}


def check_len(string: str):
    return len(string) < 1501 and string.count('\n') < 11


def has_link(message: types.Message):
    entities = message.entities
    for entity in entities:
        if entity["type"] == 'url':
            return True


def register_anti_spam_handler(dp: Dispatcher, bot: Bot):
    @dp.message_handler(lambda message: message.from_user.id not in white_list and message.chat.id == chat_id,
                        chat_id=chat_id)
    async def new_message(message: types.Message):
        if not check_len(message.text):
            await bot.delete_message(chat_id, message.message_id)
            await bot.restrict_chat_member(chat_id, message.from_user.id, types.ChatPermissions(False),
                                           until_date=datetime.now() + timedelta(minutes=1))
        if has_link(message):
            await bot.delete_message(chat_id, message.message_id)
