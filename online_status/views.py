from django.shortcuts import render
from django.core.cache import cache
from django.http import JsonResponse
from online_status.utils import OnlineStatusJSONEncoder
from online_status import settings as config
from django.contrib.auth.decorators import login_required


@login_required
def users(request):
    """Sample user dashboard able for customization, see BASE_TEMPLATE in settings.py"""
    return render(request, 'online_status/users.html', {})


def users_json(request):
    """
    Json of online users, useful f.ex. for refreshing a online users list via
    an ajax call or something
    """
    online_users = cache.get(config.CACHE_USERS)
    print(online_users)
    return JsonResponse(
        online_users, encoder=OnlineStatusJSONEncoder, safe=False
    )
