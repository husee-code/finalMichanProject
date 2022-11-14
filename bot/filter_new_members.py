from contextlib import suppress

from aiogram import types, Bot
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import CantInitiateConversation, CantTalkWithBots, CantRestrictSelf
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError

from cons_and_vars.vars import black_list, zaebis_chat, gandoniy_chat, texts, users_to_ban, \
    update_users_to_kick, get_users_to_kick
from functions import update_pre_ban_list

unsubscribed_button = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Отписался', callback_data='unsubscribed'))

link_to_group = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton(text='Перейти в чат', url="https://t.me/+Ko_B8Ua5j6g4NGJi")
)


def register_new_participant_handler(dp: Dispatcher, bot: Bot, client):
    @dp.callback_query_handler()
    async def check(callback: types.CallbackQuery):
        print('кнопка нажата')
        user_id = callback.from_user.id
        if user_id not in users_to_ban:
            iter_participants = client.iter_participants(gandoniy_chat)
            users_to_kick = [participant.id async for participant in iter_participants]
            update_users_to_kick(users_to_kick)
            if user_id in users_to_kick:
                await callback.message.answer(texts["message_if_not_unsubscribed"],
                                              reply_markup=unsubscribed_button)
            else:
                await callback.message.answer(texts["message_if_unsubscribed"], reply_markup=link_to_group)
                users_to_ban.add(user_id)
                update_pre_ban_list(list(users_to_ban))
        else:
            await callback.message.answer(user_id, texts["message_if_banned"])
        await callback.answer()

    @dp.chat_join_request_handler()
    async def new_member_handler(update: types.ChatJoinRequest):
        print('here')
        user_id = update.from_user.id
        iter_participants = client.iter_participants(gandoniy_chat)
        users_to_kick = [participant.id async for participant in iter_participants]
        update_users_to_kick(users_to_kick)
        f = True
        if user_id in black_list:
            await bot.kick_chat_member(chat_id=zaebis_chat, user_id=user_id, revoke_messages=True)
            await bot.send_message(user_id, texts["message_to_banned"])
            f = False
        
        if user_id in users_to_kick:
            if user_id in users_to_ban:
                await bot.kick_chat_member(zaebis_chat, user_id)
                await bot.send_message(user_id, texts['message_if_banned'])
                f = False

            else:
                await bot.send_message(user_id, texts['message_to_kicked'],
                                       reply_markup=unsubscribed_button)
                print(f'waiting {user_id}')
                f = False

        if f:
            await update.approve()
            print(f'{user_id} approved')


async def kick_member(chat_id, user_id, bot: Bot, send_message: bool = True):
    if send_message:
        with suppress(CantInitiateConversation, CantTalkWithBots, CantRestrictSelf, ChannelPrivateError):
            await bot.send_message(user_id, texts['message_to_kicked'])
    with suppress(CantTalkWithBots, CantRestrictSelf, ChannelPrivateError):
        await bot.kick_chat_member(chat_id, user_id)
        await bot.unban_chat_member(chat_id, user_id)


async def ban_member(chat_id, user_id, bot: Bot):
    await bot.send_message(user_id, texts['message_if_banned'])
    await bot.kick_chat_member(chat_id, user_id)

