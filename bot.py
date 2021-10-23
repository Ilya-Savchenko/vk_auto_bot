import vk_api
import vk_api.utils
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import settings
import states
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
        self.msg_handler = MessageHandler()

    def run(self):
        connect_and_fill_db()
        for event in self.poller.listen():
            self._event_handler(event)

    def _event_handler(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.object.message
            user_id = str(message.get('from_id'))
            message_text = message.get('text')

            query = UserState.select().where(UserState.user_id == user_id)
            if not query.exists():
                self._start(msg=message_text, user_id=user_id)
            else:
                self._continue(msg=message_text, user_id=user_id)

    def _start(self, user_id, msg):
        state = states.STATES.get('first_state')
        handler = self._get_handler(state)
        text, keyboard = handler(msg=msg, user_id=user_id)
        self._send_text_message(user_id, text, keyboard)

    def _continue(self, msg, user_id):
        state = UserState.get(UserState.user_id == user_id).state
        handler = self._get_handler(state)
        text, image, keyboard = handler(msg=msg, user_id=user_id)
        if image:
            self._send_image_message(user_id, image)
        self._send_text_message(user_id, text, keyboard)

    def _get_handler(self, state):
        handler_name = states.STATES.get('states').get(state).get('handler')
        handler = getattr(self.msg_handler, handler_name)
        return handler

    def _send_text_message(self, user_id, msg, keyboard=None):
        if not keyboard:
            self.vk_sess.messages.send(user_id=user_id, message=msg, random_id=vk_api.utils.get_random_id())
        else:
            self.vk_sess.messages.send(
                user_id=user_id, message=msg, random_id=vk_api.utils.get_random_id(), keyboard=keyboard.get_keyboard()
            )

    def _send_image_message(self, user_id, image):
        upload = vk_api.upload.VkUpload(self.api)
        img = upload.photo_messages(image)
        owner_id = img[0]['owner_id']
        media_id = img[0]['id']
        attachment = f'photo{owner_id}_{media_id}'
        self.vk_sess.messages.send(user_id=user_id, attachment=attachment, random_id=vk_api.utils.get_random_id())


if __name__ == '__main__':
    bot = VkBot(token=settings.TOKEN, group_id=settings.GROUP_ID)
    bot.run()
