from database.models import Good, Section, UserState
import states

class MessageHandler:

    def __init__(self):
        self.state1_tokens = []
        self.categories = {}

    def state0_msg_handler(self, msg, user_id):
        state = states.STATES.get('first_state')
        all_states = states.STATES.get('states')
        next_state = all_states.get(state).get('next_state')
        if msg.lower() == all_states.get(state).get('tokens'):
            text = all_states.get(next_state).get('text')
            text += self.generate_categories_list()
            UserState.create(user_id=user_id, state=next_state)
        else:
            text = all_states.get(state).get('error_text')
        return text

    def state1_msg_handler(self, msg, user_id):
        image = None
        user = UserState.get(UserState.user_id == user_id)
        self.state1_tokens = [str(el) for el in self._generate_tokens_for_state1()]
        state = user.state
        all_states = states.STATES.get('states')
        next_state = all_states.get(state).get('next_state')
        if msg.lower() in self.state1_tokens:
            category_name = self.categories.get(int(msg.lower()))
            category = Section.get(Section.name == category_name)
            goods_in_section = Good.select().where(Good.section == category.id)
            good = goods_in_section[0]
            user.good_id = good.id
            text = self.create_reply_msg(all_states, good, next_state)
            image = good.image
            self.save_user_state(next_state, user)
        else:
            text = all_states.get(state).get('error_text')
        return text, image

    def create_reply_msg(self, all_states, good, next_state):
        text = self.create_msg_with_product_info(good.id)
        text += all_states.get(next_state).get('text')
        return text

    def save_user_state(self, state, user):
        user.state = state
        user.save()

    def state2_msg_handler(self, msg, user_id):
        image = None
        user = UserState.get(UserState.user_id == user_id)
        print(f'{user.state}!!!!!!!!!!!!!!!')
        state = user.state
        all_states = states.STATES.get('states')
        next_state = all_states.get(state).get('next_state')
        if msg.lower() in all_states.get(state).get('tokens'):
            if msg.lower() == 'далее':
                # следующий товар
                text = '->'
            elif msg.lower() == 'назад':
                # предыдущий товар
                text = '<-'
            elif msg.lower() == 'в меню':
                # вернуться на предыдущий этап
                text = '<--'
            elif msg.lower() == 'заказать':
                # заказ
                text = all_states.get(next_state).get('text')
                self.save_user_state(next_state, user)
        else:
            text = all_states.get(state).get('error_text')
        return text, image


    def state3_msg_handler(self):
        pass

    def _generate_tokens_for_state1(self):
        number_of_sections = len(list(Section.select()))
        return list(range(1, number_of_sections + 1))

    def generate_categories_list(self):
        for i, category in enumerate(Section.select()):
            self.categories[i + 1] = category.name
        print(self.categories)
        text = ''
        for i in range(len(self.categories)):
            text += f'\n{i + 1}. {self.categories[i + 1]}'
        return text

    def create_msg_with_product_info(self, good_id):
        good = Good.get(Good.id == good_id)
        price = good.price
        name = good.name
        description = good.description
        return f'{name} \n{description} \nЦена: {price} \n'


