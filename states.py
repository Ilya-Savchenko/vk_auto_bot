STATES = {
    'first_state': 'state1',
    'states': {
        'state1': {
            'text': 'Выберите нужную категорию цифрой',
            'error_text': 'Неправильный ввод, попробуйте еще раз',
            'handler': 'state1_msg_handler',
            'next_state': 'state2',
            'previous_state': None
        },
        'state2': {
            'text': 'Если Вам понравился данный вариант нажмите кнопку заказать',
            'error_text': 'неправильный ввод',
            'handler': 'state2_msg_handler',
            'next_state': None,
            'previous_state': 'state1'
        },
    }
}


