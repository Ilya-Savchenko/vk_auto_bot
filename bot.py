import requests
import vk_api
import vk_api.utils
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import states
import settings
from database.create_db import connect_and_fill_db
from database.models import UserState, Section
from message_handler import MessageHandler


class VkBot:

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.api = vk_api.VkApi(token=self.token)
        self.poller = VkBotLongPoll(self.api, self.group_id)
        self.vk_sess = self.api.get_api()
        self.msg_handler = MessageHandler()  # обработка сообщений
        self.message_sender = None  # отправка сообщений

    def run(self):
        """Start bot"""
        connect_and_fill_db()
        self.categories = [category.name for category in Section.select()]
        print('run')
        for event in self.poller.listen():
            self.event_handler(event)


    def event_handler(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            print('event')
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
        handler_name = states.STATES.get('states').get(state).get('handler')
        handler = getattr(self.msg_handler, handler_name)
        text = handler(msg=msg, user_id=user_id)
        self.send_text_message(user_id, text)



    def _continue(self, msg, user_id):
        state = UserState.get(UserState.user_id == user_id).state
        handler_name = states.STATES.get('states').get(state).get('handler')
        handler = getattr(self.msg_handler, handler_name)
        text, image = handler(msg=msg, user_id=user_id)
        if image:
            self.send_image_message(user_id, image)
        self.send_text_message(user_id, text)
        # self.msg_handler.state1_msg_handler(msg=msg, user_id=user_id)
        # all_states = states.STATES.get('states')
        # next_state = all_states.get(state).get('next_state')
        # print('continue')
        # new_state = UserState.get(UserState.user_id == user_id)
        # new_state.state = next_state
        # # previous_state = states.STATES.get('states').get(state).get('previous_state')
        # all_states = states.STATES.get('states')
        # text = all_states.get(next_state).get('text')
        # self.send_text_message(user_id, text)


    def send_text_message(self, user_id, msg):
        self.vk_sess.messages.send(user_id=user_id, message=msg, random_id=vk_api.utils.get_random_id())

    def send_image_message(self, user_id, image):
        upload = vk_api.upload.VkUpload(self.api)
        img = upload.photo_messages(image)
        owner_id = img[0]['owner_id']
        media_id = img[0]['id']
        # access_key = img[0]['access_key']
        # attachment = f'photo{owner_id}_{media_id}_{access_key}'
        attachment = f'photo{owner_id}_{media_id}'
        self.vk_sess.messages.send(user_id=user_id, attachment=attachment, random_id=vk_api.utils.get_random_id())

        # upload_url = self.vk_sess.photos.getMessagesUploadServer().get('upload_url')
        # print(upload_url)
        # upload_data = requests.post(upload_url, files={'photo': ('image.jpg', image, 'image/jpeg')}).json()
        # print(upload_data)
        # image_data = self.vk_sess.photos.saveMessagesPhoto(**upload_data)
        #
        # owner_id = image_data[0]['owner_id']
        # media_id = image_data[0]['id']
        # self.vk_sess.messages.send(user_id=user_id, attachment=attachment, random_id=vk_api.utils.get_random_id())


if __name__ == '__main__':
    bot = VkBot(token=settings.TOKEN, group_id=settings.GROUP_ID)
    bot.run()
