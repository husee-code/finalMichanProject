import asyncio
from contextlib import suppress

import os
import json
import configparser

import aiogram
import aioschedule
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import CantRestrictChatOwner
from telethon import TelegramClient, events
from telethon.tl.types import MessageActionChatJoinedByLink, MessageActionChatAddUser, MessageActionChatDeleteUser, \
    UpdateShortMessage, InputPeerChat
from bot.filter_new_members import register_new_participant_handler, kick_member, ban_member
from cons_and_vars.vars import zaebis_chat, gandoniy_chat, users_to_kick, users_to_ban, update_users_to_kick


async def kick_pidors(client_nash: TelegramClient, pidor_client: TelegramClient, bot):
    ours = set([i.id async for i in client_nash.iter_participants(zaebis_chat)])
    pidors = set([i.id async for i in pidor_client.iter_participants(gandoniy_chat)])
    print(f'{pidors = }')
    update_users_to_kick(list(pidors))
    gandoni = ours & pidors
    for gandon in gandoni:
        with suppress(CantRestrictChatOwner):
            await kick_member(zaebis_chat, gandon, bot, send_message=False)
            print(f"пидор {gandon} кикнут")
        await asyncio.sleep(1)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(r"D:\finalMihanProject\settings.ini")
    api_id, api_hash = int(config["userbot"]["api_id"]), config["userbot"]["api_hash"]
    bot_key = config["bot"]["bot_key"]
    client_nash = TelegramClient('our_userbot', api_id, api_hash)
    print(1)
    client = TelegramClient('pidor_userbot', api_id, api_hash)
    print(2)


    bot = Bot(bot_key)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    dp.middleware.setup(LoggingMiddleware())
    register_new_participant_handler(dp, bot, client)

    client.start()
    print(2)
    client_nash.start()
    print(1)

    loop = asyncio.get_event_loop()
    loop.create_task(
        kick_pidors(client_nash, client, bot))

    @client.on(events.ChatAction(chats=[gandoniy_chat]))
    async def new_gandoniy(event):
        user_id = event.user_ids[0]
        chat_id = '-' + str(event.action_message.peer_id.chat_id)
        print(event.action_message.action)
        if type(event.action_message.action) in (MessageActionChatJoinedByLink, MessageActionChatAddUser):
            if user_id not in users_to_ban:
                users_to_kick.add(user_id)
                await kick_member(zaebis_chat, user_id, bot)
            else:
                await ban_member(zaebis_chat, user_id, bot)



    executor.start_polling(dispatcher=dp)


