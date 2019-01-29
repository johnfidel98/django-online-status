from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from online_status.status import OnlineStatus, refresh_users_list
from django.conf import settings
from online_status import settings as config
from importlib import import_module


engine = import_module(settings.SESSION_ENGINE)


class OnlineStatusMiddleware(MiddlewareMixin):
    """Cache OnlineStatus instance for user sessions"""

    def process_request(self, request):
        if request.user.is_authenticated:
            key = config.CACHE_PREFIX_USER % request.user.pk
        elif not config.ONLY_LOGGED_USERS:
            key = config.CACHE_PREFIX_ANONYM_USER % request.session.session_key
        else:
            return
        onlinestatus = cache.get(key)
        if not onlinestatus:
            onlinestatus = OnlineStatus(request)
        else:
            if config.PREVENT_CONCURRENT_LOGIN and request.session.session_key != onlinestatus.session:
                session = engine.SessionStore(session_key=onlinestatus.session)
                session.delete()
            onlinestatus.set_online(request)
        cache.set(key, onlinestatus, config.TIME_OFFLINE)
        refresh_users_list(request, updated=onlinestatus)
        return  # TODO cachar logout request para borrar key
