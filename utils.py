import settings
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from random import randint, choice


def main_keyboard():
    return ReplyKeyboardMarkup([
        ["Прислать котика", KeyboardButton("Мои координаты", request_location=True)]
    ], resize_keyboard=True)


def get_smile(user_data):
    if "emoji" not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data["emoji"]


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Выше число {user_number} мое число {bot_number} - Вы выиграли!"
    elif user_number == bot_number:
        message = f"Выше число {user_number} мое число {bot_number} - ничья!"
    else:
        message = f"Выше число {user_number} мое число {bot_number} - вы проиграли!"
    return message
