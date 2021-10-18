from database.models import Good, Section, UserState
import states

class MessageHandler:

    def __init__(self):
        self.state1_tokens = []

    def state0_msg_handler(self, msg, user_id):
        state = states.STATES.get('first_state')
        all_states = states.STATES.get('states')
        next_state = all_states.get(state).get('next_state')
        if msg.lower() == all_states.get(state).get('tokens'):
            text = all_states.get(next_state).get('text')
            UserState.create(user_id=user_id, state=next_state)
        else:
            text = all_states.get(state).get('error_text')
        return text

    def state1_msg_handler(self, msg, user_id):
        user = UserState.get(UserState.user_id == user_id)
        print(f'{user.state}!!!!!!!!!!!!!!!')
        self.state1_tokens = [str(el) for el in self._generate_tokens_for_state1()]
        print(self.state1_tokens)
        state = user.state
        print(state)
        all_states = states.STATES.get('states')
        next_state = all_states.get(state).get('next_state')
        print(next_state)
        if msg.lower() in self.state1_tokens:
            text = all_states.get(next_state).get('text')
            if next_state:
                user.state = next_state
                user.save()
                user = UserState.get(UserState.user_id == user_id)
                print(f'!!!!!!!!!!!{user.state}')
        else:
            text = all_states.get(state).get('error_text')
        return text

    def state2_msg_handler(self):
        pass

    def _generate_tokens_for_state1(self):
        number_of_sections = len(list(Section.select()))
        return list(range(1, number_of_sections + 1))
