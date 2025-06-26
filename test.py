import settings


def list_public_models():
    from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
    from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
    from clarifai_grpc.grpc.api.status import status_code_pb2

    channel = ClarifaiChannel.get_grpc_channel()
    app = service_pb2_grpc.V2Stub(channel)
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'), )

    request = service_pb2.ListModelsRequest(
        user_app_id=resources_pb2.UserAppIDSet(user_id="clarifai", app_id="main")
    )

    response = app.ListModels(request, metadata=metadata)

    if response.status.code == status_code_pb2.SUCCESS:
        print("Доступные модели:")
        for model in response.models:
            print(f"ID: {model.id}, Название: {model.name}")
    else:
        print("Не удалось получить список моделей:", response.status.description)










if __name__ == "__main__":
    list_public_models()