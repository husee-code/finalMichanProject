import os
import json

users_to_ban = set()
gandoniy_chat = -603273110
zaebis_chat = -1001669569045

with open(os.path.abspath(r'finalMichanProject/black_list/permanent.json')) as js:
    black_list: set = set(json.load(js))

users_to_kick = set()


def get_users_to_kick():
    with open(os.path.abspath(r"finalMichanProject/black_list/users_to_kick.json"), encoding='utf-8') as js:
        return set(json.load(js))


def update_users_to_kick(new_list):
    with open(os.path.abspath(r"finalMichanProject/black_list/users_to_kick.json"), 'w', encoding='utf-8') as js:
        json.dump(new_list, js)


# for chat in os.listdir(r'D:\finalMihanProject\black_list\restricted_chats'):
#     with open(rf'D:\finalMihanProject\black_list\restricted_chats/{chat}') as js:
#         chat_name = chat.replace('.json', '')
#         gandoniy_dict[chat_name] = set(json.load(js))


with open(os.path.abspath(r"finalMichanProject/cons_and_vars/texts.json"), encoding='utf-8') as js:
    texts = json.load(js)
