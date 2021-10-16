import vk_api
import vk_api.utils
from vk_api.bot_longpoll import VkBotLongPoll
import settings


class VkBot:

    def __init__(self, token, group_id):
        self.token = token
        self.group_id = group_id
        self.api = vk_api.VkApi(token=token)
        self.poll = VkBotLongPoll(self.api, self.group_id)
        self.vk_sess = self.api.get_api()

    def run(self):
        """Start bot."""
        for event in self.poll.listen():
            self.event_handling(event)


if __name__ == '__main__':
    bot = VkBot(token=settings.TOKEN, group_id=settings.GROUP_ID)
