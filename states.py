from database.models import Section

STATES = {
    'first_state': 'state0',
    'states': {
        'state0':{
            'text': 'Для старта работы напишите мне "Начать"',
            'tokens': 'начать',
            'error_text': 'Для старта работы напишите мне "Начать"',
            'handler': 'state0_msg_handler',
            'next_state': 'state1',
            'previous_state': None
        },
        'state1': {
            'text': 'Выберите нужную категорию цифрой',
            'tokens': 'generate_tokens_for_state1',  # in message handler
            'error_text': 'Неправильный ввод, нет такого ответа',
            'handler': 'state1_msg_handler',
            'next_state': 'state2',
            'previous_state': 'state0'
        },
        'state2': {
            'text': 'Если Вам понравился данный вариант нажмите кнопку заказать',
            'tokens': ('далее', 'назад', 'в меню', 'заказать'),
            'error_text': 'Неправильный ввод, нет такого ответа',
            'handler': 'state2_msg_handler',
            'next_state': None,
            'previous_state': 'state1'
        },
    }
}
