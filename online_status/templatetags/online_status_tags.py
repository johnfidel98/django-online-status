from datetime import timedelta

from django import template
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.utils import timezone
from online_status import settings as config
from online_status.status import status_for_user, status_for_allusers, STATUS

register = template.Library()


@register.inclusion_tag('online_status/online_users.html')
def online_users(limit=None):
    """Renders a list of OnlineStatus instances"""
    onlineusers = cache.get(config.CACHE_USERS)
    onlineanonymusers = None

    if not config.ONLY_LOGGED_USERS:
        now = timezone.now()

        expire_delta = timedelta(
            0, settings.SESSION_COOKIE_AGE - config.TIME_OFFLINE)
        sessions = Session.objects.filter(
            expire_date__gte=now + expire_delta).values_list(
                'session_key', flat=True)

        onlineanonymusers = [
            cache.get(config.CACHE_PREFIX_ANONYM_USER % session_key, None)
            for session_key in sessions
        ]

        onlineusers = [
            item for item in cache.get(config.CACHE_USERS, [])
            if item.status in (STATUS.idle, STATUS.online) and item.session in sessions
        ]

        if onlineanonymusers and limit:
            onlineanonymusers = onlineanonymusers[:limit]

    if onlineusers and limit:
        onlineusers = onlineusers[:limit]

    return {
        'onlineanonymusers': onlineanonymusers,
        'onlineusers': onlineusers,
    }


@register.inclusion_tag('online_status/logged_users.html')
def logged_users(limit=50):
    """Renders a list of OnlineStatus instances"""
    loggedusers = status_for_allusers()
    # for key, data in loggedusers.items():
    #     print("Key: %s, Data: %s" % (key, data["status"]))
    return {
        'loggedusers': loggedusers,
    }


@register.inclusion_tag('online_status/user_status.html')
def user_status_tag(user):
    """Renders an OnlineStatus for User with UI"""
    status = status_for_user(user)
    return {
        'onlinestatus': status,
    }


@register.simple_tag()
def user_status(user):
    """Renders an OnlineStatus instance for User"""
    return status_for_user(user)
