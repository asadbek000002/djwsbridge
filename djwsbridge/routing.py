from django.conf import settings
from djwsbridge.consumers import UserConsumer
from django.urls import re_path


def get_websocket_urlpatterns():
    try:
        prefix = settings.DJWSBRIDGE_WS_PREFIX
        path = settings.DJWSBRIDGE_WS_PATH
    except AttributeError:
        raise RuntimeError(
            "DJWSBRIDGE_WS_PREFIX topilmadi. Iltimos, settings.py faylga quyidagicha yozing:\n\n"
            "DJWSBRIDGE_WS_PREFIX = 'ws/'"
        )

    return [
        re_path(rf'^{prefix}/{path}/$', UserConsumer.as_asgi()),
    ]
