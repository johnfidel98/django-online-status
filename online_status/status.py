# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.cache import cache
from django.utils import timezone
from online_status import settings as config
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import SimpleLazyObject
from django.contrib.auth import get_user_model
from user_agents import parse
# from collections import namedtuple
# import json

_STATUS_TYPE = {
    'offline': _("Offline"),
    'idle': _("Idle"),
    'online': _("Online"),
    'unknown': _("Unknown"),
}
STATUS = lambda: None
STATUS.__dict__ = _STATUS_TYPE


class OnlineStatus(object):
    """Online status data which will be later cached"""

    def __init__(self, request):
        self.user = request.user
        self.status = STATUS.online
        self.seen = timezone.now()
        self.ip = request.META['REMOTE_ADDR']
        self.host = request.META['REMOTE_HOST']
        self.agent = parse(request.META['HTTP_USER_AGENT'])
        self.session = request.session.session_key

    def set_idle(self):
        self.status = STATUS.idle

    def set_online(self, request):
        self.status = STATUS.online
        self.seen = timezone.now()
        self.session = request.session.session_key

    def __repr__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.user, self.status, self.seen,
                                               self.ip, self.host, self.agent, self.session)


def refresh_users_list(request, **kwargs):
    """Updates online users list and their statuses"""

    updated = kwargs.pop('updated', None)
    online_users = []

    for online_status in cache.get(config.CACHE_USERS, []):
        seconds = (timezone.now() - online_status.seen).seconds

        # `updated` will be added into `online_users` later
        if online_status.user == updated.user:
            continue

        # delete expired
        if seconds > config.TIME_OFFLINE:
            cache.delete(config.CACHE_PREFIX_USER % online_status.user.pk)
            continue

        if seconds > config.TIME_IDLE:
            # default value will be used if the second cache is expired
            user_status = cache.get(
                config.CACHE_PREFIX_USER % online_status.user.pk,
                online_status)
            online_status.set_idle()
            user_status.set_idle()
            cache.set(config.CACHE_PREFIX_USER % online_status.user.pk,
                      user_status, config.TIME_OFFLINE)

        online_users.append(online_status)

    if updated.user.is_authenticated:
        online_users.append(updated)

    cache.set(config.CACHE_USERS, online_users, config.TIME_OFFLINE)


def status_for_user(user):
    """Return status for user, duh?"""
    if isinstance(user, SimpleLazyObject):
        key = config.CACHE_PREFIX_USER % user.pk
        return cache.get(key)
    return STATUS.offline


def status_for_allusers():
    """Return status for all registered users, duh?"""
    loggedusers = {}
    for user in get_user_model().objects.all():
        key = config.CACHE_PREFIX_USER % user.pk
        onlinestatus = cache.get(key)
        loggedusers[user.username] = {
            "status": onlinestatus.status if onlinestatus else STATUS.offline,
            "data": onlinestatus
        }
    return loggedusers
