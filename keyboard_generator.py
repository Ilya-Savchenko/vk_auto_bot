from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class KeyboardGenerator:

    def __init__(self):
        self.colors = VkKeyboardColor

    def generate_keyboard(self, buttons: list or tuple):
        print(buttons)
        keyboard = VkKeyboard()

        for elem in buttons:
            if 'меню' in str(elem):
                keyboard.add_button(elem, self.colors.NEGATIVE)
            elif 'заказать' in str(elem):
                keyboard.add_line()
                keyboard.add_button(elem, self.colors.POSITIVE)
            else:
                keyboard.add_button(elem, self.colors.PRIMARY)
        return keyboard
