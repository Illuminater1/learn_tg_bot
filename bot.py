import logging

import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint, choice
from glob import glob
from emoji import emojize

logging.basicConfig(filename="bot.log", level=logging.INFO)


def greet_user(update, context):
    print("Вызван //start")
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй пользователь {context.user_data['emoji']}!")
    # print(update)


def get_smile(user_data):
    if "emoji" not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, language='alias')
    return user_data["emoji"]


def talk_to_me(update, context):
    context.user_data["emoji"] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {context.user_data['emoji']}")


def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (ValueError, TypeError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message)


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)
    if user_number > bot_number:
        message = f"Выше число {user_number} мое число {bot_number} - Вы выиграли!"
    elif user_number == bot_number:
        message = f"Выше число {user_number} мое число {bot_number} - ничья!"
    else:
        message = f"Выше число {user_number} мое число {bot_number} - вы проиграли!"
    return message


def send_cat_picture(update, context):
    cat_photos_list = glob("images/cat*.jp*g")
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id, open(cat_pic_filename, "rb"))


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
