# [WIP] Websocket by JSON-RPC protocol for Django Channels

Library for using websocket in django(with channels) in jsonrpc way

### JSON-RPC specification
https://www.jsonrpc.org/specification

## Installing
WIP

## Usage example


Add wejr to django INSTALLED_APPS before your apps
```python
INSTALLED_APPS = [
    ...
    "wejr",
    ...
]
```
    

Configure channel layer via Redis PubSub
```python
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}
```

Define routers, methods, params schemas
```python
from dataclasses import dataclass, asdict
from wejr.router import Router

@dataclass
class ChatId:
    id: int

@dataclass
class MessageCreated:
    author_id: int
    content: str
    chat_id: int

client = Router()
chat = Router()

@client.method
async def chat_by_id(consumer, request, params: ChatId):
    chat = get_chat_data(params.id)
    consumer.send_result(request, chat)

@chat.method
async def message_created(consumer, request, params: MessageCreated):
    consumer.send_notification("", asdict(params))
```


Define consumer
```python
from wejr.consumers import AsyncBaseJsonRpcConsumer
from myproject.app.routers import client, chat

class MyConsumer(AsyncBaseJsonRpcConsumer):
    client_router = client
    group_routers = {
        "chat": chat,
    }
```

Define urls
```python
urlpatterns = [
    re_path(r"v1/ws", MyConsumer.as_asgi()),
]
```

Extend asgi with websocket
```python
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from djangochatws.apps.threadws import urls as ws_urls

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(ws_urls.urlpatterns)
        )
    }
)
```
