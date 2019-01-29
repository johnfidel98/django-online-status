# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from json import JSONEncoder
from online_status.status import OnlineStatus


class OnlineStatusJSONEncoder(JSONEncoder):
    def default(self, obj):
        print("---")
        print(type(obj))
        print("---")
        if isinstance(obj, OnlineStatus):
            seen = obj.seen.isoformat()
            # TODO adapt to custom user model
            user = {
                'username': obj.user.get_username(),
                'first_name': getattr(obj.user, 'first_name', ''),
                'last_name': getattr(obj.user, 'last_name', ''),
            }
            return {'user': user, 'seen': seen, 'status': obj.status, }
        else:
            pass
            # raise TypeError(repr(obj) + " is not JSON serializable")
