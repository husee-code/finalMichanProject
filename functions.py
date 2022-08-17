import os
import json


def update_pre_ban_list(banlist: list):
    with open(os.path.abspath(r'black_list\pre_ban_list.json'), 'w') as js:
        json.dump(banlist, js)

