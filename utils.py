import settings

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from random import randint, choice

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2


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


def has_objects_on_image(file_name, object_name):
    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.PAT}'), )
    userDataObject = resources_pb2.UserAppIDSet(user_id='clarifai', app_id='main')

    with open(file_name, 'rb') as f:
        file_data = f.read()
        image = resources_pb2.Image(base64=file_data)

    request = service_pb2.PostModelOutputsRequest(
        user_app_id=userDataObject,
        model_id="general-image-recognition",
        version_id="aa7f35c01e0642fda5cf400f543e7c40",
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))
        ])
    response = app.PostModelOutputs(request, metadata=metadata)
    # print(response)
    return check_response_for_object(response, object_name)


def check_response_for_object(response, object_name):
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.85:
                return True
    else:
        print(f'Ошибка распознования картинки {response.outputs[0].status.details}')

    return False



if __name__ == "__main__":
    print(has_objects_on_image('images/cat.jpg', 'dog'))
    print(has_objects_on_image('images/dog.jpg', 'dog'))