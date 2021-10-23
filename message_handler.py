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
        self.state1_tokens = [str(el) for el in self.generate_tokens_for_state1()]
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

    def state2_msg_handler(self, msg, user_id):
        image = None
        user = UserState.get(UserState.user_id == user_id)
        state = user.state
        all_states = states.STATES.get('states')
        next_state = all_states.get(state).get('next_state')
        if msg.lower() in all_states.get(state).get('tokens'):
            if msg.lower() == 'далее':
                image, text = self.next_good(all_states, image, state, user)
            elif msg.lower() == 'назад':
                image, text = self.previous_good(all_states, image, state, user)
            elif msg.lower() == 'в меню':
                previous_state = all_states.get(state).get('previous_state')
                text = all_states.get(previous_state).get('text')
                text += self.generate_categories_list()
                self.save_user_state(previous_state, user)
            elif msg.lower() == 'заказать':
                text = all_states.get(next_state).get('text')
                self.delelte_user_instance(user_id)
        else:
            text = all_states.get(state).get('error_text')
        return text, image

    def delelte_user_instance(self, user_id):
        user = UserState.get(UserState.user_id == user_id)
        user.delete_instance()

    def get_goods_in_section(self, user):
        good_id = user.good_id
        good = Good.get(Good.id == good_id)
        section = Section.get(Section.id == good.section)
        goods_in_section = Good.select().where(Good.section == section.id)
        return good_id, goods_in_section

    def previous_good(self, all_states, image, state, user):
        good_id, goods_in_section = self.get_goods_in_section(user)
        for i, good in enumerate(goods_in_section):
            if good.id == good_id:
                good = goods_in_section[i - 1]
                text = self.create_reply_msg(all_states, good, state)
                image = good.image
                print(good.id)
                user.good_id = good.id
                user.save()
        return image, text

    def next_good(self, all_states, image, state, user):
        good_id, goods_in_section = self.get_goods_in_section(user)
        for i, good in enumerate(goods_in_section):
            if good.id == good_id:
                try:
                    good = goods_in_section[i + 1]
                except IndexError:
                    good = goods_in_section[0]
                finally:
                    text = self.create_reply_msg(all_states, good, state)
                    image = good.image
                    print(good.id)
                    user.good_id = good.id
                    user.save()
        return image, text


    def create_reply_msg(self, all_states, good, state):
        text = self.create_text_with_product_info(good.id)
        text += all_states.get(state).get('text')
        return text

    def save_user_state(self, state, user):
        user.state = state
        user.save()

    def generate_tokens_for_state1(self):
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

    def create_text_with_product_info(self, good_id):
        good = Good.get(Good.id == good_id)
        price = good.price
        name = good.name
        description = good.description
        return f'{name} \n{description} \nЦена: {price} \n'


