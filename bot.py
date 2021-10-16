import vk_api
import vk_api.utils
from vk_api.bot_longpoll import VkBotLongPoll
import settings
from database.create_db import connect_and_fill_db


class VkBot:

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.api = vk_api.VkApi(token=self.token)
        self.poller = VkBotLongPoll(self.api, self.group_id)
        self.vk_sess = self.api.get_api()
        self.message_receiver = None  # прием сообщений
        self.message_handler = None  # обработка сообщений
        self.message_sender = None  # отправка сообщений


    def run(self):
        """Start bot"""
        connect_and_fill_db()
        print('run')
        for event in self.poller.listen():
            print(event)
            message = event.object.message
            user_id = str(message['from_id'])
            message_text = message['text']
            self.vk_sess.messages.send(user_id=user_id,
                                       message=message_text,
                                       random_id=vk_api.utils.get_random_id())


if __name__ == '__main__':
    bot = VkBot(token=settings.TOKEN, group_id=settings.GROUP_ID)
    bot.run()
