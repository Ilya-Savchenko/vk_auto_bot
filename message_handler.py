from database.models import Good, Section

class MessageHandler:

    def __init__(self, message):
        self.msg = message

    def handle_message(self):
        if self.msg.lower() == 'начать':
            sections_set = Section.select()
            sections = []
            for el in sections_set:
                sections.append(el.name)
            return sections

    def msg_handler(self, msg, state):
        if str(msg).isdigit() and state=='state1':
            if int(msg) < len(state):
                return True


