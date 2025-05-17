from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def send_ws_message(user_id: int, data: dict):
    channel_layer = get_channel_layer()
    if channel_layer is None:
        raise RuntimeError("Channel layer topilmadi. Django Channels sozlanmagan bo‘lishi mumkin.")
    group_name = f"user_{user_id}"
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "send_message",
            "data": data,
        }
    )
