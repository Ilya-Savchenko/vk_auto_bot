import vk_api
import vk_api.utils
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import states
import settings
from database.create_db import connect_and_fill_db
from database.models import UserState
from message_handler import MessageHandler


class VkBot:

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.api = vk_api.VkApi(token=self.token)
        self.poller = VkBotLongPoll(self.api, self.group_id)
        self.vk_sess = self.api.get_api()
        self.msg_handler = MessageHandler  # обработка сообщений
        self.message_sender = None  # отправка сообщений

    def run(self):
        """Start bot"""
        connect_and_fill_db()
        print('run')
        for event in self.poller.listen():
            self.event_handler(event)


    def event_handler(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            user_id = str(message.get('from_id'))
            message_text = message.get('text')

            query = UserState.select().where(UserState.user_id == user_id)
            if not query.exists():
                self._start(user_id=user_id)
            else:
                self._continue(user_id=user_id)

            msg = self.handle_message(message_text)
            self.send_text_message(user_id=user_id, msg=msg)


    def handle_message(self, message_text):
        handler = self.msg_handler(message_text)
        msg = handler.handle_message()
        return msg

    def _start(self, user_id):
        state = states.STATES.get('first_state')
        UserState.create(user_id=user_id, state=state)

    def _continue(self, user_id):
        state = UserState.get(UserState.user_id == user_id).state
        next_state = states.STATES.get('states').get(state).get('next_state')
        previous_state = states.STATES.get('states').get(state).get('previous_state')

    def send_text_message(self, user_id, msg):
        self.vk_sess.messages.send(user_id=user_id, message=msg, random_id=vk_api.utils.get_random_id())




if __name__ == '__main__':
    bot = VkBot(token=settings.TOKEN, group_id=settings.GROUP_ID)
    bot.run()
