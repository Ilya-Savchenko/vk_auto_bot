import vk_api
import vk_api.utils
from vk_api.bot_longpoll import VkBotLongPoll
import settings
from database.create_db import connect_and_fill_db


class VkBot:

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.api = vk_api.VkApi(token=token)
        self.poll = VkBotLongPoll(self.api, self.group_id)
        self.vk_sess = self.api.get_api()


    def run(self):
        """Start bot"""
        connect_and_fill_db()
        for event in self.poll.listen():
            print('11')


if __name__ == '__main__':
    bot = VkBot(token=settings.TOKEN, group_id=settings.GROUP_ID)
    bot.run()
