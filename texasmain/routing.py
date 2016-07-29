from channels.routing import route
from apps.pokerapp.consumers import ws_add, ws_message, ws_disconnect

channel_routing = [
    route("websocket.connect", ws_add, path=r'^/table/$'),
    route("websocket.receive", ws_message, path=r'^/table/$'),
    route("websocket.disconnect", ws_disconnect),
]