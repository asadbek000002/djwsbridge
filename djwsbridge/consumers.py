# djwsbridge/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
import json

from .utils import get_chat_model, get_message_model, filter_valid_fields
from django.core.exceptions import ImproperlyConfigured

User = get_user_model()
ALLOWED_MESSAGE_TYPES = getattr(settings, "DJWSBRIDGE_ALLOWED_TYPES", None)


class UserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if user is None or not user.is_authenticated:
            await self.close()
            return

        self.user = user
        self.user_id = user.id
        self.group_name = f"user_{self.user_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_json({"error": "Invalid JSON format"})
            return

        msg_type = data.get("type")
        # Message type tekshirish (agar ALLOWED_MESSAGE_TYPES mavjud bo‘lsa)
        if ALLOWED_MESSAGE_TYPES is not None and msg_type not in ALLOWED_MESSAGE_TYPES:
            await self.send_json({"error": f"Invalid message type: {msg_type}"})
            return

        # Chat va Message modellar mavjudligini tekshirish
        Chat = None
        Message = None
        try:
            Chat = get_chat_model()
        except ImproperlyConfigured:
            pass

        try:
            Message = get_message_model()
        except ImproperlyConfigured:
            pass

        recipient = None
        if "recipient" in data:
            try:
                recipient = int(data["recipient"])
                recipient = await User.objects.aget(id=recipient)
            except (ValueError, User.DoesNotExist):
                await self.send_json({"error": "Invalid or non-existent recipient_id"})
                return

            if getattr(recipient, "is_blocked", False):
                await self.send_json({"error": "Recipient is blocked"})
                return

        # Chat va message modeli mavjud bo‘lsa, xabarni saqlaymiz
        if Chat and Message and recipient:
            chat = await sync_to_async(self.get_or_create_chat)(Chat, self.user_id, recipient.id)

            # sender va recipient ni instance ko‘rinishida qo‘shamiz
            data_for_model = data.copy()
            data_for_model["sender"] = self.user
            data_for_model["recipient"] = recipient
            data_for_model["chat"] = chat

            try:
                valid_data = filter_valid_fields(Message, data_for_model)
                await sync_to_async(Message.objects.create)(**valid_data)
            except ValueError as e:
                await self.send_json({"error": str(e)})
                return

        # Har doim xabarni uzatamiz: avvalo boshqa foydalanuvchiga
        if recipient:
            await self.channel_layer.group_send(
                f"user_{recipient.id}",
                {
                    "type": "send_message",
                    "data": {
                        "sender": self.user_id,
                        **data
                    }
                }
            )

        # O‘ziga ham yuboriladi (feedback)
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_message",
                "data": {
                    "sender": self.user_id,
                    **data
                }
            }
        )

    @staticmethod
    def get_or_create_chat(Chat, user1_id, user2_id):
        chat = Chat.objects.filter(participants__id=user1_id) \
            .filter(participants__id=user2_id) \
            .distinct().first()
        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(user1_id, user2_id)
        return chat

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_message(self, event):
        data = event.get("data", {})
        if not isinstance(data, dict):
            await self.send_json({"error": "Invalid message format"})
            return
        await self.send_json(data)

    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))
