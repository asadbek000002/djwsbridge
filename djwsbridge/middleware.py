from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()


@database_sync_to_async
def get_user_from_jwt(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        return User.objects.get(id=user_id)
    except (TokenError, User.DoesNotExist) as e:
        print(f"[JWT ERROR] {e}")
        return None


class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope.get("headers", {}))
        token = None

        if b"authorization" in headers:
            auth_header = headers[b"authorization"].decode()
            if auth_header.lower().startswith("bearer "):
                token = auth_header.split(" ")[1]

        user = await get_user_from_jwt(token) if token else None

        if user is None:
            print("[AUTH] WebSocket ulanish rad etildi: foydalanuvchi aniqlanmadi yoki token noto‘g‘ri.")
            await send({
                "type": "websocket.close",
                "code": 4001
            })
            return

        scope["user"] = user
        return await super().__call__(scope, receive, send)
