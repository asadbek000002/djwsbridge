# 🧩 djwsbridge

**`djwsbridge` is a Django Channels-based library for real-time messaging via WebSocket.**  
It enables seamless integration for sending, storing, and broadcasting messages in real-time between users.

---

## ✨ Key Features

- Real-time messaging between users over WebSocket.
- Individual user channels (e.g., `user_{id}`) for private communication.
- Message storage via a customizable `Message` model.
- Chat context management through a customizable `Chat` model.
- Fully configurable through Django's `settings.py`.
- Ability to send messages from the backend using `send_ws_message`.

---

## 🚀 Installation

```bash
pip install djwsbridge
```

### Or install locally (for development):

```bash
git clone https://github.com/asadbek000002/djwsbridge.git
cd djwsbridge
pip install -e .
```

---

### 🔐 Authentication Support

djwsbridge is designed to work exclusively with Django REST Framework and uses JWT (JSON Web Token) authentication
provided by rest_framework_simplejwt.

This allows secure and stateless user authentication for WebSocket connections.

### ⚙️ Django Configuration

Add the following to your `settings.py`:

```python
INSTALLED_APPS = [
    "daphne",
    ...
    "rest_framework",
    "rest_framework_simplejwt",
    "channels",
    "djwsbridge",
]

ASGI_APPLICATION = "your_project.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

# Customizable settings:

# WebSocket URL prefix (protocol).
DJWSBRIDGE_WS_PREFIX = "socket"

# WebSocket URL path.
DJWSBRIDGE_WS_PATH = "mychannel"

# Optional: Allowed message types
DJWSBRIDGE_ALLOWED_TYPES = ["text", "message", "image", "signals"]
```

---

### 🔌 ASGI Configuration (`asgi.py`)

```python
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
django.setup()

from djwsbridge.routing import get_websocket_urlpatterns
from djwsbridge.middleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": TokenAuthMiddleware(
        URLRouter(
            get_websocket_urlpatterns()
        )
    ),
})
```

---

## 🔔 For Signal or Backend Messaging Only (No Chat Required)

Use this mode if you just want to send signals or notifications from the backend via WebSocket. No database models are
needed.

```python
from djwsbridge.utils import send_ws_message

# Example: send a message from a background task or signal handler
send_ws_message(
    user_id=5,
    data={"type": "text", "content": "Hello! This message was sent from the backend."}
)
```

## 🧪 Testing

Open Django shell:

```bash
python manage.py shell
```

Run:

```python
from django.contrib.auth import get_user_model
from djwsbridge.utils import send_ws_message

User = get_user_model()
user = User.objects.get(id=1)

send_ws_message(user.id, {"type": "signals", "content": "Test message!"})
```

✅ This configuration is sufficient to use send_ws_message for sending real-time data to users without requiring chat or
message models.

---

## 💬 For Full Chat Functionality (Chat + Message Storage)

📩 Sending a Message to Another User

If you want to send a message to another user, you must provide the recipient’s user ID using the `recipient` key in the WebSocket message payload `("recipient": 2)`. This ID should correspond to an existing and valid user in the system.
#### Example:

```python
{
    "type": "chat",
    "message": "Hello there!",
    "recipient": 2
}

```

### 🧑‍💻 Example Models (`models.py`)

```python
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name="chats")
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    type = models.CharField(max_length=20, default="text")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> Chat {self.chat.id}: {self.content[:30]}"

```
🔒 Note: `sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")` sender is required in the database model, but when using the WebSocket API, it is automatically inferred from the connected user — you don't need to include it in your JSON payload. All other fields are optional unless explicitly required by your implementation.

### 🧭 Usage Modes

djwsbridge supports two flexible modes:

1. With Database

Define Chat and Message models in settings.py to store chat history:

Add the following to your `settings.py`:

```python
DJWSBRIDGE_CHAT_MODEL = "yourapp.Chat"
DJWSBRIDGE_MESSAGE_MODEL = "yourapp.Message"

```

Useful for saving conversations, showing chat history, or audits.

2. Without Database

Skip model settings to use real-time messaging without saving to the database.

Ideal for lightweight signals, temporary chats, or backend-to-user updates.

This makes djwsbridge suitable for both persistent chat systems and ephemeral real-time communications.

---

## 👨‍💻 Author

- Asadbek
- GitHub: [@asadbek](https://github.com/asadbek000002)
- Telegram: [Asadbek](https://t.me/T_A_N_02)
- For issues or questions, please open an issue or submit a pull request.

---

## ⭐️ Support

If you find this project useful, please:

- ⭐ Star the repository
- 🛠 Provide feedback
- 🔄 Submit suggestions or pull requests

A reliable, modular, and WebSocket-based real-time communication solution for Django.