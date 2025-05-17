
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
git clone https://github.com/username/djwsbridge.git
cd djwsbridge
pip install -e .
```

---

## ⚙️ Django Configuration

Add the following to your `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "daphne",
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

# Path to your Chat model (format: "app_label.ModelName").
DJWSBRIDGE_CHAT_MODEL = "yourapp.Chat"

# Path to your Message model.
DJWSBRIDGE_MESSAGE_MODEL = "yourapp.Message"

# Allowed message types (optional).
DJWSBRIDGE_ALLOWED_TYPES = ["text", "message", "image", "signals"]

# WebSocket URL prefix (protocol).
DJWSBRIDGE_WS_PREFIX = "socket"

# WebSocket URL path.
DJWSBRIDGE_WS_PATH = "mychannel"
```

---

## 🔌 ASGI Configuration (`asgi.py`)

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

## 🧑‍💻 Example Models (`models.py`)

```python
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name="chats")
    created = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    type = models.CharField(max_length=20, default="text")
    created = models.DateTimeField(auto_now_add=True)
```

---

## 📤 Sending Messages from Backend

```python
from djwsbridge.utils import send_ws_message

# Example: send a message from a background task or signal handler
send_ws_message(
    user_id=5,
    data={"type": "text", "content": "Hello! This message was sent from the backend."}
)
```

---

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

---

## 📃 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

- Asadbek  
- GitHub: [@asadbek](https://github.com/asadbek000002)  
- For issues or questions, please open an issue or submit a pull request.

---

## ⭐️ Support

If you find this project useful, please:

- ⭐ Star the repository  
- 🛠 Provide feedback  
- 🔄 Submit suggestions or pull requests  

A reliable, modular, and WebSocket-based real-time communication solution for Django.