from database.models import Good, Section, UserState
import states

class MessageHandler:

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

    def state1_msg_handler(self):
        pass

    def state2_msg_handler(self):
        pass

