from glob import glob
import os
from random import choice

from utils import main_keyboard, get_smile, play_random_numbers, has_objects_on_image

def greet_user(update, context):
    print("Вызван старт")
    context.user_data["emoji"] = get_smile(context.user_data)
    update.message.reply_text(
        f"Здравствуй пользователь {context.user_data['emoji']}!",
        reply_markup=main_keyboard())
    # print(update)


def talk_to_me(update, context):
    context.user_data["emoji"] = get_smile(context.user_data)
    text = update.message.text
    print(text)
    update.message.reply_text(f"{text} {context.user_data['emoji']}",
                              reply_markup=main_keyboard())


def guess_number(update, context):
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (ValueError, TypeError):
            message = "Введите целое число"
    else:
        message = "Введите число"
    update.message.reply_text(message,
                              reply_markup=main_keyboard())


def send_cat_picture(update, context):
    cat_photos_list = glob("images/cat*.jp*g")
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id, open(cat_pic_filename, "rb"),
                           reply_markup=main_keyboard())


def user_coordinates(update, context):
    context.user_data["emoji"] = get_smile(context.user_data)
    coords = update.message.location
    update.message.reply_text(
        f"Ваши координаты {coords} {context.user_data['emoji']}!",
        reply_markup=main_keyboard()
    )
    # print(coords)


def check_user_photo(update, context):
    update.message.reply_text("Обрабатываем фото")
    os.makedirs("downloads", exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    file_name = os.path.join("downloads", f"{update.message.photo[-1].file_id}.jpg")
    photo_file.download(file_name)
    update.message.reply_text("Файл сохранен")
    if has_objects_on_image(file_name, 'cat'):
        update.message.reply_text('Обнаружен котик, сохраняю в библиотеку')
        new_file_name = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)
    else:
        os.remove(file_name)
        update.message.reply_text('Тревога! Котик не обнаружен!')
