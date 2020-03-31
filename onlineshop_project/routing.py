from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import django_chatter.routing

application = ProtocolTypeRouter({
    'websocket': AuthenticationMiddleware(
        URLRouter(django_chatter.routing.websocket_urlpatterns)
    )
})
